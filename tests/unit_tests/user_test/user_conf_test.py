import pytest
from pydantic import BaseModel
from fastapi.testclient import TestClient 

class User(BaseModel):
    email = 'user@example.com'
    nickname = '000'
    password = 'test_password'
    is_active = 'true'

class UserResponse(BaseModel):
    id: str
    email: str
    nickname: str
    is_active: bool
    is_superuser: bool
    is_verified: bool
    access_token: str
    token_type: str

class LoginUser(BaseModel):
    access_token: str
    type_token: str

@pytest.fixture(scope='session')
def user():
    return User()

@pytest.fixture(scope='session')
def user2():
    return User(email='user2@example.com', nickname = 'test_name2')

@pytest.fixture(scope='session')
def created_user_response(client: TestClient, user: User):
    response = client.post(
    '/auth/register', 
    json=user.dict())

    assert response.status_code == 201, response.status_code

    user_data = response.json()

    response_login = client.post(
        '/auth/jwt/login', 
        data={
                'username':user_data['email'],
                'password':user.password,
            }
        )

    login_data = response_login.json()

    yield UserResponse(**user_data, **login_data)

    client.delete(
    '/auth/', params={'id': response.json()['id']}
    )

@pytest.fixture(scope='session')
def login_user2(client: TestClient, user2):
    response = client.post(
    '/auth/register', 
    json=user2.dict())
    
    response_data = response.json()

    response_login = client.post(
    '/auth/jwt/login',
    data={
        'username':user2.email,
        'password':user2.password,
    }
    )

    data_login = response_login.json()

    yield LoginUser(
        access_token=data_login['access_token'],
        type_token=data_login['token_type']
        )

    client.delete(
    '/auth/', params={'id': response_data['id']}
    )
    

