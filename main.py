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


df = nutzereingabe()

print(df)

# produkt_name = input("Gebe das Produkt ein welches in die Tabelle eingetragen werden soll: ")

# Gibt uns ein Objekt "connection" zurück damit wir mit der Datenbank interaggieren können
connection = sqlite3.connect("products.db")

# Gibt aus ob Änderungen stattgefunden haben
print(connection.total_changes)

# Erlaubt uns SQL Befehle an die SQL Datenbank zu senden
cursor = connection.cursor()

cursor.execute(
    "CREATE TABLE IF NOT EXISTS verkaufstabelle (id INTEGER PRIMARY KEY, produkt_name TEXT, menge INTEGER, preis REAL, umsatz REAL)"
)

cursor.execute(
    "CREATE TABLE IF NOT EXISTS monatsübersicht (monat TEXT, gesamtumsatz REAL, gesamt_verkaufsmenge INTEGER)"
)

cursor.execute(
    """
INSERT OR IGNORE INTO verkaufstabelle (produkt_name, menge, preis, umsatz)
VALUES ('shorts', 12, 9.99, 6.99);
"""
)

cursor.execute(
    """
INSERT INTO monatsübersicht (monat)
VALUES ('januar');
"""
)

# Änderungen speichern und Verbindung schließen
connection.commit()
connection.close()


"""
# Name der SQLite-Datenbank
DATABASE_NAME = 'expenses.db'

# Verbindung zur SQLite-Datenbank herstellen
connection = sqlite3.connect(DATABASE_NAME)
cursor = connection.cursor()

    # Tabellen erstellen
create_tables(cursor)
"""
