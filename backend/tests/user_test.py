from therapistai.main import app
from fastapi.testclient import TestClient
from therapistai.auth import verify_password


def test_create_user():
    with TestClient(app) as ts:
        resp = ts.post('/user/',
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

    assert data["firstName"] ==  "Lili"
    assert data["lastName"] ==  "white"
    assert data["email"] ==  "foo@example.com"
    assert data["emailProvider"] ==  "google"
    assert data["password"] !=  "1233"
    assert verify_password("1233", data["password"])