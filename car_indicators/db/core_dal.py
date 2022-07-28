from typing import AsyncGenerator, Generic, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeMeta


from .base import async_session

Model = TypeVar("Model", bound=DeclarativeMeta)


class CoreDAL:
    @classmethod
    async def get_dal_depends(cls) -> AsyncGenerator["CoreDAL", None]:
        async with async_session() as session:
            yield cls(session)

    def __init__(self, session: AsyncSession) -> None:
        self._session = session
