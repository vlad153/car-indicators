from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTableUUID
from sqlalchemy import Column, String

from ..base import Base


class User(SQLAlchemyBaseUserTableUUID, Base):  # type: ignore
    nickname = Column(String(25), unique=True)
