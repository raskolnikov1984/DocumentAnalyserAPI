from abc import ABC, abstractmethod


class RecordValidator(ABC):
    @abstractmethod
    async def validate(
        self, row: dict, row_num: int
    ) -> list[dict]:
        ...
