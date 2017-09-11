import jwt
from aiohttp.web_exceptions import HTTPUnauthorized


def authorize():
    def wrapper(handler):
        async def wrapped(request, *a, **kw):
            encoded = request.headers.get('X-AUTH-TOKEN')
            if not encoded:
                raise HTTPUnauthorized()

            secret_key = request.app['config'].get('secret_key')
            secret_code = request.app['config'].get('secret_code')

            if jwt.decode(encoded, secret_key, algorithms=['HS256']).get('code') != secret_code:
                raise HTTPUnauthorized()

            return await handler(request, *a, **kw)

        return wrapped
    return wrapper


def db_session():
    def wrapper(handler):
        async def wrapped(request, *a, **kw):
            # Executing the handler inside a db context
            async with await request.app['db'].begin() as session:
                try:
                    return await handler(request, session, *a, **kw)
                except:
                    if session.status == 'ready':
                        await session.rollback()
                    raise

        return wrapped
    return wrapper
