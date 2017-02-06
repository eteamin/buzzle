from os import path

from redis import StrictRedis
from aiohttp.web import Response, run_app

import buzzle
from buzzle.models.content import Content

STORAGE_PATH = path.abspath(path.join(path.dirname(buzzle.__file__), 'storage'))
db = 0

async def post(request):
    r = StrictRedis(db=db)
    multipart = await request.multipart()
    file = await multipart.next()
    content = Content(STORAGE_PATH, r)
    await content.store(file, file.filename)
    return Response(text='Ok')

# Yeah it looks weird!!!
async def test_post():
    global db, STORAGE_PATH
    # Setup
    db = 15
    STORAGE_PATH = path.abspath(path.join(path.dirname(buzzle.__file__), 'test_storage'))



#
#
# def get(request, content):
#     key, value = request.query_string.split('=')
#     file = content.get_file(value)
#     # return Response(text=file.decode())
