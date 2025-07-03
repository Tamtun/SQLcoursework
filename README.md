


# HH Coursework: Анализ вакансий с HH API

Учебный проект по работе с PostgreSQL, API hh.ru и анализом вакансий.

## 📂 Структура проекта
```
SQLcoursework/
├── config/
│   └── db_config.py                 # параметры подключения к PostgreSQL
├── src/
│   ├── api/
│   │   ├── __init__.py
│   │   └── hh_api.py               # класс HHAPI — работа с hh.ru
│   ├── db/
│   │   ├── __init__.py
│   │   ├── db_manager.py           # класс DBManager — аналитика и запросы
│   │   ├── init_db.sql             # SQL-скрипт для создания таблиц
│   │   ├── insert_data.py          # загрузка данных из HH API
│   │   └── reset_db.py             # очистка и пересоздание БД
│   └── __init__.py
├── .env                            # переменные окружения
├── .flake8                         # конфиг flake8
├── .gitignore                      # игнорируемые файлы для Git
├── main.py                         
├── poetry.lock                     
├── pyproject.toml                  # конфигурация проекта
├── README.md                       # описание проекта
└── requirements.txt                # список зависимостей

```

## 📦 Возможности проекта

- Получение данных о работодателях и их вакансиях с HH API
- Хранение вакансий и компаний в базе PostgreSQL
- Аналитика: средняя зарплата, фильтрация вакансий выше средней
- Поиск вакансий по ключевому слову
- Интерфейс командной строки

## 🚀 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/tamtun/sqlcoursework.git
cd sqlcoursework
```
2. Создайте и активируйте виртуальное окружение:
```bash
python -m venv venv
```
3. Установите зависимости:
```bash
pip install -r requirements.txt
```

## ⚙️ Настройка базы данных

Проект автоматически создаёт необходимые таблицы при первом запуске `main.py`.

Убедитесь, что в `config/db_config.py` указаны корректные параметры подключения к вашей PostgreSQL:

```python
DB_NAME = 'hh_coursework'
DB_USER = 'ваш_пользователь'
DB_PASSWORD = 'ваш_пароль'
DB_HOST = 'localhost'
DB_PORT = '5432'
```

## 🔁 Сброс и загрузка данных

1. Сброс базы (очистка и пересоздание таблиц):
```bash
python -m src.db.reset_db
```
2. Загрузка вакансий из HH API:
```bash
python -m src.db.insert_data
```

## 🧠 Работа с данными

1. Запуск интерфейса:

```bash
python main.py
```
Доступные действия:
1. Компании и количество вакансий
2. Все вакансии
3. Средняя зарплата
4. Вакансии с ЗП выше средней
5. Поиск по ключевому слову