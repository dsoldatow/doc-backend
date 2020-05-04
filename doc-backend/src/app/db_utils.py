async def check_is_doctor(db, id_user):
    """"""
    resp = await db.exec_("SELECT is_doctor FROM auth where id_user = $1", id_user)
    return resp[0]['is_doctor']