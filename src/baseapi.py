from abc import ABC, abstractmethod
from typing import Any


class BaseAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_employer_id(self, query: str) -> Any:
        pass

    @abstractmethod
    def get_vacancies_by_employer_id(self, query: Any) -> None:
        pass
