from pytest import fixture

from buzzle.config.app import make_app


@fixture
def test_fixture(loop, test_client):
    """Test fixture to be used in test cases"""
    app = make_app(test=True)
    return loop.run_until_complete(test_client(app))
