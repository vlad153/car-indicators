from typing import Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

from .base import Base
from .base import async_session

Model = TypeVar("Model", bound=Base)

class CoreDAL(Generic[Model]):

    @classmethod
    async def get_dal_depends(cls):
        async with async_session() as session:
            cls(session)
    
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    