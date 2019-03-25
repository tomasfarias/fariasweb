import pytest

from app import create_app, db
from app.models import User, Post
from settings import SETTINGS


def populate_db(db):
    db.drop_all()
    db.create_all()

    admin = User(
        username='admin', email='admin@test.com', password='test'
    )
    db.session.add(admin)
    db.session.commit()


def login(client, username, password):
    response = client.post(
        '/login',
        data=dict(username='admin', password='test'),
        follow_redirects=True
    )
    return response


@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app(SETTINGS)
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    with ctx:
        populate_db(db)

    ctx.push()

    yield testing_client

    db.session.remove()
    db.drop_all()
    ctx.pop()


def test_index(test_client):
    response = test_client.get('/', follow_redirects=True)
    response2 = test_client.get('/index', follow_redirects=True)

    assert response.status_code == 200
    assert response2.status_code == 200


def test_valid_login(test_client):
    response = login(test_client, 'admin', 'test')

    assert response.status_code == 200
    assert b'Create' in response.data
    assert b'Logout' in response.data

    response = test_client.get('/logout', follow_redirects=True)
    assert response.status_code == 200
    assert b'Create' not in response.data
    assert b'Logout' not in response.data


def test_create(test_client):
    login(test_client, 'admin', 'test')
    response = test_client.post(
        '/create',
        data=dict(
            title='This is a test',
            tags=['tag-test', 'old-tag'],
            body='Post body'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'This is a test' in response.data
    assert b'Post body' in response.data
    assert b'tag-test' in response.data


def test_post_url(test_client):
    response = test_client.get('/post/this-is-a-test', follow_redirects=True)
    assert response.status_code == 200
    assert b'This is a test' in response.data
    assert b'Post body' in response.data
    assert b'tag-test' in response.data


def test_update(test_client):
    post = Post.query.first()
    response = test_client.get(f'/update/{post.id}', follow_redirects=True)
    assert response.status_code == 200
    assert b'This is a test' in response.data
    assert b'Post body' in response.data
    assert b'tag-test' in response.data

    response = test_client.post(
        f'/update/{post.id}',
        data=dict(
            title='New test title',
            tags=['new-tag', 'tag-test', 'tag-test-2'],
            body='New and interesting body'
        ),
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'New test title' in response.data
    assert b'New and interesting body' in response.data
    assert b'new-tag' in response.data
    assert b'tag-test' in response.data


def test_delete(test_client):
    post = Post.query.first()
    response = test_client.get(
        f'/delete/{post.id}',
        follow_redirects=True
    )
    assert response.status_code == 200
    assert b'New test title' not in response.data
    assert b'New and interesting body' not in response.data
    assert b'new-tag' not in response.data
    assert b'tag-test' not in response.data
