from aiohttp import web
import asyncpg
import json


async def create_news(db, data):
    """"""
    resp = await db.exec_("""insert into news(id_user, description, img,link)
                           values ($1, $2, $3, $4) returning 
                           id_news, id_user, description, img, link, "timestamp"::text""", data['id_user'], data['description'], data['img'],
                          data['link'])
    return resp


async def update_news(db, data):
    resp = await db.exec_("""update news set (id_user, description, img,link)
                           = ($1, $2, $3, $4) where id_news = $5 returning 
                           id_news, id_user, description, img, link, "timestamp"::text""", data['id_user'], data['description'],
                          data['img'],
                          data['link'], data['id_news'])
    return resp


async def get_all_news_by_user(db, id_user):
    resp = await db.exec_("""select news.id_news, dp.img, dp.name, dp.surname, dp.last_name, news.id_user, news.description, news.img, link, "timestamp"::text 
                        from news
                        left join doctor_profiles dp on dp.id_user = news.id_user
                         where news.id_user = $1""", id_user)
    return resp

async def get_all_news_for_user(db, id_user):
    resp = await db.exec_(""" select news.id_news, dp.img as user_img, dp.name, dp.surname, dp.last_name, news.id_user, news.description, news.img, link, "timestamp"::text from news
     left join doctor_profiles dp on dp.id_user = news.id_user
     where news.id_user =   any (select main_person from subscribe where follower = $1)
                              order by "timestamp" desc""", id_user)

    return resp

def valid(data, keys):
    answer = True
    for key in keys:
        answer *= key in data.keys()
    return not bool(answer)


async def create_news_handler(request):
    data = await request.json()

    response_data = await create_news(request.app['db'],data)

    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data[0])


async def update_news_handler(request):
    data = await request.json()
    if valid(data, ['id_news']):
        return web.HTTPBadRequest()

    response_data = await update_news(request.app['db'], data)

    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data[0])


async def get_news_by_handler(request):
    id_user = int(request.match_info['id_user'])
    db = request.app['db']
    response_data = await get_all_news_by_user(db, id_user)

    print(response_data)
    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data)


async def get_news_handler(request):
    id_user = int(request.match_info['id_user'])
    db = request.app['db']
    response_data = await get_all_news_for_user(db, id_user)

    print(response_data)
    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data)
