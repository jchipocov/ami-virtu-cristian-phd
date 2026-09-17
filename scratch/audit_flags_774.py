import pandas as pd
import numpy as np

df_774 = pd.read_csv('data/processed/real_hybrid_analysis_results_823.csv')
ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]

# Pre-inversion C6
df_pre = df_774.copy()
df_pre['C6'] = 6.0 - df_pre['C6']

var_pre = df_pre[ami_items].var(axis=1)
nans = df_pre[ami_items].isna().sum(axis=1)

is_flat = (var_pre == 0)
is_empty = (nans == 30)

a4 = df_774['A4'].astype(str).str.strip().str.lower()
a2 = df_774['A2_Desaprobados'].astype(str).str.strip()
is_a2a4 = (a4 == 'alto') & (a2 == 'En dos o más')

flag_orig = df_774['Flag_Inconsistencia'] == True

print(f"Total registros en df_774: {len(df_774)}")
print(f"Total con Flag_Inconsistencia original: {flag_orig.sum()}")
print(f"Total Flatliners (var=0): {is_flat.sum()}")
print(f"Total Escala vacia: {is_empty.sum()}")
print(f"Total A2/A4: {is_a2a4.sum()}")

print(f"Solapamiento Flatliner y A2/A4: {(is_flat & is_a2a4).sum()}")
print(f"Total Flatliner O A2/A4: {(is_flat | is_a2a4).sum()}")
print(f"Coincidencia exacta con Flag_Inconsistencia: {((is_flat | is_a2a4) == flag_orig).all()}")

# Breakdown of the 21 flatliners:
print("\nDesglose de los 21 flatliners por valor uniforme:")
for val in [5, 4, 3, 2, 1]:
    c = 0
    for idx, r in df_pre[is_flat].iterrows():
        u = r[ami_items].dropna().unique()
        if len(u) == 1 and u[0] == val:
            c += 1
    if c > 0:
        print(f"  Uniforme {val}: {c} casos")

# Now check how many of the 21 flatliners and 10 A2/A4 are in the 45 IA excluded
is_ia_low = df_774['Indice_Coherencia'] < 0.60
print(f"\nDe los 45 casos excluidos por IA (< 0.60):")
print(f"  - Son flatliners (var=0): {(is_ia_low & is_flat).sum()}")
print(f"  - Son A2/A4: {(is_ia_low & is_a2a4).sum()}")
print(f"  - Total con Flag_Inconsistencia: {(is_ia_low & flag_orig).sum()}")
print(f"  - Sin ninguna inconsistencia cuantitativa (validos en Likert): {(is_ia_low & ~flag_orig).sum()}")
