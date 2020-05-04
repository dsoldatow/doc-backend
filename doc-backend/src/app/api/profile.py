from aiohttp import web
import asyncpg
import json


async def auth_db(db, login, password):
    """"""
    resp = await db.exec_("SELECT id_user FROM auth where login = $1 and password = $2", login, password)
    return resp


async def get_profile_user(db, id_user):
    resp = await db.exec_("select * from user_profiles where id_user =  $1", id_user)
    return resp


async def get_profile_doctor(db, id_doctor):
    resp = await db.exec_("select * from doctor_profiles where id_user =  $1", id_doctor)
    return resp


def valid(data, keys):
    answer = True
    for key in keys:
        answer *= key in data.keys()
    return bool(answer)


async def handler_get_profile(request):
    data = await request.post()

    db = request.app['db']
    response_data = []

    if 'id_doctor' in data.keys():
        response_data = await get_profile_doctor(db, data['id_doctor'])
    elif 'id_user' in data.keys():
        response_data = await get_profile_user(db, data['id_user'])
    else:
        return web.HTTPBadRequest()

    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data[0])


async def update_user_profile(request, data):
    pass


async def update_doctor_profile(request, data):
    pass


async def handler_update_profile(request):
    data = await request.post()
    db = request['db']
    if 'id_doctor' in data.keys():
        response_data = await update_doctor_profile(db, data)
    elif 'id_user' in data.keys():
        response_data = await update_user_profile(db, data)
    else:
        return web.HTTPBadRequest()

    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data)
