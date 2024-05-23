import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import t

# Specify the path of the CSV file
umsaetze_df = r"C:\Users\l.hapke\Desktop\python\Übung 2 Kiwo - Visualisierung von Daten\umsatzdaten_gekuerzt.csv" #Replace with your actual file path

# Read the CSV file
umsaetze_df = pd.read_csv(umsaetze_df)

# Print the first 5 rows of the DataFrame
print(umsaetze_df.head())

def wochentag_aus_datum(datum):
    # Wochentage in Deutsch
    wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
    
    try:
        # Datum in datetime-Objekt umwandeln
        datum_obj = pd.to_datetime(datum)
        
        # Überprüfen, ob das Datum gültig ist
        if pd.isnull(datum_obj):
            return "Ungültiges Datum"
        
        # Wochentag aus dem datetime-Objekt extrahieren
        wochentag_index = datum_obj.dayofweek
        
        # Den entsprechenden Wochentag aus der Liste abrufen und zurückgeben
        return wochentage[wochentag_index]
    except ValueError:
        return "Ungültiges Datum"

# Beispiel DataFrame
data = {
    'Datum': ["2024-04-30", "2024-05-01", "2024-05-02", "2024-05-03", "2024-05-04", "2024-13-32"],
}

df = pd.DataFrame(data)

# Neue Spalte für den Wochentag hinzufügen
umsaetze_df['Wochentag'] = umsaetze_df['Datum'].apply(wochentag_aus_datum)

print(umsaetze_df)

unique_warengruppen = umsaetze_df['Warengruppe'].unique()
print("Eindeutige Werte in der Spalte 'Warengruppe':")
for warengruppe in unique_warengruppen:
    print(warengruppe)

# Umsätze nach Datum gruppieren und Summe berechnen
umsatzagg_df = umsaetze_df.groupby('Datum')['Umsatz'].sum().reset_index()

# Spalte umbenennen
umsatzagg_df.rename(columns={'Umsatz': 'Umsatzagg'}, inplace=True)

# DataFrame zusammenführen, um die Umsatzaggregationsdaten hinzuzufügen
umsaetze_df = pd.merge(umsaetze_df, umsatzagg_df, on='Datum', how='left')

# Ergebnis anzeigen
print(umsaetze_df.head())


# Annahme: Der DataFrame umsaetze_df ist bereits vorhanden und enthält die Spalten 'Wochentag' und 'Umsatz'
import numpy as np
import matplotlib.pyplot as plt

# Einstellung der Schriftart
plt.rcParams['font.family'] = 'Raleway'

# Einstellung des Hintergrunds
plt.rcParams['axes.facecolor'] = 'lightpink'

# Reihenfolge der Wochentage festlegen
wochentage = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

# Umsätze nach Wochentag gruppieren und Durchschnitt berechnen
durchschnittsumsatz_pro_wochentag = umsaetze_df.groupby('Wochentag')['Umsatz'].mean()

confidence = 0.95
n = len(umsaetze_df)  # Number of data points
std_err = umsaetze_df.groupby('Wochentag')['Umsatz'].std() / np.sqrt(n)  # Standard error
t_value = t.ppf((1 + confidence) / 2, n - 1)  # T-score
margin_of_error = t_value * std_err  # Margin of error
# Balkendiagramm erstellen

plt.figure(figsize=(10, 6))
durchschnittsumsatz_pro_wochentag = durchschnittsumsatz_pro_wochentag.reindex(wochentage)  # Reihenfolge anpassen
bars = plt.bar(np.arange(len(durchschnittsumsatz_pro_wochentag)), durchschnittsumsatz_pro_wochentag, color='lightgreen', edgecolor='black', linewidth=1.5, capsize=5)
plt.errorbar(np.arange(len(durchschnittsumsatz_pro_wochentag)), durchschnittsumsatz_pro_wochentag, yerr=margin_of_error, fmt='none', ecolor='black', capsize=5)
plt.title('Durchschnittlicher Umsatz je Wochentag', fontsize=14, fontweight='bold', color='black')  # Titel fett und größer
plt.xlabel('Wochentag', fontsize=12, fontweight='bold', color='black')  # Achsenbeschriftungen fett
plt.ylabel('Durchschnittlicher Umsatz (€)', fontsize=12, fontweight='bold', color='black')  # Achsenbeschriftungen fett
plt.xticks(np.arange(len(durchschnittsumsatz_pro_wochentag)), wochentage, rotation=0, color='black')  # Schrift gerade
plt.yticks(color='black')  # Farbe der y-Achsenbeschriftungen auf Schwarz setzen
plt.grid(axis='y', linestyle='--', alpha=0.7)

# Mittelwerte innerhalb der Balken anzeigen
for bar, mean in zip(bars, durchschnittsumsatz_pro_wochentag):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height / 2, f'{mean:.2f} €', ha='center', va='center', color='black', fontweight='bold')

plt.tight_layout()

plt.show()


# das konfidenzintervall noch mal mit den reduzierten Anzahl an "Umsatztagen" berechnen
