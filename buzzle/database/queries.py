

async def insert_content(session, instance):
    query = """
            INSERT INTO CONTENTS (NAME, UUID, iS_DELETED, CREATION_TIME)
            VALUES ('%s', '%s', '%s', '%s')
            RETURNING CONTENT_UID
            """ % (instance.name, instance.uuid, instance.is_deleted, instance.creation_time)
    rows = await session.execute(query)
    row = await rows.fetchone()
    return row[0]


async def select_content(session, content_uid):
    query = """
            SELECT (UUID, NAME) FROM CONTENTS WHERE (CONTENT_UID = '%s')
            """ % (content_uid)
    result = await session.execute(query)
    if not result.rowcount:
        return None
    row = await result.fetchone()
    return row[0].replace(')', '').replace('(', '').split(',')
