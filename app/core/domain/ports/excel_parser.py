from abc import ABC, abstractmethod


class ExcelParser(ABC):
    @abstractmethod
    async def parse(self, file_path: str) -> list[dict]:
        ...
