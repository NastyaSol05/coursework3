from typing import Any


class Vacancy:
    """Класс для работы с вакансиями HeadHunter"""

    @staticmethod
    def parse_salary(salary: Any) -> Any:
        new_salary = None
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
