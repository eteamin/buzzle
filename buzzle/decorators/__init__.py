

def db_session():
    def decorator(handler):
        async def wrapper(request, *a, **kw):
            # Executing the handler inside a db context
            async with await request.app['db'].begin() as session:
                try:
                    return await handler(request, session, *a, **kw)
                except:
                    if session.status == 'ready':
                        await session.rollback()
                    raise

        return wrapper
    return decorator
