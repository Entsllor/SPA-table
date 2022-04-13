from fastapi import status
from .conftest import DEFAULT_USER_PASS, DEFAULT_USER_NAME, DEFAULT_USER_EMAIL, USER_CREATE_DATA

USERS_ENDPOINT = "users/"


def test_open_docs_page(client):
    response = client.get("docs/")
    assert response.status_code == 200


def test_get_404_if_page_does_not_exist(client):
    response = client.get("THIS/PAGE/DOES/NOT/EXIST")
    assert response.status_code == 404


def test_registration_with_valid_data(client):
    response = client.post(USERS_ENDPOINT, json=USER_CREATE_DATA.dict())
    response_data = response.json()
    assert response_data["username"] == DEFAULT_USER_NAME
    assert response_data["email"] == DEFAULT_USER_EMAIL
    assert response.status_code == status.HTTP_201_CREATED
    assert DEFAULT_USER_PASS not in response.text
