from os import path
from aiohttp.web import Application, Response, run_app

import buzzle
from buzzle.src.core.store import Storage

PATH = path.abspath(path.dirname(buzzle.__file__))
storage = Storage(PATH)

async def post(request):
    multipart = await request.multipart()
    file = await multipart.next()
    await storage.store_file(file.filename, file)
    return Response(text='Ok')

async def get(request):
    key, value = request.query_string.split('=')
    file = await storage.get_file(value)
    return Response(text=file.decode())

buzzle_app = Application()
buzzle_app.router.add_post('/apiv1/', post)
buzzle_app.router.add_get('/apiv1/', get)
