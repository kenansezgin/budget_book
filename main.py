import sqlite3
from datetime import datetime

datum = datetime.now().strftime("%d-%m-%Y")
print(datetime.now().strftime("%B"))
print(f"{datum.strftime("%B")})


def nutzereingabe():
    produkt_name = input("Gebe den Produktnamen ein: ")
    menge = int(input("Gebe die Menge ein: "))
    preis = float(input("Gebe den Preis ein: "))

    return produkt_name, menge, preis


def create_table(connection, cursor):

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS verkaufstabelle (
            id INTEGER PRIMARY KEY,
            datum TEXT,
            produkt_name TEXT,
            menge INTEGER,
            preis REAL,
            umsatz REAL
        )  
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS jahresübersicht (
            id INTEGER PRIMARY KEY,
            produkt_name TEXT,
            budget REAL,
            january REAL DEFAULT 0,
            february REAL DEFAULT 0,
            march REAL DEFAULT 0,
            april REAL DEFAULT 0,
            may REAL DEFAULT 0,
            june REAL DEFAULT 0,
            july REAL DEFAULT 0,
            august REAL DEFAULT 0,
            september REAL DEFAULT 0,
            october REAL DEFAULT 0,
            november REAL DEFAULT 0,
            december REAL DEFAULT 0
        );
        """
    )
    connection.commit()


def insert_values(connection, cursor, df):
    produkt_name, menge, preis = df

    cursor.execute(
        """
        INSERT OR IGNORE INTO verkaufstabelle (
            datum,
            produkt_name,
            menge, 
            preis,
            umsatz
        ) 
        VALUES (?, ?, ?, ?, ?);
        """,
        (datum, produkt_name, menge, preis, menge * preis),
    )

    # Änderungen speichern und Verbindung schließen
    connection.commit()


def monthly_results(connection, cursor):
    cursor.execute(
        """
        SELECT SUM(umsatz)
        FROM verkaufstabelle
        WHERE datum =  strftime("%B")"""
    )


def main():
    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    df = nutzereingabe()
    create_table(connection, cursor)
    insert_values(connection, cursor, df)
    monthly_results(connection.cursor)
    connection.close()


if __name__ == "__main__":
    main()


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
