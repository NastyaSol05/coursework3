import os
from typing import Any

from dotenv import load_dotenv

from src.DBManager import DBManager
from src.hhapi import HhAPI

load_dotenv()
DBNAME = os.getenv("dbname")
USER = os.getenv("user")
PASSWORD = os.getenv("password")
HOST = os.getenv("host")
PORT = os.getenv("port")
company_name = [
    "Яндекс Команда для бизнеса",
    "Skyeng",
    "Т-Банк",
    "РОСЭЛТОРГ",
    "Сбер для экспертов",
    "Альфа-Банк",
    "Demis Group",
    "ПАО ВТБ, Подразделения Поддержки и Контроля",
    "Кейсистемс",
    "ООО Команда Ф5",
]
employer_ids = []
vacancies = []

hh_api = HhAPI()
for i in company_name:
    employer_ids.append(hh_api.get_employer_id(i))

hh_api = HhAPI()
for i in employer_ids:
    for j in hh_api.get_vacancies_by_employer_id(i):
        vacancies.append(j)

employers = dict(zip(employer_ids, company_name))


def main() -> Any:
    db = DBManager(DBNAME, USER, PASSWORD, HOST, PORT)  # type: ignore
    db.create_database()
    db.drop_tables()

    db.create_table_employers()
    db.fill_table_employer(employers)

    db.create_table_vacancies()
    db.fill_table_vacancies(vacancies)

    print(
        "Выберите действие: \n"
        "1. Получить список всех компаний и количество вакансий у каждой компании\n"
        "2. Получить список всех вакансий с указанием названия компании, "
        "названия вакансии и зарплаты и ссылки на вакансию\n"
        "3. Получить среднюю зарплату по вакансиям\n"
        "4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям\n"
        "5. Получить список всех вакансий в названии которого содержится переданное вами слово\n"
    )
    user_input = int(input("Ваш выбор - "))

    if user_input == 1:
        print(db.get_companies_and_vacancies_count())
    elif user_input == 2:
        print(db.get_all_vacancies())
    elif user_input == 3:
        print(db.get_avg_salary())
    elif user_input == 4:
        print(db.get_vacancies_with_higher_salary())
    elif user_input == 5:
        keyword = input("Введите слово: ")
        print(db.get_vacancies_with_keyword(keyword))

    db.close_cursor()
    db.close_connection()


if __name__ == "__main__":
    main()
