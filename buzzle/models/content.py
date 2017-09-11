from uuid import uuid1
from os import path, mkdir
from datetime import datetime

import aiofiles
from aiohttp.multipart import MultipartReader

from buzzle.database.queries import insert_content, select_content


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
        return await insert_content(session, i)

    @classmethod
    async def one_or_none(cls, session, content_uid):
        return await select_content(session, content_uid)
