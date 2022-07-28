from typing import Optional
import uuid

from pydantic import EmailStr, constr, Field

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: str = Field(..., min_length=3, max_length=25)


class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: str = Field(..., min_length=4)
    nickname: str = Field(..., min_length=3, max_length=25)


class UserUpdate(schemas.BaseUserUpdate):
    nickname: Optional[str] = Field(..., min_length=3, max_length=25)
