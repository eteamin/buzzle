from aiohttp import streamer, FormData

from buzzle.tests import test_fixture

f = test_fixture


@streamer
def file_sender(writer, file_name=None):
    with open(file_name, 'rb') as file:
        chunk = file.read(2**16)
        while chunk:
            yield from writer.write(chunk)
            chunk = file.read(2**16)


async def test_post_content(f):
    data = FormData()
    data.add_field(
        'file',
        open('stuff/ok.png', 'rb'),
        filename='ok.png'
    )

    resp = await f.post('/api/content', data=data)
    assert await resp.json().get('ok') is True
