# Importiere benötigte Module
import sqlite3  # Datenbank
import glob     # Für Dateisuche im Dateisystem
import os       # Für Dateisystemoperationen
from datetime import datetime, date  # Für Datumsmanipulation


# Definiere den Pfad zur SQLite-Datenbank
DB_PATH = "./example.db"

# Prüft, ob die Datenbank vorhanden ist und erstellt sie, falls nicht
def check_db(conn):
    if os.path.exists(DB_PATH):
        # Verbindet sich mit der SQLite-Datenbank
        create_table(conn)
        conn.close

# Erstellt die Tabellen, wenn sie noch nicht existieren
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS annual_overview (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            budget NUMERIC,
            january NUMERIC,
            february NUMERIC,
            march NUMERIC,
            april NUMERIC,
            may NUMERIC,
            june NUMERIC,
            july NUMERIC,
            august NUMERIC,
            september NUMERIC,
            october NUMERIC,
            november NUMERIC,
            december NUMERIC,
            total NUMERIC
        );

        -- Tabellen für alle Monate
        CREATE TABLE IF NOT EXISTS january (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS february (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS march (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS april (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS may (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS june (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS july (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS august (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS september (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS october (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS november (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        
        CREATE TABLE IF NOT EXISTS december (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            boldt NUMERIC,
            groceries NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            museum NUMERIC
        );
        """
    )
    conn.commit()  # Speichert Änderungen in der Datenbank

# Adapter: datetime.date -> str (für Speicherung im deutschen Format TT.MM.JJJJ)
sqlite3.register_adapter(date, lambda d: d.strftime("%d.%m.%Y"))
sqlite3.register_adapter(datetime, lambda d: d.strftime("%d.%m.%Y"))

# Konverter: str -> datetime.date (für Abruf im deutschen Format TT.MM.JJJJ)
sqlite3.register_converter(
    "DATE", lambda s: datetime.strptime(s.decode(), "%d.%m.%Y").date()
)

# Holt das heutige Datum im Format TT.MM.JJJJ
today_date = datetime.now().date()

# Fügt festgelegte Fixkosten in die Tabelle ein
def add_fix_values(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO annual_overview (description, budget, january, february, march, april, may, june, july, august, september, november, december, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ("income", 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000),
            ("rent", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("electricity", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("gas", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("dsl", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("mobile_data", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("monthly_ticket", 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40),
            ("website_hosting", 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90),
            ("website", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("apple_icloud_50GB", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
        ],
    )
    conn.commit()  # Speichert Änderungen in der Datenbank

# Sammelt Benutzereingaben für tägliche Ausgaben und speichert diese
def collect_expenses(conn):
    cursor = conn.cursor()

    # Benutzereingaben für verschiedene Ausgabenkategorien
    while True:
        try:
            food_value = float(input("Heutige Ausgaben für Essen?: "))
            break
        except ValueError:
            print("Das war keine korrekte Angabe. Bitte versuche es erneut.")

    while True:
        try:
            groceries_value = float(input("Heutige Ausgaben für Lebensmittel?: "))
            break
        except ValueError:
            print("Das war keine korrekte Angabe. Bitte versuche es erneut.")

    while True:
        try:
            boldt_value = float(input("Heutige Ausgaben für Boldt?: "))
            break
        except ValueError:
            print("Das war keine korrekte Angabe. Bitte versuche es erneut.")

    # Einfügen der heutigen Ausgaben in die Tabelle
    # Programm muss erkennen welches Datum wir heute haben und es in die richtige Tabelle mit dem richtigen Monat in die Zeile mit dem richtigen Monat hineinsetzen.
    # das benötige ich print(  today_date.month) und ich benötige ich vermutlich eine dictionary
    cursor.execute(
        """
        INSERT INTO variable_costs (date, description, budget, january, february, march, april, may, june, july, august, september, october, november, december)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [today_date, "food", food_value, groceries_value, boldt_value]

        
      
    )
    conn.commit()

if __name__ == "__main__":
    # Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(DB_PATH)

    # Überprüfen und Erstellen der Datenbank und Tabellen
    check_db(conn)

    # Festgelegte Fixkosten sammeln und in die Datenbank einfügen
    add_fix_values(conn)

    # Tägliche Ausgaben sammeln und in die Datenbank einfügen
    collect_expenses(conn)

    # Verbindung zur Datenbank schließen
    conn.close()

    print("SQLite-Datenbank und Tabellen erfolgreich erstellt und Daten hinzugefügt!")