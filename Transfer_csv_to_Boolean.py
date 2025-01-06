import pandas as pd

# Lese die CSV-Datei ein
df = pd.read_csv('Results_Document-Alerting-Master_01_E03.csv', delimiter=';')

# Definiere eine Funktion, die entscheidet, welche Werte zu True und welche zu False konvertiert werden
def convert_to_boolean(value):
    true_values = ['True', 'true', 1, '1', 'yes', 'Yes']  # Werte, die als True interpretiert werden sollen
    false_values = ['False', 'false', 0, '0', 'no', 'No']  # Werte, die als False interpretiert werden sollen
    if value in true_values:
        return True
    elif value in false_values:
        return False
    else:
        return None  # Für Werte, die nicht eindeutig sind

# Wandle jede Spalte um
for column in df.columns:
    df[column] = df[column].apply(convert_to_boolean)

# Speichere die angepasste Datei
df.to_csv('Results_Document-Alerting-Master_01_E03_bool.csv', index=False)
