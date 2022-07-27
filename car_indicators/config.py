from typing import Optional, Union
from pydantic import AnyUrl, BaseSettings, PostgresDsn, SecretStr, EmailStr

class SQLiteDsn(AnyUrl):
    allowed_schemes = {
        'sqlite',
        'sqlite+aiosqlite',
    }
    user_required = False

class Settings(BaseSettings):
    
    host = '127.0.0.1'
    port = 5000

    smtp_address: str = 'localhost'
    smtp_port: int = 2500
    smtp_email: EmailStr
    smtp_password: str = 'smtp_password'


    db_dialect = ''
    db_username = ''
    db_password = ''
    db_host = ''
    db_port = ''
    db_name = ''

    secret_key: SecretStr = 'hack_me'
    is_debug = True

    db_dsn: Union[str, None] = None

    # class Config:
    #     env_file = '.env'
    #     env_file_encoding = 'utf-8'
