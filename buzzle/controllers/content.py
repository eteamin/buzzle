from aiohttp.web import json_response

from buzzle.models.content import Content


async def post(request):
    Content.from_request(request)
    return json_response(dict(ok=True))

