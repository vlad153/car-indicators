
from typing import Optional
import uuid

from pydantic import EmailStr, constr

from fastapi_users import schemas

class UserRead(schemas.BaseUser[uuid.UUID]):
    nickname: constr(min_length=3, max_length=25)

class UserCreate(schemas.CreateUpdateDictModel):
    email: EmailStr
    password: constr(min_length=4)
    nickname: constr(min_length=3, max_length=25)

class UserUpdate(schemas.BaseUserUpdate):
    nickname: Optional[constr(min_length=3, max_length=25)] = None

