from typing import Any

import psycopg2  # type: ignore

from src.vacancies import Vacancy


class DBManager:
    """Класс для работы с PostgreSQL"""

    def __init__(self, dbname: str, user: str, password: str, host: str, port: str) -> None:
        self.DBNAME = dbname
        self.USER = user
        self.PASSWORD = password
        self.HOST = host
        self.PORT = port
        self.__connection = self.__connect_db("postgres", user, password, host, port)
        self.__cursor = self.__connection.cursor()

    @staticmethod
    def __connect_db(dbname: str, user: str, password: str, host: str, port: str) -> Any:
        """Создаёт подключение к PostgreSQL"""
        return psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

    def create_database(self) -> None:
        """Создает новую БД"""
        self.__connection.autocommit = True
        self.__cursor.execute("SELECT 1 FROM pg_database WHERE datname = 'coursework3'")
        exists = self.__cursor.fetchone()
        if not exists:
            self.__cursor.execute("CREATE DATABASE coursework3")
            self.__connection.commit()
        self.__connection = self.__connect_db(self.DBNAME, "postgres", "anastaA05", "localhost", "5432")
        self.__cursor = self.__connection.cursor()

    def drop_tables(self) -> None:
        """Удаляет все таблицы из БД"""
        self.__cursor.execute("DROP TABLE IF EXISTS vacancies")
        self.__cursor.execute("DROP TABLE IF EXISTS employers")
        self.__connection.commit()

    def create_table_employers(self) -> None:
        """Создает таблицу в БД для работников"""
        self.__cursor.execute(
            """
        CREATE TABLE employers
        (
            id INT PRIMARY KEY,
            employer_name VARCHAR(255) NOT NULL
        );
        """
        )
        self.__connection.commit()

    def create_table_vacancies(self) -> None:
        """Создает таблицу в БД для вакансий"""
        self.__cursor.execute(
            """
                CREATE TABLE vacancies
                (
                    id SERIAL PRIMARY KEY,
                    employer_id INT NOT NULL,
                    vacancies_name VARCHAR(255) NOT NULL,
                    salary INT,
                    link VARCHAR(255) NOT NULL,
                    FOREIGN KEY (employer_id) REFERENCES employers(id)
                );
                """
        )
        self.__connection.commit()

    def fill_table_employer(self, employers: dict) -> None:
        """Заполняет таблицу работников"""
        for employer in employers.items():
            query = "INSERT INTO employers (id, employer_name) VALUES (%s, %s)"
            self.__cursor.execute(query, employer)
        self.__connection.commit()

    def fill_table_vacancies(self, vacancies: list) -> None:
        """Заполняет таблицу вакансий"""
        for vacancy in vacancies:
            insert_data = (
                vacancy.get("name"),
                int(vacancy.get("employer")["id"]),
                Vacancy.parse_salary(vacancy.get("salary")),
                vacancy.get("alternate_url"),
            )
            query = "INSERT INTO vacancies (vacancies_name, employer_id, salary, link) VALUES (%s, %s, %s, %s)"
            self.__cursor.execute(query, insert_data)
        self.__connection.commit()

    def get_companies_and_vacancies_count(self) -> Any:
        """Возвращает список компаний и их количество вакансий"""
        self.__cursor.execute(
            """
            SELECT employers.employer_name, COUNT(vacancies.id) AS vacancies_count FROM employers
            LEFT JOIN vacancies ON employers.id = vacancies.employer_id
            GROUP BY employers.employer_name
            """
        )
        return self.__cursor.fetchall()

    def get_all_vacancies(self) -> Any:
        """Возвращает все вакансии"""
        self.__cursor.execute(
            """
            SELECT employers.employer_name, vacancies_name, salary, link FROM vacancies
            JOIN employers ON employers.id = vacancies.employer_id
            """
        )
        return self.__cursor.fetchall()

    def get_avg_salary(self) -> Any:
        """Возвращает средний доход компаний"""
        self.__cursor.execute(
            """
            SELECT AVG(salary) AS avg_salary FROM vacancies
            """
        )
        return self.__cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self) -> Any:
        """Возвращает вакансии с доходом выше среднего дохода"""
        self.__cursor.execute(
            """
            SELECT * FROM vacancies
            WHERE salary > (SELECT AVG(salary) FROM vacancies)
            """
        )
        return self.__cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword: str) -> Any:
        """Возвращает вакансии с указанным ключевым словом"""
        self.__cursor.execute(f"SELECT * FROM vacancies WHERE vacancies_name LIKE '%{keyword}%'")
        return self.__cursor.fetchall()

    def close_connection(self) -> None:
        """Закрывает подключение к БД"""
        self.__connection.close()

    def close_cursor(self) -> None:
        """Закрывает курсор"""
        self.__cursor.close()
