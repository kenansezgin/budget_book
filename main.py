import sqlite3
from datetime import datetime, date

# Adapter: datetime.date -> str (für Speicherung im deutschen Format TT.MM.JJJJ)
sqlite3.register_adapter(date, lambda d: d.strftime("%d.%m.%Y"))
sqlite3.register_adapter(datetime, lambda d: d.strftime("%d.%m.%Y"))

# Konverter: str -> datetime.date (für Abruf im deutschen Format TT.MM.JJJJ)
sqlite3.register_converter(
    "DATE", lambda s: datetime.strptime(s.decode(), "%d.%m.%Y").date()
)

# Verbindung zur Datenbank herstellen mit aktivierten Konvertern
connection = sqlite3.connect(
    "example_database.db", detect_types=sqlite3.PARSE_DECLTYPES
)
cursor = connection.cursor()

# Aktuelles Datum abrufen
today_date = datetime.now().date()  # Heute als Datum (TT.MM.JJJJ)


def create_db():
    # Tabelle für fix costs erstellen
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS fix_costs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        rent FLOAT,
        electricity FLOAT,
        gas FLOAT,
        dsl FLOAT,
        mobile_data FLOAT,
        monthly_ticket FLOAT,
        website_hosting FLOAT,
        website FLOAT,
        apple_icloud_50GB FLOAT
        )"""
    )

    # Tabelle für Ausgaben erstellen
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        food FLOAT,
        groceries FLOAT,
        boldt FLOAT,
        hygiene FLOAT,
        books FLOAT,
        museum FLOAT
    )"""
    )


def add_fix_costs():
    cursor.execute(
        """
        INSERT INTO fix_costs (rent, electricity, gas, dsl, mobile_data, monthly_ticket, website_hosting, website, apple_icloud_50GB)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (0.0, 0.0, 0.0, 0.0, 40.0, 1.90, 0.0, 1.0, 0.0),
    )


def collect_expenses():
    # Benutzereingaben für Ausgaben
    food_value = float(input("Heutige Ausgaben für Essen?: "))
    groceries_value = float(input("Heutige Ausgaben für Lebensmittel?: "))
    boldt_value = float(input("Heutige Ausgaben für Boldt?: "))

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

# Fix kosten sammeln
add_fix_costs()

# Ausgaben sammeln
collect_expenses()

# Änderungen speichern und Verbindung schließen
connection.commit()
connection.close()

print("SQLite-Datenbank und Tabelle erfolgreich erstellt und Daten hinzugefügt!")
