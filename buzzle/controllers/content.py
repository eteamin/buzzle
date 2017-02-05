

async def post(request, storage):
    multipart = await request.multipart()
    file = await multipart.next()
    await storage.store_file(file.filename, file)
    # return Response(text='Ok')

async def get(request, storage):
    key, value = request.query_string.split('=')
    file = await storage.get_file(value)
    # return Response(text=file.decode())
