import time

import pytest
from fastapi import status
from pydantic import ValidationError

from .conftest import DEFAULT_USER_PASS, DEFAULT_USER_NAME, DEFAULT_USER_EMAIL, USER_CREATE_DATA, auth_header
from ..crud import RefreshTokens, Users, AccessTokens
from ..schemas import table_rows
from ..schemas.tokens import AccessTokenOut

USERS_ENDPOINT = "users/"
USER_PRIVATE_DATA_URL = "users/me"
LOGIN_URL = "login/"
REVOKE_URL = "revoke/"


@pytest.mark.asyncio
async def test_open_docs_page(client):
    response = await client.get("docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_404_if_page_does_not_exist(client):
    response = await client.get("THIS/PAGE/DOES/NOT/EXIST")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_registration_with_valid_data(client):
    response = await client.post(USERS_ENDPOINT, json=USER_CREATE_DATA.dict())
    response_data = response.json()
    assert response_data["username"] == DEFAULT_USER_NAME
    assert response_data["email"] == DEFAULT_USER_EMAIL
    assert response.status_code == status.HTTP_201_CREATED
    assert DEFAULT_USER_PASS not in response.text


@pytest.mark.asyncio
async def test_failed_registration_if_not_unique_username(default_user, client):
    user_with_same_username = USER_CREATE_DATA.copy()
    user_with_same_username.email = "ANOTHER" + DEFAULT_USER_EMAIL
    response = await client.post(USERS_ENDPOINT, json=user_with_same_username.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_failed_registration_if_not_unique_email(default_user, client):
    user_with_same_email = USER_CREATE_DATA.copy()
    user_with_same_email.username = "ANOTHER" + DEFAULT_USER_NAME
    response = await client.post(USERS_ENDPOINT, json=user_with_same_email.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.asyncio
async def test_login(default_user, client):
    response = await client.post(
        LOGIN_URL,
        data={'username': default_user.username, 'password': DEFAULT_USER_PASS},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    assert AccessTokenOut(**response.json())  # validate response content


@pytest.mark.asyncio
async def test_failed_login_wrong_password(default_user, client):
    response = await client.post(
        LOGIN_URL,
        data={'username': default_user.username, 'password': "__WRONG_PASSWORD"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    with pytest.raises(ValidationError):
        assert AccessTokenOut(**response.json())  # validate response content


@pytest.mark.asyncio
async def test_failed_login_user_does_not_exist(default_user, client):
    response = await client.post(
        LOGIN_URL,
        data={'username': "__WRONG_USERNAME", 'password': DEFAULT_USER_PASS},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    with pytest.raises(ValidationError):
        assert AccessTokenOut(**response.json())  # validate response content


@pytest.mark.asyncio
async def test_revoke_tokens(client, token_pair, default_user):
    cookies = {"refresh_token": token_pair.refresh_token, "client_id": str(default_user.id)}
    response = await client.post(REVOKE_URL, json=token_pair.dict(), cookies=cookies)
    assert response.status_code == 200
    assert AccessTokenOut(**response.json())


@pytest.mark.asyncio
async def test_failed_revoke_tokens_if_refresh_token_expired(client, token_pair, default_user):
    cookies = {"refresh_token": token_pair.refresh_token, "client_id": str(default_user.id)}
    await RefreshTokens.change_expire_term(default_user.id, token_pair.refresh_token, time.time() - 100)
    response = await client.post(REVOKE_URL, json=token_pair.dict(), cookies=cookies)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_failed_revoke_tokens_if_refresh_token_invalid(client, token_pair, default_user):
    cookies = {"refresh_token": token_pair.refresh_token + "_invalid", "client_id": str(default_user.id)}
    await RefreshTokens.change_expire_term(default_user.id, token_pair.refresh_token, time.time() - 100)
    response = await client.post(REVOKE_URL, json=token_pair.dict(), cookies=cookies)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_failed_revoke_tokens_if_refresh_token_belongs_to_another_user(client, token_pair):
    another_user = await Users.create(username="ANOTHER_USER", password="Another_Password", email="another@email")
    cookies = {"refresh_token": token_pair.refresh_token, "client_id": str(another_user.id)}
    response = await client.post(REVOKE_URL, json=token_pair.dict(), cookies=cookies)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.asyncio
async def test_get_private_user_data(client, token_pair):
    response = await client.get(
        USER_PRIVATE_DATA_URL,
        headers={"Authorization": " ".join((token_pair.token_type, token_pair.access_token))}
    )
    assert response.status_code == 200
    assert DEFAULT_USER_EMAIL in response.text


@pytest.mark.asyncio
async def test_failed_get_private_user_data_invalid_token(client, token_pair):
    response = await client.get(
        USER_PRIVATE_DATA_URL,
        headers={"Authorization": " ".join((token_pair.token_type, token_pair.access_token, "_invalid"))}
    )
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert DEFAULT_USER_EMAIL not in response.text


@pytest.mark.asyncio
async def test_failed_get_private_user_data_expired_token(client, default_user):
    access_token = await AccessTokens.create(user_id=default_user.id, expire_delta=-10)
    response = await client.get(USER_PRIVATE_DATA_URL,
                                headers={"Authorization": " ".join(("Bearer", access_token.body))})
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert DEFAULT_USER_EMAIL not in response.text


TableRowsUrl = "table/rows/"


@pytest.mark.asyncio
async def test_failed_get_private_user_data_without_token(client, token_pair):
    response = await client.get(USER_PRIVATE_DATA_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    assert DEFAULT_USER_EMAIL not in response.text


@pytest.mark.asyncio
async def test_delete_table_row(db, access_token, default_table_row, client):
    url = TableRowsUrl + str(default_table_row.id)
    assert default_table_row in db
    response = await client.delete(url, headers=auth_header(access_token))
    assert response.status_code == 200
    assert default_table_row not in db


@pytest.mark.asyncio
async def test_failed_delete_table_row_not_found(db, access_token, client):
    url = TableRowsUrl + '999'
    response = await client.delete(url, headers=auth_header(access_token))
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_get_table_row(db, default_table_row, client, access_token):
    url = TableRowsUrl + str(default_table_row.id)
    response = await client.get(url, headers=auth_header(access_token))
    assert response.status_code == 200
    assert response.json()['id'] == default_table_row.id
    assert response.json()['name'] == default_table_row.name


@pytest.mark.asyncio
async def test_get_table_rows(table, client, access_token):
    response = await client.get(TableRowsUrl, headers=auth_header(access_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == len(table)


@pytest.mark.asyncio
async def test_get_table_rows_if_empty_table(db, client, access_token):
    response = await client.get(TableRowsUrl, headers=auth_header(access_token))
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0


@pytest.mark.asyncio
async def test_get_table_rows_with_limit_and_offset(db, table, client, access_token):
    response = await client.get(TableRowsUrl + "?limit=2&offset=1", headers=auth_header(access_token))
    assert response.status_code == 200
    rows = response.json()
    ids = [row['id'] for row in rows]
    assert ids == [2, 3]


@pytest.mark.asyncio
async def test_get_table_rows_where_id_eq_2(db, table, client, access_token):
    response = await client.get(TableRowsUrl + "?filter_by=id__eq:2", headers=auth_header(access_token))
    assert response.status_code == 200
    rows = response.json()
    ids = [row['id'] for row in rows]
    assert rows and all(id_ == 2 for id_ in ids)


@pytest.mark.asyncio
async def test_get_table_rows_where_id_greate_or_equal_2(db, table, client, access_token):
    response = await client.get(TableRowsUrl + "?filter_by=id__ge:2", headers=auth_header(access_token))
    assert response.status_code == 200
    rows = response.json()
    ids = [row['id'] for row in rows]
    assert rows and all(id_ >= 2 for id_ in ids)


@pytest.mark.asyncio
async def test_get_table_rows_where_quantity_lower_3(db, table, client, access_token):
    response = await client.get(TableRowsUrl + "?filter_by=quantity__lt:2", headers=auth_header(access_token))
    assert response.status_code == 200
    rows = response.json()
    quantities = [row['quantity'] for row in rows]
    assert rows and all(quantity < 3 for quantity in quantities)


@pytest.mark.asyncio
async def test_get_table_rows_filtered_by_name(db, table, client, access_token):
    response = await client.get(TableRowsUrl + "?filter_by=name__like:%_3", headers=auth_header(access_token))
    assert response.status_code == 200
    rows = response.json()
    names = [row['name'] for row in rows]
    assert rows and all(name.endswith("_3") for name in names)


@pytest.mark.asyncio
async def test_get_table_rows_with_limit_offset_and_ordering(db, table, client, access_token):
    response = await client.get(TableRowsUrl + "?limit=2&offset=1&ordering_fields=-name",
                                headers=auth_header(access_token))
    assert response.status_code == 200
    rows = response.json()
    ids = [row['id'] for row in rows]
    assert ids == [2, 1]


@pytest.mark.asyncio
async def test_post_table_row(client, access_token):
    table_row_create_data = {"name": "_test_post_table_row", "distance": 10, "quantity": 5}
    response = await client.post(TableRowsUrl, json=table_row_create_data, headers=auth_header(access_token))
    created_row = response.json()
    assert response.status_code == 201
    table_rows.TableRow(**created_row)  # validate


@pytest.mark.asyncio
async def test_patch_table_row(client, access_token, table, db):
    url = TableRowsUrl + str(table[-1].id)
    data = {"name": "_test_patch_table_row"}
    response = await client.patch(url, json=data, headers=auth_header(access_token))
    assert response.status_code == 200
    assert table[-1].name == data['name']


@pytest.mark.asyncio
async def test_put_table_row(client, access_token, table):
    url = TableRowsUrl + str(table[-1].id)
    data = {"name": "_test_put_table_row", "distance": int(table[-1].distance + 10)}
    response = await client.put(url, json=data, headers=auth_header(access_token))
    assert response.status_code == 200
    assert table[-1].name == data['name']
    assert table[-1].distance == data['distance']


@pytest.mark.asyncio
async def test_failed_patch_table_row_not_found(client, access_token):
    url = TableRowsUrl + str(999)
    data = {"name": "_test_failed_patch_table_row_not_found"}
    response = await client.patch(url, json=data, headers=auth_header(access_token))
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_failed_put_table_row_not_found(client, access_token):
    url = TableRowsUrl + str(999)
    data = {"name": "_test_failed_put_table_row_not_found"}
    response = await client.put(url, json=data, headers=auth_header(access_token))
    assert response.status_code == 404
