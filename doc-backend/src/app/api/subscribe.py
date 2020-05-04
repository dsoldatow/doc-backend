from aiohttp import web
import asyncpg
import json


async def subscribe_db(db, follower, main_person):
    """"""
    resp = await db.exec_("insert into subscribe(follower, main_person) values($1, $2)", follower, main_person)
    return resp


async def unsubscribe_db(db, follower, main_person):
    """"""
    resp = await db.exec_("delete from subscribe where follower = $1 and main_person=$2", follower, main_person)
    return resp


def valid(data, keys):
    answer = True
    for key in keys:
        answer*= key in data.keys()
    return not bool(answer)


async def unsubscribe_handler(request):
    data = await request.json()
    print(dict(data), data)
    if valid(data, ['follower', 'main_person']):
        return web.HTTPBadRequest()

    response_data = await unsubscribe_db(request.app['db'], data['follower'], data['main_person'])

    return web.HTTPOk()


async def subscribe_handler(request):
    data = await request.json()
    print(dict(data), data)
    if valid(data, ['follower', 'main_person']):
        return web.HTTPBadRequest()

    response_data = await subscribe_db(request.app['db'],data['follower'], data['main_person'])

    return web.HTTPCreated()