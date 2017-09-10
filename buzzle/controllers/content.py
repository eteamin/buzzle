from os import path

from aiohttp.web import json_response, FileResponse

from buzzle.models.content import Content
from buzzle.decorators import db_session


@db_session()
async def post(request, session):
    content_uid = await Content.from_request(request, session)
    return json_response(dict(content_uid=content_uid))


@db_session()
async def get(request, session):
    uuid, name = await Content.one_or_none(session, request.match_info['content_uid'])
    if not uuid:
        return json_response(dict(error='content not found'), status=404)

    file = path.join(request.app['storage'], uuid, name)
    return FileResponse(file)
