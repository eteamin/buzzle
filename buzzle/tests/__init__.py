from webtest import TestApp
from redis import StrictRedis

from buzzle.wsgi import app


def load_app():
    return TestApp(app)


class TestApplication(object):
    def setUp(self):
        self.app = load_app()
        self.r = StrictRedis(db=15)

    def tearDown(self):
        self.r.flushall()

