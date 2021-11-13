import psycopg2

connection = psycopg2.connect(database="postgres", user="postgres", password="722926", host="127.0.0.1", port=5432)

cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS employee ("
    "id SERIAL NOT NULL PRIMARY KEY, "
    "surname VARCHAR(50) NOT NULL,"
    "name VARCHAR(50) NOT NULL,"
    "middle_name VARCHAR(50) NOT NULL,"
    "birthday DATE"
    ");"
)

connection.commit()
# Fetch all rows from database
#record = cursor.fetchall()

#print("Database:- ", record)