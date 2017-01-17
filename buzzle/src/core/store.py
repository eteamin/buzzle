import aiofiles
import redis


class Storage(object):
    def __init__(self, path):
        self.path = path
        self.r = redis.StrictRedis()

    async def store_file(self, filename, buffer):
        storage_path = '%s/%s' % (self.path, filename)
        async with aiofiles.open(storage_path, 'wb') as stored_file:
            while True:
                chunk = await buffer.read_chunk()
                if not chunk:
                    break
                await stored_file.write(chunk)
        self.r.set(filename, storage_path)

    async def get_file(self, filename):
        return self.r.get(filename)
