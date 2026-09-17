import pandas as pd
import numpy as np

# Load raw excel to trace 823 -> 818 -> 774
df_raw = pd.read_excel('data/raw/Formulario de Investigación Académica Doctoral - BIU(823).xlsx')

consent_col = df_raw.columns[6]
virtual_col = df_raw.columns[8]

# 1. Filtro consentimiento
mask_consent = df_raw[consent_col].astype(str).str.upper().str.strip() == "ACEPTO PARTICIPAR"
df_818 = df_raw[mask_consent].copy().reset_index(drop=True)

# 2. Filtro virtual
mask_virtual = df_818[virtual_col].astype(str).str.strip().str.upper().isin(["SÍ", "SI"])
df_774 = df_818[mask_virtual].copy().reset_index(drop=True)
df_774['ID_Estudiante'] = [f'STU_{str(i).zfill(4)}' for i in range(1, len(df_774) + 1)]

print(f"Bruto: {len(df_raw)} -> Consentimiento: {len(df_818)} -> Virtual (Elegibles): {len(df_774)}")

# Likert columns
raw_likert_cols = df_774.columns[9:39]
mapping = {
    'Totalmente en desacuerdo': 1, 'En desacuerdo': 2, 'Neutral': 3,
    'De acuerdo': 4, 'Totalmente de acuerdo': 5,
    'Nunca': 1, 'Raramente': 2, 'A veces': 3, 'Frecuentemente': 4, 'Siempre': 5,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5
}
ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
df_likert = df_774[raw_likert_cols].apply(lambda col: col.map(mapping)).astype(float)
df_likert.columns = ami_items

# Inversion de C6: f(x) = 6 - x
df_likert['C6'] = 6.0 - df_likert['C6']

# Evaluacion de reglas objetivas de calidad cuantitativa en los 774
# 1. Varianza cero en datos brutos pre-inversion (o post-inversion)
# En datos brutos pre-inversion (los 30 items respondidos exactamente iguales):
df_likert_raw = df_774[raw_likert_cols].apply(lambda col: col.map(mapping)).astype(float)
var_pre_raw = df_likert_raw.var(axis=1)
nans_per_row = df_likert_raw.isna().sum(axis=1)

# Flatliners (varianza cero en items no nulos, con al menos 2 respuestas)
is_flatliner = (var_pre_raw == 0) & (nans_per_row < 30)

# Escala totalmente vacia
is_empty_scale = (nans_per_row == 30)

print(f"\n--- AUDITORIA DE REGLAS OBJETIVAS EN N=774 ---")
print(f"Flatliners (Varianza = 0 pre-inversion): {is_flatliner.sum()}")
for val in [5, 4, 3, 2, 1]:
    sub_count = 0
    for idx, r in df_likert_raw[is_flatliner].iterrows():
        unique_vals = r.dropna().unique()
        if len(unique_vals) == 1 and unique_vals[0] == val:
            sub_count += 1
    if sub_count > 0:
        print(f"  - Uniformes {val}: {sub_count}")

print(f"Escalas completamente vacias (30 NaNs): {is_empty_scale.sum()}")
print(f"Solapamiento flatliner y vacia: {(is_flatliner & is_empty_scale).sum()}")

total_exclusiones_objetivas = is_flatliner | is_empty_scale
print(f"Total exclusiones puramente cuantitativas: {total_exclusiones_objetivas.sum()}")

n_cuantitativo_oficial = len(df_774) - total_exclusiones_objetivas.sum()
print(f"\n>>> N CUANTITATIVO RESULTANTE: {n_cuantitativo_oficial} <<<")

# Verifiquemos que pasa si comparamos con hybrid_csv_path
df_hybrid = pd.read_csv('data/processed/real_hybrid_analysis_results_823.csv')
print(f"\nVerificacion en hybrid_csv (N={len(df_hybrid)}):")
# Chequear flatliners en hybrid
hybrid_likert_raw = df_hybrid[ami_items].copy()
# Note that in hybrid, C6 is already inverted, so let's re-invert C6 to see pre-inversion
hybrid_likert_pre = hybrid_likert_raw.copy()
hybrid_likert_pre['C6'] = 6.0 - hybrid_likert_pre['C6']
var_hybrid_pre = hybrid_likert_pre.var(axis=1)
nans_hybrid = hybrid_likert_pre.isna().sum(axis=1)

is_flat_hyb = (var_hybrid_pre == 0) & (nans_hybrid < 30)
is_empty_hyb = (nans_hybrid == 30)
print(f"Flatliners en hybrid_csv: {is_flat_hyb.sum()}")
print(f"Escalas vacias en hybrid_csv: {is_empty_hyb.sum()}")
print(f"Total exclusiones objetivas en hybrid_csv: {(is_flat_hyb | is_empty_hyb).sum()}")
print(f"N resultante en hybrid_csv: {len(df_hybrid) - (is_flat_hyb | is_empty_hyb).sum()}")
