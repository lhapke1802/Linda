import pandas as pd
import matplotlib.pyplot as plt
import statsmodels.api as sm
from statsmodels.stats.multicomp import MultiComparison
from scipy.stats import t

# Specify the path of the CSV file for "kiwo"
kiwo_df = r"C:\Users\l.hapke\Desktop\python\Datensätze\kiwo.csv" #Replace with your actual file path

# Read the CSV file
kiwo_df = pd.read_csv(kiwo_df)

# Print the first 5 rows of the DataFrame
print(kiwo_df.head())


# Specify the path of the CSV file for "Umsatzdaten"
umsaetze_df = r"C:\Users\l.hapke\Desktop\python\Datensätze\umsatzdaten_gekuerzt.csv" #Replace with your actual file path

# Read the CSV file
umsaetze_df = pd.read_csv(umsaetze_df)

# Print the first 5 rows of the DataFrame
print(umsaetze_df.head())

# Specify the path of the CSV file for "Wetter"
wetter_df = r"C:\Users\l.hapke\Desktop\python\Datensätze\wetter.csv" #Replace with your actual file path

# Read the CSV file
wetter_df = pd.read_csv(wetter_df)

# Print the first 5 rows of the DataFrame
print(wetter_df.head())

# Merge the dataframes on the 'Datum' column
merged_df = pd.merge(kiwo_df, umsaetze_df, on='Datum', how='outer')
merged_df = pd.merge(merged_df, wetter_df, on='Datum', how='outer')



# Print the first 5 rows of the merged DataFrame
print(merged_df.head())



print(merged_df.info())

print(merged_df.describe())

print(merged_df['KielerWoche'].value_counts())
print(merged_df['Warengruppe'].value_counts())
print(merged_df['Windgeschwindigkeit'].value_counts())

print(merged_df['Umsatz'].kurtosis())
print(merged_df['Umsatz'].skew())

print(merged_df['Bewoelkung'].kurtosis())
print(merged_df['Bewoelkung'].skew())

print(merged_df['Temperatur'].kurtosis())
print(merged_df['Temperatur'].skew())

print(merged_df['Windgeschwindigkeit'].kurtosis())
print(merged_df['Windgeschwindigkeit'].skew())

merged_df['KielerWoche'].value_counts().plot(kind='bar')
plt.xlabel('Kieler Woche')
plt.ylabel('Häufigkeit')
plt.title('Kieler Woche Tage')
plt.show()

merged_df['Warengruppe'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Verteilung der Warengruppen')
plt.ylabel('')
plt.show()

merged_df['Windgeschwindigkeit'].value_counts().plot(kind='pie', autopct='%1.1f%%')
plt.title('Verteilung der Warengruppen')
plt.ylabel('')
plt.show()

plt.figure(figsize=(8, 6))
plt.bar(merged_df['Warengruppe'], merged_df['Umsatz'])
plt.title('Umsatz nach Warengruppe')
plt.xlabel('Warengruppe')
plt.ylabel('Umsatz')
plt.grid(axis='y')
plt.show()

plt.figure(figsize=(8, 6))
plt.bar(merged_df['Datum'], merged_df['Temperatur'])
plt.title('Temperatur je Tag')
plt.xlabel('Datum', )
plt.ylabel('Temperatur')
plt.grid(axis='y')
plt.show()

plt.figure(figsize=(8, 6))
plt.bar(merged_df['Datum'], merged_df['Windgeschwindigkeit'])
plt.title('Windgeschwindigkeit je Tag')
plt.xlabel('Datum', )
plt.ylabel('Windgeschwindigkeit')
plt.grid(axis='y')
plt.show()

plt.figure(figsize=(8, 6))
plt.bar(merged_df['Datum'], merged_df['Wettercode'])
plt.title('Wettercode je Tag')
plt.xlabel('Datum', )
plt.ylabel('Wettercode')
plt.grid(axis='y')
plt.show()
# Imputation fehlender Werte mit dem Mittelwert
merged_df['Temperatur'].fillna(merged_df['Temperatur'].mean(), inplace=True)

# Scatterplot mit Trendlinie
plt.figure(figsize=(8, 6))

# Scatterplot der Daten
plt.scatter(merged_df['Temperatur'], merged_df['Umsatz'], label='Daten')

# Lineare Regression
X = sm.add_constant(merged_df['Temperatur']) # Konstante hinzufügen
model = sm.OLS(merged_df['Umsatz'], X).fit() # Lineare Regression durchführen
plt.plot(merged_df['Temperatur'], model.predict(X), color='red', label='Trendlinie')

plt.title('Umsatz in Bezug zur Temperatur (mit Imputation)')
plt.xlabel('Temperatur')
plt.ylabel('Umsatz')
plt.legend()
plt.grid(True)
plt.show()
