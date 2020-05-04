from aiohttp import web
import asyncpg
import json
from db_utils import check_is_doctor

async def get_messages_db(db, id_chat):
    """"""
    resp = await db.exec_("""SELECT id_message, id_chat, from_user, to_user, message, "timestamp"::text FROM messages 
                                where id_chat = $1 """, id_chat)
    return resp


async def get_chat_id(db, data):
    resp = await db.exec_("SELECT id_chat FROM chats where (from_user = $1 and to_user = $2) or (from_user = $2 and to_user = $1)", data['from_user'],
                          data['to_user'])
    if not resp:
        resp = await db.exec_("""insert into chats(from_user, to_user) values($1, $2) 
                          returning id_chat""", data['from_user'], data['to_user'])
    return resp[0]


async def create_message_in_db(db, data):
    id_chat = await get_chat_id(db, data)
    resp = await db.exec_("""insert into messages(id_chat,from_user, to_user, message) values($1, $2, $3, $4) 
                          returning id_message, id_chat, from_user, to_user, message, "timestamp"::text""",
                          id_chat['id_chat'], data['from_user'], data['to_user'], data['message'])
    return resp


def valid(data, keys):
    answer = True
    for key in keys:
        answer *= key in data.keys()
    return not bool(answer)


async def get_chats_db(db, id_user):
    """"""
    is_doctor = await check_is_doctor(db,id_user)
    if is_doctor:
        resp = await db.exec_("""    
                             with pum as (SELECT chats.id_chat, chats.from_user, chats.to_user, name, surname, last_name, max(msg.timestamp)
                                 FROM chats 
                                left join doctor_profiles dp on dp.id_user = chats.from_user
                                left join messages msg on msg.id_chat = chats.id_chat
                                where chats.to_user = $1
                                group by chats.id_chat, name, surname, last_name)
                                select pum.id_chat, pum.from_user as "to_user",pum.name, pum.surname, pum.last_name, msg.from_user as msg_from_user, msg.to_user as msg_to_user, pum.max::text as "msg_timestamp", message from pum
                                left join messages msg on msg.timestamp = pum.max
                                 """, id_user)
    else:
        resp = await db.exec_("""    
                                    with pum as (SELECT chats.id_chat, chats.from_user, chats.to_user, name, surname, last_name, max(msg.timestamp)
                                 FROM chats 
                                left join user_profiles dp on dp.id_user = chats.to_user
                                left join messages msg on msg.id_chat = chats.id_chat
                                where chats.from_user = $1
                                group by chats.id_chat, name, surname, last_name)
                                select pum.id_chat, pum.to_user, pum.name, pum.surname, pum.last_name, msg.from_user as msg_from_user, msg.to_user as msg_to_user, pum.max::text as "msg_timestamp", message from pum
                                left join messages msg on msg.timestamp = pum.max
                                         """, id_user)

    return resp


async def get_chats_handler(request):
    id_user = int(request.match_info['id_user'])
    db = request.app['db']
    response_data = await get_chats_db(db, id_user)

    return web.json_response(response_data)


async def get_messages_handler(request):
    id_chat = int(request.match_info['id_chat'])
    response_data = await get_messages_db(request.app['db'], id_chat)

    if not response_data:
        return web.HTTPBadGateway()

    print(response_data)

    return web.json_response(response_data)


async def create_message_handler(request):
    data = await request.json()
    db = request.app['db']
    response_data = await create_message_in_db(db, data)

    return web.json_response(response_data[0])
