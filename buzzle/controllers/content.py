from aiohttp.web import json_response

from buzzle.models.content import Content
from buzzle.decorators import flush


@flush()
async def post(request, session):
    content_uid = await Content.from_request(request, session)
    return json_response(dict(content_uid=content_uid))

