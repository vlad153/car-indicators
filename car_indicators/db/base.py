from hypothesis import settings
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine.url import URL

from ..config import Settings

Base = declarative_base()

_settings = Settings()
print(_settings.db_username)
print(_settings.db_dialect)
_url = URL(
    _settings.db_dialect, 
    username=_settings.db_username, 
    password=_settings.db_password, 
    host=_settings.db_host, 
    port=_settings.db_port, 
    database=_settings.db_name
) 

print(_url)

async_engine = create_async_engine(_url, future=True, echo=False)

async_session = sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession) 

