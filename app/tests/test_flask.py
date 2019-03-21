import pytest

from app import create_app
from settings import SETTINGS, USERNAME, PASSWORD

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
    response2 = test_client.get('/index', follow_redirects=True)

    assert response.status_code == 200
    assert response2.status_code == 200


def test_valid_login(test_client):
    response = test_client.post(
        '/login',
        data=dict(username=USERNAME, password=PASSWORD),
        follow_redirects=True
    )
    assert response.status_code == 200

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200


def test_create(test_client):
    test_client.post(
        '/login',
        data=dict(username=USERNAME, password=PASSWORD),
        follow_redirects=True
    )
    response = test_client.get('/create', follow_redirects=True)
    assert response.status_code == 200
