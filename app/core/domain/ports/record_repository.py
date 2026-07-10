from abc import ABC, abstractmethod

from app.core.domain.models import CbamRecord


class RecordRepository(ABC):
    @abstractmethod
    async def save(self, record: CbamRecord) -> CbamRecord:
        ...

    @abstractmethod
    async def find_all(
        self, page: int = 1, page_size: int = 20
    ) -> tuple[list[CbamRecord], int]:
        ...

    @abstractmethod
    async def count(self) -> int:
        ...
