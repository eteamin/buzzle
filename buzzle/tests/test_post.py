from aiohttp import FormData

from buzzle.tests import test_fixture

f = test_fixture

async def test_post_content(f):
    data = FormData()
    data.add_field(
        'file',
        open('stuff/ok.png', 'rb'),
        filename='ok.png'
    )

    async with await f.post('/api/contents', data=data) as resp:
        _resp = await resp.json()
        assert _resp.get('content_uid') > 0
