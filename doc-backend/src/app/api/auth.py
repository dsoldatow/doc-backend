from aiohttp import web
import asyncpg
import json


async def auth_db(db, login, password):
    """"""
    resp = await db.exec_("SELECT id_user FROM auth where login = $1 and password = $2", login, password)
    return resp


async def sign_up(db, login, password, is_doctor):
    resp = await db.exec_("insert into auth(login, password, is_doctor) values($1, $2, $3) "
                          "returning id_user", login, password, is_doctor)
    if is_doctor:
        db.exec_("insert into doctor_profiles(id_doctor) values ($1)", resp[0]['id_user'])
    else:
        db.exec_("insert into user_profiles(id_user) values ($1)", resp[0]['id_user'])

    return resp


def valid(data, keys):
    answer = True
    for key in keys:
        answer*= key in data.keys()
    return bool(answer)


async def auth_handler(request):
    data = await request.post()
    if valid(data, ['login', 'password']):
        return web.HTTPBadRequest()

    response_data = await auth_db(request.app['db'], data['login'], data['password'])

    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data[0])


async def sign_up_handler(request):
    data = await request.post()
    if valid(data, ['login', 'password', 'is_doctor']):
        return web.HTTPBadRequest()
    response_data = []
    try:
        response_data = await sign_up(request.app['db'], data['login'], data['password'], data['is_doctor'])
    except Exception as e:
        if 'dublicate' in str(e):
            return web.HTTPConflict()

    if not response_data:
        return web.HTTPNonAuthoritativeInformation()
    return web.json_response(response_data[0])