
from fastapi import APIRouter

from ..db.user.schema import UserRead, UserCreate, UserUpdate
from ..db.user.manager import fastapi_users, auth_backend

auth_user_router = APIRouter(prefix='/auth', tags=['auth'])

auth_user_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix='/jwt'
)

auth_user_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate)
)

auth_user_router.include_router(fastapi_users.get_reset_password_router())

auth_user_router.include_router(fastapi_users.get_verify_router(UserRead))

auth_user_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate)
)