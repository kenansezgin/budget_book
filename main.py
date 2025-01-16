import sqlite3
from datetime import datetime


def nutzereingabe():
    produkt_name = input(f"Gebe den Produktnamen ein: ")
    menge = int(input(f"Gebe die Menge ein: "))
    preis = float(input(f"Gebe die Preis ein: "))
    datum = str(input(f"Gebe Einkaufsmonat ein oder drücke Enter für heutiges Datum: "))
    if not datum:
        datum = datetime.now().strftime("%B")
    return produkt_name, menge, preis, datum


def create_db():
    # Gibt uns ein Objekt "connection" zurück damit wir mit der Datenbank interaggieren können
    connection = sqlite3.connect("products.db")

    # Erlaubt uns SQL Befehle an die SQL Datenbank zu senden
    cursor = connection.cursor()
    return connection, cursor


def create_table(connection, cursor):
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS verkaufstabelle (id INTEGER PRIMARY KEY, produkt_name TEXT, menge INTEGER, preis REAL, umsatz REAL)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monatsübersicht (monat TEXT, gesamtumsatz REAL, gesamt_verkaufsmenge INTEGER)"
    )


def insert_values(connection, cursor, df):

    cursor.execute(
        "INSERT OR IGNORE INTO verkaufstabelle (produkt_name, menge, preis, umsatz) VALUES ('shorts', 12, 9.99, 6.99);"
    )

    cursor.execute("INSERT INTO monatsübersicht (monat) VALUES ('januar');")

    # Änderungen speichern und Verbindung schließen
    connection.commit()
    connection.close()


def main():
    df = nutzereingabe()
    x = create_db()
    create_table(x[0], x[1])
    insert_values(x[0], x[1], df)


if __name__ == "__main__":
    main()


"""
# Name der SQLite-Datenbank
DATABASE_NAME = 'expenses.db'

# Verbindung zur SQLite-Datenbank herstellen
connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

    # Tabellen erstellen
create_tables(cursor)
"""

# Gibt aus ob Änderungen stattgefunden haben
# print(connection.total_changes)
