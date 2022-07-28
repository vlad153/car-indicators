from typing import Optional, Union
from pydantic import AnyUrl, BaseSettings, PostgresDsn, SecretStr, EmailStr


class SQLiteDsn(AnyUrl):
    allowed_schemes = {
        "sqlite",
        "sqlite+aiosqlite",
    }
    user_required = False


class Settings(BaseSettings):

    host: str = "127.0.0.1"
    port: int = 5000

    smtp_address: str = "localhost"
    smtp_port: int = 2500
    smtp_email: EmailStr
    smtp_password: str = "smtp_password"

    db_dialect: str
    db_username: str
    db_password: str
    db_host: str
    db_port: int
    db_name: str

    secret_key: SecretStr = SecretStr("hack_me")
    is_debug: bool = True

    db_dsn: Union[str, None] = None

    # class Config:
    #     env_file = '.env'
    #     env_file_encoding = 'utf-8'
