from os import remove

import aiofiles


class Content(object):
    def __init__(self, storage_path, redis_connection):
        self.storage_path = storage_path
        self.r = redis_connection

    async def store(self, file, filename):
        file_path = self._file_path(filename)
        async with aiofiles.open(file_path, 'wb') as stored_file:
            while True:
                chunk = await file.read_chunk()
                if not chunk:
                    break
                await stored_file.write(chunk)
        self.r.set(filename, file_path)

    def retrieve(self, filename):
        return self.r.get(filename)

    def delete(self, filename):
        file_path = self.retrieve(filename)
        remove(file_path)

    def _file_path(self, filename):
        return '{}/{}'.format(self.storage_path, filename)
