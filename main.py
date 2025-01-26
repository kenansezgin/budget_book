import sqlite3
from datetime import datetime


def nutzereingabe():
    produkt_name = input("Gebe den Produktnamen ein: ")
    menge = int(input("Gebe die Menge ein: "))
    preis = float(input("Gebe die Preis ein: "))
    monat = input("Gebe Einkaufsmonat ein oder drücke Enter für heutiges monat: ")
    if not monat:
        monat = datetime.now().strftime("%B")
    return produkt_name, menge, preis, monat


def create_table(connection, cursor):

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS verkaufstabelle (id INTEGER PRIMARY KEY, produkt_name TEXT, menge INTEGER, preis REAL, umsatz REAL, monat TEXT)"
    )

    connection.commit()


def insert_values(connection, cursor, df):
    produkt_name, menge, preis, monat = df

    cursor.execute(
        "INSERT OR IGNORE INTO verkaufstabelle (produkt_name, menge, preis, umsatz, monat) VALUES (?, ?, ?, ?, ?);",
        (produkt_name, menge, preis, menge * preis, monat),
    )

    cursor.execute(
        """
        CREATE VIEW IF NOT EXISTS monatsübersicht AS
        SELECT
            produkt_name,
            SUM(menge) AS verkaufsmenge_gesamt,
            SUM (umsatz) AS umsatz_gesamt,
            monat
        FROM verkaufstabelle
        GROUP BY produkt_name, monat;
        """
    )

    # Änderungen speichern und Verbindung schließen
    connection.commit()


def main():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    df = nutzereingabe()
    create_table(connection, cursor)
    insert_values(connection, cursor, df)
    connection.close()


if __name__ == "__main__":
    main()


#  cursor.execute(
#         "INSERT OR IGNORE INTO monatsübersicht (produkt_name, verkaufsmenge_gesamt, umsatz_gesamt, monat) VALUES (?, ?, ?, ?);",
#         (produkt_name, monat,),
#     )


# Gibt aus ob Änderungen stattgefunden haben
# print(connection.total_changes)


# REATE VIEW view_name AS
# SELECT column1, column2, ...
# FROM table_name
# WHERE condition;

# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;

# SELECT column1, column2, ...
# FROM table_name;

# SELECT SUM(column_name)
# FROM table_name
# WHERE condition;
