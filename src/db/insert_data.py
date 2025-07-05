from src.api.hh_api import HHAPI
from config.db_config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT
import psycopg2


def insert_data():
    hh_api = HHAPI()

    employers = [
        {"id": 1740, "name": "Яндекс"},
        {"id": 80, "name": "Альфа-Банк"},
        {"id": 3529, "name": "Сбер"},
        {"id": 84585, "name": "Авито"},
        {"id": 3776, "name": "МТС"},
        {"id": 1122462, "name": "Skyeng"},
        {"id": 633069, "name": "Selectel"},
        {"id": 78638, "name": "Тинькофф"},
        {"id": 4181, "name": "Контур"},
        {"id": 2561, "name": "Газпром нефть"},
    ]

    try:
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cur = conn.cursor()

        for emp in employers:
            print(f"\n📌 Обработка: {emp['name']} (ID: {emp['id']})")

            vacancies = hh_api.get_vacancies_by_employer(emp["id"])
            print(f"🔎 Найдено вакансий: {len(vacancies)}")
            if vacancies:
                print(
                    f"📄 Пример вакансии: {vacancies[0]['title']} | ЗП: {vacancies[0].get('salary_from')}–{vacancies[0].get('salary_to')}"
                )

            cur.execute(
                """
                INSERT INTO employers (employer_id, name, url, description)
                VALUES (%s, %s, %s, %s)
                ON CONFLICT (employer_id) DO NOTHING;
            """,
                (emp["id"], emp["name"], f"https://hh.ru/employers/{emp['id']}", "—"),
            )

            for vac in vacancies:
                cur.execute(
                    """
                    INSERT INTO vacancies (employer_id, title, salary_from, salary_to, url)
                    VALUES (%s, %s, %s, %s, %s);
                """,
                    (
                        vac["employer_id"],
                        vac["title"],
                        vac.get("salary_from"),
                        vac.get("salary_to"),
                        vac["url"],
                    ),
                )

        conn.commit()
        cur.close()
        conn.close()
        print("\n🎉 Все данные успешно загружены в PostgreSQL.")

    except Exception as e:
        print(f"❌ Ошибка при подключении к PostgreSQL: {e}")


if __name__ == "__main__":
    insert_data()
