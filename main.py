import sqlite3
import os
from datetime import datetime, date

# Adapter für das deutsche Datumsformat TT.MM.JJJJ
# Adapter for the German date format DD.MM.YYYY
sqlite3.register_adapter(date, lambda d: d.strftime("%d.%m.%Y"))
sqlite3.register_adapter(datetime, lambda d: d.strftime("%d.%m.%Y"))

# Konverter: String -> Datum im deutschen Format
# Converter: String -> Date in German format
sqlite3.register_converter(
    "DATE", lambda s: datetime.strptime(s.decode(), "%d.%m.%Y").date()
)

# Pfad zur SQLite-Datenbank
# Path to the SQLite database
DB_PATH = "./example_database_2.db"

# Aktuelles Datum im deutschen Format abrufen
# Retrieve today's date in German format
today_date = datetime.now().date()


def check_database():
    """
    Überprüft, ob die Datenbank existiert. Falls nicht, wird eine neue Datenbank erstellt.
    Checks if the database exists. If not, a new database is created.
    """
    if not os.path.exists(DB_PATH):
        print("Datenbank existiert nicht, erstelle neue Datenbank.")
        conn = sqlite3.connect(DB_PATH)  # Verbindung zur SQLite-Datenbank herstellen
        create_tables(conn)  # Tabellen erstellen (falls sie nicht existieren)
        conn.close()  # Verbindung schließen
    else:
        print("Datenbank existiert bereits.")


def create_tables(conn):
    """
    Erstellt die Tabellen 'fixed_costs' und 'variable_costs', falls sie noch nicht existieren.
    Creates the 'fixed_costs' and 'variable_costs' tables if they don't exist yet.
    """
    cursor = conn.cursor()

    # Tabelle für fixe Kosten erstellen
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS fixed_costs (
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
    print("Tabelle 'fixed_costs' erstellt oder existiert bereits.")

    # Tabelle für variable Kosten mit Standardwerten erstellen
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS variable_costs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE NOT NULL,
            food FLOAT DEFAULT 0.0,
            groceries FLOAT DEFAULT 0.0,
            boldt FLOAT DEFAULT 0.0,
            clothing FLOAT DEFAULT 0.0,
            leisure FLOAT DEFAULT 0.0,
            hygiene_medicine FLOAT DEFAULT 0.0,
            books FLOAT DEFAULT 0.0,
            other FLOAT DEFAULT 0.0
        );
        """
    )
    print("Tabelle 'variable_costs' erstellt oder existiert bereits.")

    conn.commit()  # Änderungen in der Datenbank speichern


def add_fixed_costs(conn):
    """
    Fügt die fixen Kosten mit Standardwerten in die Tabelle 'fixed_costs' ein.
    Inserts fixed costs with default values into the 'fixed_costs' table.
    """
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO fixed_costs (rent, electricity, gas, dsl, mobile_data, monthly_ticket, website_hosting, website, apple_icloud_50GB)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (0.0, 0.0, 0.0, 0.0, 40.0, 1.90, 0.0, 1.0, 0.0),
    )
    conn.commit()  # Änderungen in der Datenbank speichern
    print("Fixkosten wurden erfolgreich in die Datenbank eingefügt.")


def collect_variable_costs(conn):
    """
    Fragt den Benutzer nach den ausgewählten täglichen variablen Kosten und speichert diese in der Tabelle 'variable_costs'.
    Prompts the user for the selected daily variable costs and saves them into the 'variable_costs' table.
    """
    cursor = conn.cursor()

    food_value = float(
        input("Heutige Ausgaben für Essen?: ")
    )  # Ausgabe für Essen / Food
    groceries_value = float(
        input("Heutige Ausgaben für Lebensmittel?: ")
    )  # Ausgabe für Lebensmittel / Groceries
    boldt_value = float(
        input("Heutige Ausgaben für Boldt?: ")
    )  # Ausgabe für Boldt / Boldt

    cursor.execute(
        """
        INSERT INTO variable_costs (date, food, groceries, boldt)
        VALUES (?, ?, ?, ?)
        """,
        (today_date, food_value, groceries_value, boldt_value),
    )
    conn.commit()
    print("Variable Kosten wurden erfolgreich in die Datenbank eingefügt.")


if __name__ == "__main__":
    """
    Hauptprogramm: Überprüft die Datenbank, fügt fixe Kosten hinzu und sammelt die ausgewählten variablen Kosten.
    Main program: Checks the database, adds fixed costs, and collects the selected variable costs.
    """
    # Verbindung zur SQLite-Datenbank herstellen
    conn = sqlite3.connect(DB_PATH, detect_types=sqlite3.PARSE_DECLTYPES)

    check_database()  # Überprüfen der Datenbank und Tabellen erstellen
    create_tables(conn)  # Sicherstellen, dass die Tabellen existieren
    add_fixed_costs(conn)  # Fixkosten hinzufügen
    collect_variable_costs(conn)  # Variable Kosten sammeln
    conn.close()  # Verbindung zur Datenbank schließen

    print("Daten erfolgreich hinzugefügt!")  # Erfolgsmeldung
