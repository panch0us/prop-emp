# Модуль для создания базы данных для учета имущества
import sqlite3


def exist_db():
    """Проверяем существует база данных?"""
    pass


def create_db():
    """Создание базы данных"""
    # Создаем файл базы данных. Если он уже создан - подключаемся.
    conn = sqlite3.connect('property-accounting.db')
    # Создаем объект курсора для выполнения запросов
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS employee
    (id INTEGER PRIMARY KEY,
    surname   TEXT    NOT NULL,
    name   TEXT    NOT NULL,
    middle_name   TEXT    NOT NULL)''')

    cur.execute('''CREATE TABLE IF NOT EXISTS property
    (p_id INTEGER PRIMARY KEY,
    title TEXT    NOT NULL,
    type    TEXT    NOT NULL,
    id INT,
    FOREIGN KEY (id) REFERENCES employee (id))''')
    conn.commit()


if __name__ == '__main__':
    if exist_db():
        print('База данных уже создана!')
    else:
        create_db()