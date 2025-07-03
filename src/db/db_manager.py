import psycopg2
from config.db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        self.cur = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """Получает список компаний и количество их вакансий."""
        self.cur.execute(
            """
            SELECT e.name, COUNT(v.id)
            FROM employers e
            LEFT JOIN vacancies v ON e.employer_id = v.employer_id
            GROUP BY e.name
            ORDER BY COUNT(v.id) DESC;
        """
        )
        return self.cur.fetchall()

    def get_all_vacancies(self):
        """Получает все вакансии с полной информацией."""
        self.cur.execute(
            """
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            ORDER BY v.salary_from DESC NULLS LAST;
        """
        )
        return self.cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по всем вакансиям."""
        self.cur.execute(
            """
            SELECT ROUND(AVG(
                (COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2.0
            )) AS avg_salary
            FROM vacancies v
            WHERE salary_from IS NOT NULL OR salary_to IS NOT NULL;
        """
        )
        result = self.cur.fetchone()
        return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """Получает вакансии с ЗП выше средней."""
        avg_salary = self.get_avg_salary()
        self.cur.execute(
            """
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE ((COALESCE(v.salary_from, 0) + COALESCE(v.salary_to, 0)) / 2.0) > %s;
        """,
            (avg_salary,),
        )
        return self.cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает вакансии, содержащие ключевое слово в названии."""
        self.cur.execute(
            """
            SELECT e.name, v.title, v.salary_from, v.salary_to, v.url
            FROM vacancies v
            JOIN employers e ON v.employer_id = e.employer_id
            WHERE LOWER(v.title) LIKE %s;
        """,
            (f"%{keyword.lower()}%",),
        )
        return self.cur.fetchall()

    def close(self):
        """Закрывает подключение к базе."""
        self.cur.close()
        self.conn.close()
