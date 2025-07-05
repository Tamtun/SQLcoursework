CREATE TABLE employers (
    employer_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    url TEXT,
    description TEXT
);

CREATE TABLE vacancies (
    vacancy_id SERIAL PRIMARY KEY,
    employer_id INTEGER REFERENCES employers(employer_id),
    title TEXT NOT NULL,
    salary_from INTEGER,
    salary_to INTEGER,
    url TEXT
);
