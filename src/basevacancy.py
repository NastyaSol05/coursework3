from abc import ABC, abstractmethod
from typing import Any


class BaseVacancy(ABC):
    """Abstract base class for vacancy operations."""

    @classmethod
    @abstractmethod
    def add_vacancy(cls, *args: Any, **kwargs: Any) -> Any:
        pass

    @classmethod
    @abstractmethod
    def get_vacancy(cls, *args: Any, **kwargs: Any) -> Any:
        pass

    @classmethod
    @abstractmethod
    def save_vacancy(cls, *args: Any, **kwargs: Any) -> Any:
        pass

    @classmethod
    @abstractmethod
    def delete_vacancy(cls, *args: Any, **kwargs: Any) -> Any:
        pass
