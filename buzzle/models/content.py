from uuid import uuid1
from os import remove, path, mkdir

import aiofiles
from aiohttp.multipart import MultipartReader


class Content(object):

    @classmethod
    async def from_request(cls, request):
        storage_path = request.app['storage']
        file_path = cls.file_path(storage_path)
        reader = MultipartReader.from_response(request)
        part = await reader.next()
        file = path.join(file_path, part.filename)
        async with aiofiles.open(file, 'wb') as dest:
            while True:
                chunk = await part.read_chunk()
                if not chunk:
                    break
                await dest.write(chunk)

    @classmethod
    def file_path(cls, storage_path):
        _path = path.join(storage_path, str(uuid1()))
        mkdir(_path)
        return _path
