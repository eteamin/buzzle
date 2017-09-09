from os import remove

import aiofiles


class Content(object):
    def __init__(self, storage_path, redis_connection):
        self.storage_path = storage_path
        self.r = redis_connection

    async def store(self, content, content_name):
        content_path = self._file_path(content_name)
        async with aiofiles.open(content_path, 'wb') as stored_content:
            while True:
                chunk = await content.read_chunk()
                if not chunk:
                    break
                await stored_content.write(chunk)
        self.r.set(content_name, content_path)

    def retrieve(self, content_name):
        return self.r.get(content_name)

    def delete(self, content_name):
        content_path = self.retrieve(content_name)
        remove(content_path)

    def _file_path(self, content_name):
        return '{}/{}'.format(self.storage_path, content_name)


