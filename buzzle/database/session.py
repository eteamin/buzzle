import aiopg


class DbSession(object):
    engine = None
    connection = None
    cursor = None
    status = None

    def __init__(self, engine, *, transactional=True):
        self.transactional = transactional
        self.engine = engine
        self.connection = None
        self.status = 'new'

    @property
    def pool(self):
        return self.engine.pool

    @classmethod
    def new(cls):
        return cls()

    async def commit(self):
        await self.cursor.execute('COMMIT')
        self.status = 'committed'

    async def rollback(self):
        await self.cursor.execute('ROLLBACK')
        self.status = 'rollbacked'

    async def __aenter__(self):
        self.connection = await self.pool.acquire()
        self.cursor = await self.connection.cursor()
        if self.transactional:
            await self.cursor.execute('BEGIN')
        self.status = 'ready'
        return self

    # noinspection PyUnusedLocal
    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.transactional and self.status == 'ready':
            await self.commit()
        self.cursor.close()
        await self.pool.release(self.connection)

    async def execute(self, query, *, params=None):
        query = query.replace('?', '%s')
        try:
            await self.cursor.execute(query, params)
            return self.cursor
        # noinspection PyBroadException
        except:
            if self.transactional:
                await self.rollback()
            raise


class PostgreSqlEngine(object):
    def __init__(self, conf):
        self.conf = conf

    _pool = None

    @property
    def pool(self):
        if self._pool is None:
            raise ValueError('Engine is noy initialized')
        return self._pool

    @property
    def dsn(self):
        return 'dbname=%s user=%s password=%s host=%s port=%s' % (
            self.conf.get('postgres.db'),
            self.conf.get('postgres.user'),
            self.conf.get('postgres.password'),
            self.conf.get('postgres.host'),
            self.conf.get('postgres.port'),
        )

    async def initialize(self):

        if self._pool is not None:
            raise ValueError('Object is already initialized')

        self._pool = await aiopg.create_pool(
            self.dsn,
            minsize=10,
            timeout=60
        )

    async def shutdown(self):
        self.pool.terminate()
        await self.pool.wait_closed()
        self._pool = None

    async def begin(self):
        return DbSession(self, transactional=True)

    async def session(self):
        return DbSession(self, transactional=False)

    async def execute(self, query: str, *, params=None):
        async with await self.session() as session:
            await session.execute(query, params=params)

    async def __aenter__(self):
        await self.initialize()
        return self

    # noinspection PyUnusedLocal
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.shutdown()

