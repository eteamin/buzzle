from uuid import uuid1
from os import remove

import aiofiles


class Content(object):

    @classmethod
    async def from_request(cls, request):
        content_path = self._file_path(content_name)
        async with aiofiles.open(content_path, 'wb') as stored_content:
            while True:
                chunk = await content.read_chunk()
                if not chunk:
                    break
                await stored_content.write(chunk)

