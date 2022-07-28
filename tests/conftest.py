import asyncio

import pytest
from car_indicators.main import app
from car_indicators.db.base import Base, async_engine
from fastapi.testclient import TestClient
from pydantic import BaseModel

from .unit_tests.user_test.user_conf_test import (
    LoginUser,
    User,
    created_user_response,
    login_user2,
    user,
    user2,
)


# class User(BaseModel):
#     email = 'user@example.com'
#     nickname = '000'
#     password = 'test_password'
#     is_active = 'true'

# class LoginUser(BaseModel):
#     access_token: str
#     type_token: str

# @pytest.fixture(scope='session')
# def user():
#     return User()

# @pytest.fixture(scope='session')
# def user2():
#     return User(email='user@example.com', nickname = 'test_name2')


def get_client():
    async def create_all_db():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)

    asyncio.run(create_all_db())

    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def client():
    client = get_client()
    yield client


# @pytest.fixture(scope='session')
# def created_user(client, user):
#     response = client.post(
#     '/auth/register',
#     json=user.dict())

#     yield response

#     client.delete(
#     '/auth/', params={'id': response.json()['id']}
#     )


@pytest.fixture(
    params=[
        pytest.param(("asyncio", {"use_uvloop": True}), id="asyncio+uvloop"),
        pytest.param(("asyncio", {"use_uvloop": False}), id="asyncio"),
        pytest.param(
            ("trio", {"restrict_keyboard_interrupt_to_checkpoints": True}), id="trio"
        ),
    ],
    scope="session",
)
def anyio_backend(request):
    return request.param
