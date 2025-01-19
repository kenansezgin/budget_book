# Zeile 19 und 23 überlege dir neue Spalten und entscheide was die Spalten sein sollen und was die Zeilen sein sollen

import sqlite3
from datetime import datetime


def nutzereingabe():
    produkt_name = input(f"Gebe den Produktnamen ein: ")
    menge = int(input(f"Gebe die Menge ein: "))
    preis = float(input(f"Gebe die Preis ein: "))
    monat = str(input(f"Gebe Einkaufsmonat ein oder drücke Enter für heutiges monat: "))
    if not monat:
        monat = datetime.now().strftime("%B")
    return produkt_name, menge, preis, monat


def create_table():
    connection = sqlite3.connect("alternative_1.db")
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS verkaufstabelle (id INTEGER PRIMARY KEY, produkt_name TEXT, menge INTEGER, preis REAL, monat TEXT, umsatz REAL)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monatsübersicht (monat TEXT, gesamtumsatz REAL, gesamt_verkaufsmenge INTEGER)"
    )
    connection.commit()
    connection.close()


def insert_values(df):
    produkt_name, menge, preis, monat = df
    connection = sqlite3.connect("alternative_1.db")
    cursor = connection.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO verkaufstabelle (produkt_name, menge, preis, umsatz) VALUES (?, ?, ?, ?, ?);",
        (produkt_name, menge, preis, monat, menge * preis),
    )

    cursor.execute(
        "INSERT INTO monatsübersicht (monat) VALUES ('?');",
        (monat),
    )

    # Änderungen speichern und Verbindung schließen
    connection.commit()
    connection.close()


def main():
    df = nutzereingabe()
    create_table()
    insert_values(df)


if __name__ == "__main__":
    main()

# Gibt aus ob Änderungen stattgefunden haben
# print(connection.total_changes)
