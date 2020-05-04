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


async def update_user_profile(db, data):
    resp = await db.exec_("""update user_profiles set(name,surname,last_name, company, city, spec, description = 
                                = ($1,$2,$3,$4,$5) where id_user=$6 returning *""",
                          data.get('name', ''),
                          data.get('surname', ''),
                          data.get('last_name', ''),
                          data.get('city', ''),
                          data.get('description', ''),
                          data['id_user']
                          )
    return resp


async def update_doctor_profile(db, data):
    resp = await db.exec_("""update doctor_profiles set(name,surname,last_name, company, city, spec, description = 
                            = ($1,$2,$3,$4,$5,$6,$7) where id_doctor=$8 returning *""",
                          data.get('name', ''),
                          data.get('surname', ''),
                          data.get('last_name', ''),
                          data.get('company', ''),
                          data.get('city', ''),
                          data.get('spec', ''),
                          data.get('description', ''),
                          data['id_doctor']
                          )
    return resp


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


async def search_doctors_in_db(db, search):
    resp = await db.exec_("""select distinct doctor_profiles.*
  from
  (
   select split_part(S,' ',N.column1) w1,split_part(S,' ',N.column2) w2,
          split_part(S,' ',N.column3) w3,
          substr('%%',2-N.column1/2) p1,substr('%%',2-N.column2/2) p2,
          substr('%%',2-N.column3/2) p3,(rtrim(S) like '% _')::int+1 np
     from (values(1,2,3),(1,3,2),(2,1,3),(2,3,1),(3,2,1),(3,1,2)) N,
          (select Cast(lower($1) as varchar) S) S
  ) A
 join users
   on  lower(name)      LIKE w1||substr(p1,np,1)
  and lower(surname)    LIKE w2||substr(p2,np,1)
  and lower(last_name) LIKE w3||substr(p3,np,1)""", search)
    return resp


async def search_profile_handler(request):
    data = await request.post()
    response_data = await search_doctors_in_db(request['db'], data.get('search'))

    return web.json_response(response_data)
