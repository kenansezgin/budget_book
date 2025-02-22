import sqlite3
import pandas as pd
from datetime import datetime

# test
# 📌 Monats-Mapping für die Spaltennamen in der Pivot-Tabelle
MONAT_MAPPING = {
    1: "Januar",
    2: "Februar",
    3: "März",
    4: "April",
    5: "Mai",
    6: "Juni",
    7: "Juli",
    8: "August",
    9: "September",
    10: "Oktober",
    11: "November",
    12: "Dezember",
}

# 🛑 Nutzereingabe auskommentiert, Testdaten werden verwendet
# def nutzereingabe():
#     datum = input("Bitte gebe Sie das Datum ein: ")
#     produkt_name = input("Gebe den Produktnamen ein: ")
#     menge = int(input("Gebe die Menge ein: "))
#     preis = float(input("Gebe den Preis ein: "))
#     return datum, produkt_name, menge, preis


def create_table(connection, cursor):
    """
    Erstellt die beiden notwendigen Tabellen:
    - `verkaufstabelle`: Speichert alle Verkäufe mit Datum, Produkt, Menge, Preis und Umsatz.
    - `jahresübersicht`: Speichert die monatlichen Umsätze pro Produkt.
    """
    cursor.execute(
        f"""
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
        f"""
        CREATE TABLE IF NOT EXISTS jahresübersicht (
            id INTEGER PRIMARY KEY,
            produkt_name TEXT,
            budget REAL,
            {", ".join(f"{monat} REAL DEFAULT 0" for monat in MONAT_MAPPING.values())}
        );
        """
    )
    connection.commit()


def insert_values(connection, cursor):
    """
    Füllt die `verkaufstabelle` mit Testdaten (anstatt Nutzereingabe).
    """
    print("\n🛠 **Schritt 1: Testdaten einfügen...**")

    testdaten = [
        ("01.01.2024", "Laptop", 2, 1200.50),
        ("15.02.2024", "Monitor", 1, 300.00),
        ("20.03.2024", "Maus", 5, 25.99),
        ("10.06.2024", "Tastatur", 3, 49.99),
        ("05.09.2024", "Schreibtisch", 1, 250.00),
    ]

    cursor.executemany(
        """
        INSERT OR IGNORE INTO verkaufstabelle (datum, produkt_name, menge, preis, umsatz) 
        VALUES (?, ?, ?, ?, ?);
        """,
        [
            (datum, produkt, menge, preis, menge * preis)
            for datum, produkt, menge, preis in testdaten
        ],
    )

    connection.commit()
    print("✅ **Testdaten erfolgreich eingefügt.**")


def yearly_results(conn, cursor):
    """
    Liest die `verkaufstabelle`, erstellt eine Pivot-Tabelle und speichert sie in `jahresübersicht`.
    """

    print("\n📊 **Schritt 2: Daten aus der Verkaufstabelle in DataFrame laden...**\n")
    df = pd.read_sql_query(
        "SELECT datum, produkt_name, umsatz FROM verkaufstabelle", conn
    )

    # ✅ Debug: Anzeige des DataFrames
    print("🔍 **Lade Daten aus der Datenbank in DataFrame:**\n")
    print(df.to_string(index=False))  # Bessere Anzeige ohne die Index-Spalte anzuzeigen

    # Konvertiere das Datum (String) in ein echtes Datumsformat (datetime Objekt)
    df["datum"] = pd.to_datetime(df["datum"], format="%d.%m.%Y")
    df["Monat"] = df["datum"].dt.month  # Extrahiere die Monatszahl

    # ✅ Debug: Spaltentypen anzeigen
    print("\n🔍 **Spaltentypen im DataFrame:**")
    print(df.dtypes)

    # ✅ Debug: Einzigartige Werte für Produkte und Monate
    print("\n🔍 **Einzigartige Produktnamen:**", df["produkt_name"].unique())
    print("🔍 **Einzigartige Monate:**", df["Monat"].unique())

    print("\n📈 **Schritt 3: Pivot-Tabelle erstellen...**\n")

    # Erstelle die Pivot-Tabelle (Monatszahlen als Spalten)
    pivot_df = df.pivot_table(
        index="produkt_name",
        columns="Monat",
        values="umsatz",
        aggfunc="sum",
        fill_value=0,  # Fehlende Werte direkt mit 0 füllen
    )

    # ✅ Debug: Pivot-Tabelle vor Umbenennung von Monatszahlen zu Monatsnamen anzeigen
    print("🔍 **Pivot-Tabelle vor der Umbenennung (Mit Monatszahlen):**\n")
    print(pivot_df.to_string())

    # 🔄 Sicherstellen, dass ALLE 12 Monate als Spalten vorhanden sind
    #   ,weil in der Pivot-Tabelle aktuell nur die Monate enthalten sind, wo auch ein Umsatz entstanden ist.
    for monat in range(1, 13):
        if monat not in pivot_df.columns:
            pivot_df[monat] = 0  # Fehlende Monate hinzufügen

    # Spalten umbenennen (1 → "Januar", 2 → "Februar", ...)
    pivot_df.columns = [MONAT_MAPPING[m] for m in pivot_df.columns]

    # 🛠 Index (Produktname) zurück in eine Spalte umwandeln
    pivot_df.reset_index(inplace=True)

    # ✅ Debug: Pivot-Tabelle nach Umbenennung von Monatzszahlen zu Monatsnamen anzeigen
    print("\n🔍 **Pivot-Tabelle nach der Umbenennung (Mit Monatsnamen):**\n")
    print(pivot_df.to_string(index=False))

    print("\n🗑 **Schritt 4: `jahresübersicht` leeren...**")
    cursor.execute("DELETE FROM jahresübersicht")
    conn.commit()
    print("✅ `jahresübersicht` wurde geleert.")

    print("\n📤 **Schritt 5: Speichern der Pivot-Tabelle in `jahresübersicht`...**")
    pivot_df.to_sql("jahresübersicht", conn, if_exists="replace", index=False)
    print("✅ **Pivot-Tabelle wurde erfolgreich in `jahresübersicht` gespeichert.**")


def main():
    """
    Hauptprogramm:
    - Stellt die Verbindung zur Datenbank her
    - Erstellt die Tabellen
    - Fügt Testdaten ein
    - Führt die Analyse durch
    - Schließt die Verbindung
    """
    print("\n🏁 **Starte das Programm...**\n")

    connection = sqlite3.connect("products.db")
    cursor = connection.cursor()

    create_table(connection, cursor)
    insert_values(connection, cursor)
    yearly_results(connection, cursor)

    connection.close()
    print("\n✅ **Programm erfolgreich abgeschlossen.**")


if __name__ == "__main__":
    main()
