from typing import Any

import requests

from src.baseapi import BaseAPI


class HhAPI(BaseAPI):
    """
    Класс для работы с API HeadHunter
    Класс BaseAPI является родительским классом
    """

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def get_vacancies(self, query: Any = None) -> Any:
        if query:
            self.__params["text"] = query
            response = requests.get(url=self.__url, params=self.__params)  # type: ignore
        else:
            response = requests.get(self.__url)

        response.raise_for_status()
        if response.status_code != 200:
            raise "Не удалось подключиться к HeadHunter"  # type: ignore
        vacancies = response.json()["items"]
        return vacancies

    @property
    def url(self) -> str:
        return self.__url