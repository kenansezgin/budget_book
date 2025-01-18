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


def create_table(connection, cursor):

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS verkaufstabelle (id INTEGER PRIMARY KEY, produkt_name TEXT, menge INTEGER, preis REAL, umsatz REAL)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monatsübersicht (monat TEXT, gesamtumsatz REAL, gesamt_verkaufsmenge INTEGER)"
    )
    connection.commit()


def insert_values(connection, cursor, df):
    produkt_name, menge, preis, datum = df

    cursor.execute(
        "INSERT OR IGNORE INTO verkaufstabelle (produkt_name, menge, preis, umsatz) VALUES (?, ?, ?, ?);",
        (produkt_name, menge, preis, datum),
    )

    cursor.execute("INSERT INTO monatsübersicht (monat) VALUES ('januar');")

    # Änderungen speichern und Verbindung schließen
    connection.commit()


def main():
    connection = sqlite3.connect("alternative_2.db")
    cursor = connection.cursor()

    df = nutzereingabe()
    create_table(connection, cursor)
    insert_values(connection, cursor, df)
    connection.close()


if __name__ == "__main__":
    main()

# Gibt aus ob Änderungen stattgefunden haben
# print(connection.total_changes)