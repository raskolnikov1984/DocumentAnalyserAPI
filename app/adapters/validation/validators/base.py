from abc import ABC, abstractmethod


class BaseValidator(ABC):
    @abstractmethod
    async def validate(self, row: dict, row_num: int) -> list[dict]:
        ...
