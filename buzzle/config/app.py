# -*- coding: utf-8 -*-
import yaml
from os import path

from aiohttp.web import run_app, Application

from buzzle.database.session import PostgreSqlEngine
from buzzle.config.routes import routes


STORAGE_PATH = path.abspath(path.join(path.dirname(__file__), '..', 'storage'))


def load_conf(test):
    file = 'development.yaml' if not test else 'test.yaml'
    config_file = path.abspath(path.join(path.dirname(__file__), '..', file))
    with open(config_file, 'r') as c:
        return yaml.load(c)


async def init_pg(app):
    conf = app['config']
    engine = PostgreSqlEngine(conf)
    await engine.initialize()
    app['db'] = engine


async def close_pg(app):
    await app['db'].shutdown()


def make_app(test=False):
    onlinelux = Application()
    onlinelux['config'] = load_conf(test)

    # Assign Routes
    for r in routes():
        onlinelux.router.add_route(r.method, r.path, r.handler)

    # Setup DB
    onlinelux.on_startup.append(init_pg)

    # Some DB clean-up stuff
    onlinelux.on_cleanup.append(close_pg)

    return onlinelux


if __name__ == '__main__':
    run_app(make_app(), port=8585)
