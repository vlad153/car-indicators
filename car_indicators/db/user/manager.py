import uuid
from typing import Callable, Optional

import fastapi_users
from fastapi import BackgroundTasks, Depends, Request
from fastapi_users import BaseUserManager, FastAPIUsers, UUIDIDMixin
from fastapi_users.authentication import (AuthenticationBackend,
                                          BearerTransport, JWTStrategy)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from loguru import logger

from ...config import Settings  
from ...email.send_verify_email import send_verification_email
from ...email.send_reset_password import send_reset_password_email
from ..base import async_session
from .model import User

settings = Settings()

def pre_send_email(method_send_email: Callable[[str, str], None]):
    
    def send_email_dependency(background_tasks: BackgroundTasks):
        def send_email_token(receiver_email: str, token: str):
            background_tasks.add_task(method_send_email, receiver_email, token)

        return send_email_token
    return send_email_dependency
    

class UserManager(UUIDIDMixin, BaseUserManager[User, uuid.UUID]):
    
    reset_password_token_secret = settings.secret_key
    verification_token_secret = settings.secret_key

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
        ):
        logger.info('User {} has registered.', user.id)
    
    async def on_after_request_verify(
                self, 
                user: User, 
                token: str, 
                request: Optional[Request] = None
            ) -> None: 
        send_verification_email(user.email, token)

        logger.debug(
            'Verification email sent to user ({}) with token ({}).', 
            user.email, 
            token
        )

    async def on_after_verify(
        self, user: User, request: Optional[Request] = None
        ) -> None:
        logger.info('User {} has verified', user.id)

    
    async def on_after_forgot_password(
            self, 
            user: User, 
            token: str, 
            request: Optional[Request] = None,
            ) -> None:
        send_reset_password_email(user.email, token)
        logger.info('User {} has requested reset password', user.id)

    
class MangerUserDAL(SQLAlchemyUserDatabase):
    pass

async def retrieve_user_manager():
    async with async_session() as session:
        yield UserManager(MangerUserDAL(session, User))

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=settings.secret_key, lifetime_seconds=3600)

bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

auth_backend = AuthenticationBackend(
    name='jwt', transport=bearer_transport, get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, uuid.UUID](retrieve_user_manager, [auth_backend])

current_active_user = fastapi_users.current_user(active=True)


