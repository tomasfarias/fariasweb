import pytest

from app import create_app
from settings import SETTINGS

TEST_DB = 'test.db'


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(SETTINGS)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()


def test_index(test_client):
    response = test_client.get('/', follow_redirects=True)
    assert response.status_code == 200
