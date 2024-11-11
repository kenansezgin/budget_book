# Importiere benötigte Module
import sqlite3  # Zum Arbeiten mit einer SQLite-Datenbank
import glob     # Zum Suchen von Dateien im Dateisystem
import os       # Zum Durchführen von Dateisystemoperationen
from datetime import datetime  # Zum Arbeiten mit Datumsangaben

# Heutiges Datum im Format TT.MM.JJJJ als String
date = datetime.now().strftime("%d.%m.%Y")

# Definiere den Pfad zur SQLite-Datenbank
DB_PATH = "./example.db"

# Prüft, ob die Datenbank vorhanden ist und erstellt sie, falls nicht
def check_db(conn):
    if os.path.exists(DB_PATH):  # Überprüft, ob die Datei für die Datenbank existiert
        create_table(conn)  # Falls die Datenbank existiert, werden die Tabellen erstellt
        conn.close  # Verbindung zur Datenbank wird geschlossen

# Erstellt die Tabellen, wenn sie noch nicht existieren
def create_table(conn):
    cursor = conn.cursor()  # Erstellt einen Cursor zum Ausführen von SQL-Befehlen
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS annual_overview (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            type TEXT NOT NULL,
            financial_item TEXT NOT NULL,
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
        """
    )  # Erstellt die Tabelle annual_overview zur Speicherung der monatlichen Ausgabenübersicht, falls sie nicht existiert
    conn.commit()  # Speichert die Änderungen in der Datenbank

    cursor.execute(
    	"""
        -- Tabelle für tägliche variable Ausgaben
        CREATE TABLE IF NOT EXISTS daily_variable_expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            food NUMERIC,
            groceries NUMERIC,
            transport NUMERIC,
            hygiene NUMERIC,
            books NUMERIC,
            accommodation NUMERIC,
            clothing NUMERIC,
            museum NUMERIC,
            total NUMERIC
        );
        """
    )  # Erstellt die Tabelle daily_variable_expenses zur Speicherung der täglichen Ausgaben, falls sie nicht existiert
    conn.commit()  # Speichert Änderungen in der Datenbank

# Fügt festgelegte Fixkosten in die Tabelle annual_overview ein
def add_values_to_overview(conn):
    cursor = conn.cursor()  # Erstellt einen Cursor zum Ausführen von SQL-Befehlen
    cursor.executemany(
        """
        INSERT INTO annual_overview (type, financial_item, budget, january, february, march, april, may, june, july, august, september, october, november, december, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        [
            ("income", "income", 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 1000, 0),
            ("fix", "rent", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("fix", "electricity", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("fix", "gas", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("fix", "dsl", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("fix", "mobile_data", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("fix", "monthly_ticket", 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 40, 0),
            ("fix", "website_hosting", 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 1.90, 0),
            ("fix", "website", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("fix", "apple_icloud_50GB", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0),
            ("var", "food", 300, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("var", "groceries", 200, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("var", "transport", 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("var", "hygiene", 50, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("var", "books", 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("var", "accommodation", 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("var", "clothing", 15, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            ("var", "museum", 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        ]
    )  # Fügt mehrere vorab festgelegte Datensätze für fixierte und variable Kosten in die Tabelle annual_overview ein
    conn.commit()  # Speichert die Änderungen in der Datenbank

# Sammelt Benutzereingaben für tägliche Ausgaben und speichert diese
def collect_variable_expenses(conn):
    cursor = conn.cursor()  # Erstellt einen Cursor zum Ausführen von SQL-Befehlen

    # Benutzereingaben für verschiedene Ausgabenkategorien
    while True:
        try:
            food = float(input("Heutige Ausgaben für Essen?: "))
            break
        except ValueError:
            print("Das war keine korrekte Angabe. Bitte versuche es erneut.")

    while True:
        try:
            groceries = float(input("Heutige Ausgaben für Lebensmittel?: "))
            break
        except ValueError:
            print("Das war keine korrekte Angabe. Bitte versuche es erneut.")

    while True:
        try:
            transport = float(input("Heutige Ausgaben für Transport?: "))
            break
        except ValueError:
            print("Das war keine korrekte Angabe. Bitte versuche es erneut.")

    # Fügt die Benutzereingaben als heutigen Ausgabeneintrag in die Tabelle daily_variable_expenses ein
    cursor.execute(
        """
        INSERT INTO daily_variable_expenses (date, food, groceries, transport, hygiene, books, accommodation, clothing, museum, total)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
        """,
        [date, food, groceries, transport, 0, 0, 0, 0, 0, 0]
    )
    conn.commit()  # Speichert die Änderungen in der Datenbank
    
# Methode, die die Gesamtsummer der täglichen variablen Ausgaben in der Tabelle annual_overview im entsprechenden Monat einfügt
def variable_expenses_to_annual_overview(conn):
    cursor = conn.cursor()
    
    
	
	
if __name__ == "__main__":
    # Verbindung zur SQLite-Datenbank
    conn = sqlite3.connect(DB_PATH)  # Stellt eine Verbindung zur Datenbank her

    # Überprüfen und Erstellen der Datenbank und Tabellen
    check_db(conn)  # Ruft die Funktion zum Überprüfen und Erstellen der Tabellen auf

    # Festgelegte Fixkosten sammeln und in die Datenbank einfügen
    add_values_to_overview(conn)  # Fügt die vorab festgelegten Fixkosten in die Tabelle annual_overview ein

    # Tägliche Ausgaben sammeln und in die Datenbank einfügen
    collect_variable_expenses(conn)  # Ruft die Funktion zum Sammeln und Einfügen der täglichen Ausgaben auf
    
    variable_expenses_to_annual_overview(conn)  # Überträgt die täglichen Ausgaben in die Monatsübersicht (noch zu implementieren)

    # Verbindung zur Datenbank schließen
    conn.close()  # Schließt die Verbindung zur Datenbank

    print("SQLite-Datenbank und Tabellen erfolgreich erstellt und Daten hinzugefügt!")  # Erfolgsmeldung