from typing import Any


class Vacancy:
    """Класс для работы с вакансиями HeadHunter"""

    __slots__ = ["name", "alternate_url", "salary", "requirement"]

    def __init__(self, name: str, alternate_url: str, salary: Any, requirement: str) -> None:
        self.name = name
        self.alternate_url = alternate_url
        self.salary = Vacancy.__parse_salary(salary)
        if requirement is not None:
            self.requirement = requirement
        else:
            self.requirement = ""

    def __str__(self) -> str:
        return (
            f"Вакансия: {self.name}, зарплата по вакансии: {self.salary}, "
            f"ссылка на вакансию: {self.alternate_url}\n\t{self.requirement}"
        )

    @staticmethod
    def __parse_salary(salary: Any) -> int:
        new_salary = 0
        if isinstance(salary, dict):
            if salary is not None:
                if salary["from"] is not None:
                    new_salary = int(salary["from"])
        elif isinstance(salary, str):
            if salary is not None:
                new_salary = int(salary.replace(" ", "").split("-")[0])
        elif isinstance(salary, int):
            new_salary = salary
        return new_salary

    def __gt__(self, other: Any) -> Any:
        return self.salary > other.salary

    @classmethod
    def cast_to_object_list(cls, hh_vacancies: dict) -> list:
        vacancies = []
        for i in hh_vacancies:
            vacancies.append(cls(i["name"], i["alternate_url"], i["salary"], i["snippet"]["requirement"]))

        return vacancies