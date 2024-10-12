import sqlite3
from datetime import datetime

# Verbindung zur Datenbank herstellen
connection = sqlite3.connect("example_database.db")
cursor = connection.cursor()

# Aktuelles Datum abrufen
today_date = datetime.now().date()  # Heute als Datum (YYYY-MM-DD)


def create_db():
    # Tabelle erstellen, falls sie nicht existiert
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        food FLOAT,
        groceries FLOAT,
        boldt FLOAT
    )"""
    )


def collect_expenses():
    # Benutzereingaben für Ausgaben
    food_value = float(input("Heutige Ausgaben für Essen?: "))  # Umwandlung in float
    groceries_value = float(
        input("Heutige Ausgaben für Lebensmittel?: ")
    )  # Umwandlung in float
    boldt_value = float(input("Heutige Ausgaben für Boldt?: "))  # Umwandlung in float

    # Einfügen der Daten für das heutige Datum
    cursor.execute(
        """
        INSERT INTO expenses (date, food, groceries, boldt)
        VALUES (?, ?, ?, ?)
        """,
        (today_date, food_value, groceries_value, boldt_value),
    )


# Tabelle erstellen
create_db()
# Ausgaben sammeln
collect_expenses()

# Änderungen speichern und Verbindung schließen
connection.commit()
connection.close()

print("SQLite-Datenbank und Tabelle erfolgreich erstellt und Daten hinzugefügt!")
