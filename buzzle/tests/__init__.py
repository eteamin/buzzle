from os import path

from pytest import fixture
import yaml
import jwt

from buzzle.config.app import make_app

CONFIG = path.abspath(path.join(path.dirname(__file__), '..', 'test.yaml'))
TEST_STUFF = path.abspath(path.join(path.dirname(__file__), 'stuff', 'ok.png'))


@fixture
def test_fixture(loop, test_client):
    """Test fixture to be used in test cases"""
    app = make_app(test=True)
    return loop.run_until_complete(test_client(app))


def auth_headers():
    with open(CONFIG, 'r') as c:
        configuration = yaml.load(c)
    secret_key = configuration.get('secret_key')
    secret_code = configuration.get('secret_code')
    return {
        'X-AUTH-TOKEN': jwt.encode({'code': secret_code}, secret_key, algorithm='HS256').decode()
    }


