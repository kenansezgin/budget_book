import sqlite3


def create_db():

    connection = sqlite3.connect("example_database.db")

    cursor = connection.cursor()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        email TEXT UNIQUE NOT NULL
    )
    """
    )

    cursor.execute(
        """
    INSERT INTO users (name, age, email) 
    VALUES ('Raphael', 33, 'raphael@example.com')
    """
    )

    connection.commit()
    connection.close()

    print("SQLite-Datenbank und Tabelle erfolgreich erstellt!")


create_db()
