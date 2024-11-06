import sqlite3

# Erlaubt globale Variablen
import glob

# Erlaubt Dateisystemdaten
import os
from datetime import datetime, date

# Konstante um den Datenbankpfad festzulegen
DB_PATH = "./example.db"


def check_db(conn):
    # does the path exists
    if os.path.exists(DB_PATH):
        # Connection of SQLite DB is now inside the variable conn

        create_table(conn)
        conn.close


def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS fix_costs (
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
        );
    """
    )
    conn.commit()

    cursor.execute(
        """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date DATE NOT NULL,
        food FLOAT,
        groceries FLOAT,
        boldt FLOAT,
        hygiene FLOAT,
        books FLOAT,
        museum FLOAT
        );
    """
    )
    conn.commit()


# Adapter: datetime.date -> str (für Speicherung im deutschen Format TT.MM.JJJJ)
sqlite3.register_adapter(date, lambda d: d.strftime("%d.%m.%Y"))
sqlite3.register_adapter(datetime, lambda d: d.strftime("%d.%m.%Y"))

# Konverter: str -> datetime.date (für Abruf im deutschen Format TT.MM.JJJJ)
sqlite3.register_converter(
    "DATE", lambda s: datetime.strptime(s.decode(), "%d.%m.%Y").date()
)


# Aktuelles Datum abrufen
today_date = datetime.now().date()  # Heute als Datum (TT.MM.JJJJ)


def add_fix_costs(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO fix_costs (rent, electricity, gas, dsl, mobile_data, monthly_ticket, website_hosting, website, apple_icloud_50GB)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (0.0, 0.0, 0.0, 0.0, 40.0, 1.90, 0.0, 1.0, 0.0),
    )


def collect_expenses(conn):

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


if __name__ == "__main__":

    conn = sqlite3.connect(DB_PATH)
    create_table(conn)
""""
    check_db(conn)
  
    # Fix kosten sammeln
    add_fix_costs(conn)

    # Ausgaben sammeln
    collect_expenses()

    # Änderungen speichern und Verbindung schließen
    # connection.commit()
    conn.close(conn)

    print("SQLite-Datenbank und Tabelle erfolgreich erstellt und Daten hinzugefügt!")


# library streamlit: um eine webseite zu erstellen und datenbanken zu füllen
"""
