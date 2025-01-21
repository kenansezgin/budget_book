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
        "CREATE TABLE IF NOT EXISTS verkaufstabelle (id INTEGER PRIMARY KEY, produkt_name TEXT, menge INTEGER, preis REAL, monat TEXT, umsatz REAL)"
    )

    cursor.execute(
        "CREATE TABLE IF NOT EXISTS monatsübersicht (monat TEXT, gesamtumsatz REAL, gesamt_verkaufsmenge INTEGER)"
    )
    connection.commit()




def insert_values(connection, cursor, df):
    produkt_name, menge, preis, monat = df

    cursor.execute(
        "INSERT OR IGNORE INTO verkaufstabelle (produkt_name, menge, preis, umsatz) VALUES (?, ?, ?, ?, ?);",
        (produkt_name, menge, preis, monat, menge * preis),
    )

    cursor.execute(
        "INSERT INTO monatsübersicht (monat) VALUES (?);",
        (monat,),
    )


    cursor.execute(
        "UPDATE monatsübersicht SET gesamtumsatz = (SELECT SUM(umsatz) FROM verkaufstabelle) WHERE monat = 'January';
    )

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



# UPDATE table_name
# SET column1 = value1, column2 = value2, ...
# WHERE condition;

# SELECT column1, column2, ...
# FROM table_name;

# SELECT SUM(column_name)
# FROM table_name
# WHERE condition; 
