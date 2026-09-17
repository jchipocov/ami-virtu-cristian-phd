import pandas as pd
df_raw = pd.read_excel('data/raw/Formulario de Investigación Académica Doctoral - BIU(823).xlsx')

print("Columnas 39 a 45 del raw excel:")
for i, col in enumerate(df_raw.columns[39:46], 39):
    print(f"Col {i}: {col}")

col_a2 = df_raw.columns[40]
col_a4 = df_raw.columns[42]
print(f"\nA2 nombre completo: {col_a2}")
print(f"A2 valores unicos: {df_raw[col_a2].value_counts(dropna=False)}")

print(f"\nA4 nombre completo: {col_a4}")
print(f"A4 valores unicos: {df_raw[col_a4].value_counts(dropna=False)}")
