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

buzzle = Application()
buzzle.router.add_post('/', post)

run_app(buzzle)