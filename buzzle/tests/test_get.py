from tempfile import mkdtemp
from uuid import uuid1
from os import path
import aiofiles

from aiohttp import FormData
from pytest import fixture

from buzzle.tests import test_fixture

f = test_fixture


@fixture
async def setup(func):
    data = FormData()
    data.add_field(
        'file',
        open('stuff/ok.png', 'rb'),
        filename='ok.png'
    )

    async with await func.post('/api/contents', data=data) as resp:
        _resp = await resp.json()
        return _resp.get('content_uid')


async def test_get(f):
    content_uid = await setup(f)

    path_to_file = path.join(mkdtemp(), str(uuid1()))

    async with await f.get('/api/contents/{}'.format(content_uid)) as resp:
        async with aiofiles.open(path_to_file, 'wb') as tmp:
            while True:
                chunk = await resp.content.read(2048)
                if not chunk:
                    break
                await tmp.write(chunk)

    assert md5(path_to_file) == md5('stuff/ok.png')


def md5(fname):
    import hashlib
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()
