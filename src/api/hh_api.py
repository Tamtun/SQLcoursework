import requests


class HHAPI:
    """Класс для работы с API hh.ru."""

    BASE_URL = "https://api.hh.ru"

    def get_employer_by_name(self, name: str) -> dict | None:
        url = f"{self.BASE_URL}/employers"
        params = {"text": name}
        response = requests.get(url, params=params)

        if response.status_code != 200:
            print(f"⚠️ Ошибка запроса работодателя '{name}': {response.status_code}")
            return None

        data = response.json()
        if data.get("items"):
            employer = data["items"][0]
            return {
                "id": employer["id"],
                "name": employer["name"],
                "url": employer.get("alternate_url"),
                "description": employer.get("description", "—"),
            }
        else:
            print(f"⚠️ Работодатель '{name}' не найден")
            return None

    def get_vacancies_by_employer(self, employer_id: int, per_page: int = 100) -> list:
        import time

        url = f"{self.BASE_URL}/vacancies"
        params = {
            "employer_id": employer_id,
            "per_page": per_page,
            "only_with_salary": True,
        }

        response = requests.get(url, params=params)
        if response.status_code != 200:
            print(
                f"❌ Ошибка получения вакансий: {response.status_code} для employer_id={employer_id}"
            )
            return []

        data = response.json()
        items = data.get("items", [])
        if not items:
            print(f"⚠️ Вакансии не найдены для employer_id={employer_id}")
            return []

        vacancies = []
        for item in items:
            salary = item.get("salary") or {}
            if salary.get("from") or salary.get("to"):
                vacancies.append(
                    {
                        "employer_id": employer_id,
                        "title": item.get("name"),
                        "salary_from": salary.get("from"),
                        "salary_to": salary.get("to"),
                        "url": item.get("alternate_url"),
                    }
                )

        print(f"📥 Денежных вакансий: {len(vacancies)} для employer_id={employer_id}")
        time.sleep(0.5)
        return vacancies
