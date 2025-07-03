import psycopg2
from config.db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def reset_database():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cur = conn.cursor()

    cur.execute("DROP TABLE IF EXISTS vacancies;")
    cur.execute("DROP TABLE IF EXISTS employers;")

    cur.execute(
        """
        CREATE TABLE employers (
            employer_id INTEGER PRIMARY KEY,
            name TEXT,
            url TEXT,
            description TEXT
        );
    """
    )
    cur.execute(
        """
        CREATE TABLE vacancies (
            id SERIAL PRIMARY KEY,
            employer_id INTEGER REFERENCES employers(employer_id),
            title TEXT,
            salary_from INTEGER,
            salary_to INTEGER,
            url TEXT
        );
    """
    )

    conn.commit()
    cur.close()
    conn.close()
    print("✅ База данных успешно сброшена и пересоздана.")


if __name__ == "__main__":
    reset_database()
