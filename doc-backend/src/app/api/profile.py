from aiohttp import web
import asyncpg
import json
from app.db_utils import check_is_doctor

async def auth_db(db, login, password):
    """"""
    resp = await db.exec_("SELECT id_user FROM auth where login = $1 and password = $2", login, password)
    return resp


async def get_profile_user(db, id_user):
    resp = await db.exec_("select * from user_profiles where id_user =  $1", id_user)
    return resp


async def get_profile_doctor(db, id_user):
    resp = await db.exec_("select * from doctor_profiles where id_user =  $1", id_user)
    return resp


def valid(data, keys):
    answer = True
    for key in keys:
        answer *= key in data.keys()
    return not bool(answer)


async def handler_get_profile(request):
    id_user = int(request.match_info['id_user'])

    db = request.app['db']
    response_data = []
    is_doctor = await check_is_doctor(db, id_user)
    if is_doctor:
        response_data = await get_profile_doctor(db, is_doctor)
    elif not is_doctor:
        response_data = await get_profile_user(db, is_doctor)
    else:
        return web.HTTPBadRequest()
    print(response_data)
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
    resp = await db.exec_("""update doctor_profiles set(name,surname,last_name, company, city, spec, description) = 
                             ($1,$2,$3,$4,$5,$6,$7) where id_user=$8 returning *""",
                          data.get('name', ''),
                          data.get('surname', ''),
                          data.get('last_name', ''),
                          data.get('company', ''),
                          data.get('city', ''),
                          data.get('spec', ''),
                          data.get('description', ''),
                          data['id_user']
                          )
    return resp


async def handler_update_profile(request):
    data = await request.json()
    db = request.app['db']
    id_user = data['id_user']
    is_doctor = check_is_doctor(db, id_user)
    if is_doctor:
        response_data = await update_doctor_profile(db, data)
    elif not is_doctor:
        response_data = await update_user_profile(db, data)
    else:
        return web.HTTPBadRequest()

    if not response_data:
        return web.HTTPNonAuthoritativeInformation()

    return web.json_response(response_data[0])


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
 join doctor_profiles
   on  lower(name)      LIKE w1||substr(p1,np,1)
  and lower(surname)    LIKE w2||substr(p2,np,1)
  and lower(last_name) LIKE w3||substr(p3,np,1)""", search)
    return resp


async def search_profile_handler(request):
    search = request.match_info['search']
    response_data = await search_doctors_in_db(request.app['db'], search)

    return web.json_response(response_data)
