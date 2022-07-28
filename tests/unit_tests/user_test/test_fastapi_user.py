from pickletools import optimize
from typing import Union
from urllib import response

from fastapi.testclient import TestClient
from hypothesis import given, settings
from hypothesis.strategies import text, emails, booleans, none, characters

import pytest

from car_indicators.db.user.manager import UserManager
from .user_conf_test import LoginUser, UserResponse

from ...conftest import client, get_client, User

optional_bool = booleans() | none()


class TestCreateUser:
    @staticmethod
    @settings(deadline=1000)
    @given(
        nickname=text(min_size=3, max_size=25),
        password=text(
            min_size=4,
            alphabet=characters(
                blacklist_categories=["Cs"], blacklist_characters=["\x00"]
            ),
        ),
    )
    def test_created_user(nickname, password):
        email = "example@email.com"
        data_user = {
            "nickname": nickname,
            "email": email,
            "password": password,
        }

        client = get_client()
        response = client.post("/auth/register", json=data_user)

        assert response.status_code == 201, response.text
        data = response.json()

        assert data["email"] == email
        assert "id" in data
        assert data["nickname"] == nickname
        assert data["is_active"] == True
        assert data["is_superuser"] == False
        assert data["is_verified"] == False

    small_or_big_nickname = text(max_size=2) | text(min_size=26)

    @staticmethod
    @given(nickname=small_or_big_nickname, email=text(), password=text(min_size=3))
    def test_fail_crate_user(nickname, email, password):

        data_user = {
            "nickname": nickname,
            "email": email,
            "password": password,
        }

        client = get_client()
        response = client.post("/auth/register", json=data_user)

        assert response.status_code == 422, response.text

    @staticmethod
    def test_create_same_user(user: User):

        client = get_client()
        response = client.post("/auth/register", json=user.dict())

        assert response.status_code == 201, response.text

        data_user = response.json()
        assert data_user["email"] == user.email

        response2 = client.post("/auth/register", json=user.dict())

        assert response2.status_code == 400, response2.text

        data_user2 = response2.json()

        assert "detail" in data_user2
        assert data_user2["detail"] == "REGISTER_USER_ALREADY_EXISTS"


@pytest.mark.usefixtures("created_user_response")
class TestLogin:
    @staticmethod
    def test_success_login(user: User, client: TestClient):

        response = client.post(
            "/auth/jwt/login",
            data={
                "username": user.email,
                "password": user.password,
            },
        )
        assert response.status_code == 200, response.json()

        login_data = response.json()

        assert "access_token" in login_data
        assert isinstance(login_data["access_token"], str), login_data["access_token"]

        assert login_data["token_type"] == "bearer"

    @staticmethod
    def test_bad_credential_login(client: TestClient, user: User):

        response = client.post(
            "/auth/jwt/login",
            data={"username": user.email, "password": "some_password"},
        )
        assert response.status_code == 400, response.status_code
        login_data = response.json()
        assert "detail" in login_data, login_data
        assert login_data["detail"] == "LOGIN_BAD_CREDENTIALS"

    @staticmethod
    def test_not_valid_data_login(client: TestClient):

        response = client.post(
            "/auth/jwt/login",
            data={"wrong_data": "not_email", "password": "some_password"},
        )
        assert response.status_code == 422, response.json()


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_request_verify(
    created_user_response: UserResponse, client, anyio_backend, monkeypatch
):
    async def mock_on_after_request_verify(*args, **kwargs):
        return None

    monkeypatch.setattr(
        UserManager, "on_after_request_verify", mock_on_after_request_verify
    )

    user_data = created_user_response
    response = client.post(
        "/auth/request-verify-token", json={"email": user_data.email}
    )
    assert response.status_code == 202, response.text
    data_verify = response.json()

    assert not data_verify, data_verify


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_verification(
    created_user_response: UserResponse, client, anyio_backend, monkeypatch
):
    token = "some_token"

    async def mock_verify(*args, **kwargs):
        return created_user_response

    monkeypatch.setattr(UserManager, "verify", mock_verify)

    response = client.post("/auth/verify", json={"token": token})

    assert response.status_code == 200
    assert response.json()["email"] == created_user_response.email


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_request_reset_password(
    created_user_response: UserResponse, client: TestClient, anyio_backend, monkeypatch
):
    async def mock_on_after_forgot_password(*args, **kwargs):
        return None

    monkeypatch.setattr(
        UserManager, "on_after_forgot_password", mock_on_after_forgot_password
    )

    data_user = created_user_response

    response = client.post("/auth/forgot-password", json={"email": data_user.email})

    assert response.status_code == 202, response.text
    data_verify = response.json()

    assert not data_verify, data_verify


@pytest.mark.parametrize("anyio_backend", ["asyncio"])
async def test_reset_password(
    created_user_response: UserResponse, client: TestClient, anyio_backend, monkeypatch
):
    async def mock_reset_password(*args, **kwargs):
        return None

    monkeypatch.setattr(UserManager, "reset_password", mock_reset_password)

    data_user = created_user_response

    response = client.post(
        "/auth/reset-password", json={"token": "some_token", "password": "new_password"}
    )

    assert response.status_code == 200, response.text
    data_verify = response.json()

    assert not data_verify, data_verify


class TestWrongData:

    url_post_json = [
        "/auth/register",
        "/auth/forgot-password",
        "/auth/reset-password",
        "/auth/request-verify-token",
        "/auth/verify",
    ]

    @staticmethod
    @pytest.mark.parametrize("test_url,", url_post_json)
    def test_wrong_post_json(client: TestClient, test_url):
        response = client.post(test_url, json={"wrong_data": "wrong_data"})
        assert response.status_code == 422, response.status_code

    @staticmethod
    def test_wrong_patch_json(client: TestClient):
        response = client.patch("/auth/me", json={"wrong_data": "wrong_data"})
        assert response.status_code == 422, response.status_code


class TestLogout:
    @staticmethod
    def test_logout(login_user2: LoginUser, client: TestClient):

        response = client.post(
            "/auth/jwt/logout",
            headers={"Authorization": f"Bearer {login_user2.access_token}"},
        )

        assert response.status_code == 200, response.status_code

        response = client.post(
            "/auth/jwt/logout", headers={"Authorization": f"Bearer bad_token"}
        )

        assert response.status_code == 401, response.status_code


# def delete_user_password(created_user_response, client):
#     assert created_user_response.status_code == 201
#     data_user = created_user_response.json()


#     response = client.delete('/auth/', params={'id':data_user['id']})

#     assert response.status_code == 204, response.text
#     assert not response.json(), response.json()
