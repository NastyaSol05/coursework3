from typing import Any

import requests  # type: ignore

from src.baseapi import BaseAPI


class HhAPI(BaseAPI):
    """
    Класс для работы с API HeadHunter
    Класс BaseAPI является родительским классом
    """

    def __init__(self) -> None:
        self.__url = "https://api.hh.ru/vacancies"
        self.__url_employer = "https://api.hh.ru/employers"
        self.__params = {"text": "", "page": 0, "per_page": 100}

    def get_employer_id(self, query: str) -> Any:
        """Получаем id работников"""
        self.__params["text"] = query
        response = requests.get(url=self.__url_employer, params=self.__params)  # type: ignore

        response.raise_for_status()
        if response.status_code != 200:
            raise "Не удалось подключиться к HeadHunter"  # type: ignore
        return int(response.json()["items"][0]["id"])

    @property
    def url_employer(self) -> str:
        """Ссылка на API работников"""
        return self.__url_employer

    def get_vacancies_by_employer_id(self, query: Any = None) -> Any:
        """Получаем вакансии по id работника"""
        if query:
            self.__params["employer_id"] = query
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
        """Ссылка на API вакансий"""
        return self.__url
