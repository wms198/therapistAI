import pytest
from fastapi.testclient import TestClient
from therapistai.auth import verify_password
from therapistai.db.models import User
from therapistai.main import app

def _set_token(client, token):
    client.headers = {'Authorization': f'Bearer {token}'}
    return client

@pytest.fixture
def password():
    return '1233'

@pytest.fixture
def user(password):
    payload = {
        "firstName": "Lili",
        "lastName": "white",
        "email": "foo@example.com",
        "emailProvider": "google",
        "password": password
    }
    with TestClient(app) as ts:
        resp = ts.post('/user/',json=payload)
    assert resp.status_code == 201
    user = resp.json()
    assert 'id' in user
    assert 'password' not in user
    return User(**user)

@pytest.fixture
def client():
    with TestClient(app) as ts:
        yield ts

@pytest.fixture
def authenticated_client(user, password, client):
    resp = client.post('/auth', json={
        'email': user.email,
        'password': password,
    })
    _set_token(client, resp.json()['access_token'])
    yield client


def test_create_user(client):
    resp = client.post('/user/',
        json={
            "firstName": "Lili",
            "lastName": "white",
            "email": "foo@example.com",
            "emailProvider": "google",
            "password": "1233"
        }
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"]

def test_login(user, password, client):
    resp = client.post('/auth', json={
        'email': user.email,
        'password': password,
    })
    assert resp.status_code == 200
    body = resp.json()
    assert 'access_token' in body
    assert 'refresh_token' in body
    _set_token(client, body['access_token'])
    me = client.get('/user/me')
    assert me.status_code == 200


def test_can_not_create_same_user(user, client):
    resp = client.post('/user/',
        json={
            "firstName": "Lili",
            "lastName": "white",
            "email": user.email,
            "emailProvider": "google",
            "password": "1233"
        }
    )
    assert resp.status_code == 409
    data = resp.json()
    assert data["error"] ==  "User with the email already exists"


def test_get_user(user, client):
    resp = client.get(f'/user/{user.id}')
    assert resp.status_code == 200
    data = resp.json()
    assert data

    assert data["firstName"] ==  user.firstName
    assert data["lastName"] ==  user.lastName
    assert data["email"] ==  user.email
    assert data["emailProvider"] ==  user.emailProvider

def test_get_users(user, client):
    resp = client.get('/user/')
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    assert data[0]["firstName"] ==  user.firstName
    assert data[0]["lastName"] ==  user.lastName
    assert data[0]["email"] ==  user.email 
    assert data[0]["emailProvider"] ==  user.emailProvider

def test_update_user(user, authenticated_client):
    resp = authenticated_client.put(f'/user/{user.id}',
        json={
            "firstName": "Tom"
        })
    assert resp.status_code == 200
    data = resp.json()

    assert data["id"] == user.id
    assert data["firstName"] ==  "Tom"
    assert data["lastName"] ==  user.lastName
    assert data["email"] ==  user.email
    assert data["emailProvider"] ==  user.emailProvider

def test_update_user_not_login(user, client):
    resp = client.put(f'/user/{user.id + 1}',
        json={
            "firstName": "Tom"
        })
    assert resp.status_code == 401


def test_delete(user, client, authenticated_client):
    resp = authenticated_client.delete(f'user/{user.id}')
    assert resp.status_code == 200
    data = resp.json()

    assert data["message"] ==  "Item deleted successfully"
    resp = authenticated_client.delete(f'user/{user.id}')
    assert resp.status_code == 401
    data = resp.json()
    resp = client.get('/user')
    users = resp.json()
    assert not users
