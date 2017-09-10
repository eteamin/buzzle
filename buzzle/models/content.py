from uuid import uuid1
from os import remove, path, mkdir
from datetime import datetime

import aiofiles
from aiohttp.multipart import MultipartReader


class Content(object):
    content_uid = None
    name = None
    uuid = None
    creation_time = None
    is_deleted = None

    @classmethod
    async def from_request(cls, request, session):
        storage_path = request.app['storage']
        _id = str(uuid1())
        file_path = cls.file_path(storage_path, _id)
        reader = MultipartReader.from_response(request)
        part = await reader.next()
        file = path.join(file_path, part.filename)
        async with aiofiles.open(file, 'wb') as dest:
            while True:
                chunk = await part.read_chunk()
                if not chunk:
                    break
                await dest.write(chunk)
        instance = cls()
        instance.name = part.filename
        instance.uuid = _id
        instance.creation_time = datetime.now()
        instance.is_deleted = False
        return await cls.insert(session, instance)

    @classmethod
    def file_path(cls, storage_path, uid):
        _path = path.join(storage_path, uid)
        mkdir(_path)
        return _path

    @classmethod
    async def insert(cls, session, i):
        insert_query = """
        INSERT INTO CONTENTS (NAME, UUID, iS_DELETED, CREATION_TIME)
        VALUES ('%s', '%s', '%s', '%s')
        RETURNING CONTENT_UID
        """ % (i.name, i.uuid, i.is_deleted, i.creation_time)
        rows = await session.execute(insert_query)
        row = await rows.fetchone()
        return row[0]

    @classmethod
    async def one_or_none(cls, session, content_uid):
        select_query = """
        SELECT (UUID, NAME) FROM CONTENTS WHERE (CONTENT_UID = '%s')
        """ % (content_uid)
        result = await session.execute(select_query)
        if not result.rowcount:
            return None
        row = await result.fetchone()
        return row[0].replace(')', '').replace('(', '').split(',')

