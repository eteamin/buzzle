# -*- coding: utf-8 -*-
import json
from os import path

from aiohttp.web import run_app, Application

from buzzle.database.session import PostgreSqlEngine


STORAGE_PATH = path.abspath(path.join(path.dirname(__file__), '..', 'storage'))


def load_conf():
    config_file = path.abspath(path.join(path.dirname(__file__), '..', 'development.yaml'))
    with open(config_file, 'r') as c:
        return json.load(c)


async def init_pg(app):
    conf = app['config']
    engine = PostgreSqlEngine(conf)
    await engine.initialize()
    app['db'] = engine


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


def make_app():
    onlinelux = Application()
    onlinelux['config'] = load_conf()

    # Setup DB
    onlinelux.on_startup.append(init_pg)

    # Some DB clean-up stuff
    onlinelux.on_cleanup.append(close_pg)

    return onlinelux


if __name__ == '__main__':
    run_app(make_app(), port=8585)
