from os import path
import asyncio

import yaml
from buzzle.database.session import PostgreSqlEngine


def load_conf():
    config_file = path.abspath(path.join(path.dirname(__file__), '..', 'development.yaml'))
    with open(config_file, 'r') as c:
        return yaml.load(c)


async def init():
    conf = load_conf()
    engine = PostgreSqlEngine(conf)
    await engine.initialize()
    async with await engine.begin() as cursor:
        with open('scheme.sql', 'r') as scheme:
            await cursor.execute(scheme.read())


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init())
