import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from config.db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
from src.db.db_manager import DBManager


def create_database_if_not_exists():
    """Создаёт базу данных, если она ещё не существует."""
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur = conn.cursor()

        cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        exists = cur.fetchone()

        if not exists:
            cur.execute(f"CREATE DATABASE {DB_NAME};")
            print(f"✅ База данных '{DB_NAME}' создана.")
        else:
            print(f"ℹ️ База данных '{DB_NAME}' уже существует.")

        cur.close()
        conn.close()
    except Exception as e:
        print(f"❌ Ошибка при создании базы данных: {e}")


def init_db():
    """Создаёт таблицы в базе данных, если они ещё не существуют."""
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS employers (
            employer_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            url TEXT,
            description TEXT
        );
    """
    )

    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS vacancies (
            vacancy_id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            title TEXT NOT NULL,
            salary_from INTEGER,
            salary_to INTEGER,
            url TEXT
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ Таблицы проверены или созданы.")


def main():
    create_database_if_not_exists()
    init_db()

    db = DBManager()

    while True:
        print("\n📊 Выберите действие:")
        print("1 — Компании и количество вакансий")
        print("2 — Все вакансии")
        print("3 — Средняя зарплата")
        print("4 — Вакансии с ЗП выше средней")
        print("5 — Поиск вакансий по ключевому слову")
        print("0 — Выход")

        choice = input("👉 Введите номер действия: ")

        if choice == "1":
            results = db.get_companies_and_vacancies_count()
            print("\n📌 Компании и количество вакансий:")
            for name, count in results:
                print(f"- {name}: {count} вакансий")

        elif choice == "2":
            results = db.get_all_vacancies()
            print("\n📄 Все вакансии:")
            for company, title, salary_from, salary_to, url in results:
                print(f"- {company} | {title} | ЗП: {salary_from}–{salary_to} | {url}")

        elif choice == "3":
            avg = db.get_avg_salary()
            print(f"\n💰 Средняя зарплата: {avg if avg else 'Недостаточно данных'}")

        elif choice == "4":
            results = db.get_vacancies_with_higher_salary()
            print("\n📈 Вакансии с ЗП выше средней:")
            for company, title, salary_from, salary_to, url in results:
                print(f"- {company} | {title} | ЗП: {salary_from}–{salary_to} | {url}")

        elif choice == "5":
            keyword = input("🔎 Введите ключевое слово для поиска: ")
            results = db.get_vacancies_with_keyword(keyword)
            print(f"\n📌 Вакансии, содержащие «{keyword}»:")
            for company, title, salary_from, salary_to, url in results:
                print(f"- {company} | {title} | ЗП: {salary_from}–{salary_to} | {url}")

        elif choice == "0":
            print("👋 До встречи!")
            break

        else:
            print("⚠️ Неверный выбор. Попробуй снова.")

    db.close()


if __name__ == "__main__":
    main()
