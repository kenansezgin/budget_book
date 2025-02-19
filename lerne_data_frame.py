import pandas as pd  # Pandas importieren

# 1️⃣ Daten als Dictionary definieren
data = {
    "Produkt": ["Apfel", "Banane", "Orange", "Apfel", "Banane", "Orange"],
    "Menge": [10, 5, 8, 15, 7, 12],
    "Preis": [0.5, 0.3, 0.7, 0.5, 0.3, 0.7],
    "Datum": [
        "01.02.2024",
        "02.02.2024",
        "03.02.2024",
        "04.02.2024",
        "05.02.2024",
        "06.02.2024",
    ],
}


df = pd.DataFrame(data)
print(df)

# Neue Spalte einfügen
df["Umsatz"] = df["Menge"] * df["Preis"]
print(df)


# Datum in ein korrektes Format umwandeln
df["Datum"] = pd.to_datetime(df["Datum"], format="%d.%m.%Y")
print(df)

# Ausgabe des Datums im deutschen Format anzeigen
print(df.assign(Datum=df["Datum"].dt.strftime("%d.%m.%Y")))

# Daten filtern: Alle Verkäufe nach dem 03.02.2024
gefilterte_daten = df[df["Datum"] > "2024-02-03"]
print("\n ", gefilterte_daten)

# Daten gruppieren: Gesamtumsatz pro Produkt
print("Hier ist der Umsatz: ")
umsatz_pro_produkt = df.groupby("Produkt")["Umsatz"].sum()
print(umsatz_pro_produkt)

# 7️⃣ DataFrame als CSV-Datei speichern
df.to_csv("verkaufsdaten.csv", index=False)

# 8️⃣ Ergebnisse anzeigen
print("📊 Ursprüngliche Daten:")
print(df)

print("\n📌 Verkäufe nach dem 03.02.2024:")
print(gefilterte_daten)

print("\n💰 Gesamtumsatz pro Produkt:")
print(umsatz_pro_produkt)


df["Gesamtumsatz"] = df.groupby("Produkt")["Umsatz"].sum()

print(df)
