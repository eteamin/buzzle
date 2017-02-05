

async def post(request, content):
    multipart = await request.multipart()
    file = await multipart.next()
    await content.store_file(file.filename, file)
    # return Response(text='Ok')
#
#
# def get(request, content):
#     key, value = request.query_string.split('=')
#     file = content.get_file(value)
#     # return Response(text=file.decode())
