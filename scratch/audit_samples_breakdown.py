import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

critico_cols = [f'C{i}' for i in range(1, 11)]
tecnico_cols = [f'T{i}' for i in range(1, 11)]
participativo_cols = [f'P{i}' for i in range(1, 11)]
ami_items = critico_cols + tecnico_cols + participativo_cols

df_774 = pd.read_csv('data/processed/real_hybrid_analysis_results_823.csv')

# Let's inspect the 4 cases in IA that overlapped with Flag_Inconsistencia
# In df_774, Flag_Inconsistencia is already present
print("En df_774 (N=774):")
print("Flag_Inconsistencia value counts:", df_774['Flag_Inconsistencia'].value_counts())

# The 45 excluded by IA:
df_ia_45 = df_774[df_774['Indice_Coherencia'] < 0.60]
print(f"Total IA < 0.60: {len(df_ia_45)}")
print(f"De ellos, Flag_Inconsistencia=True: {(df_ia_45['Flag_Inconsistencia'] == True).sum()}")
print(f"De ellos, Flag_Inconsistencia=False: {(df_ia_45['Flag_Inconsistencia'] == False).sum()}")

# 774 - 31 con Flag_Inconsistencia = 743
# Let's inspect the 31 cases with Flag_Inconsistencia in df_774:
df_31 = df_774[df_774['Flag_Inconsistencia'] == True]
print(f"Total casos con Flag_Inconsistencia=True en N=774: {len(df_31)}")

# Breakdown of the 31 cases:
flat_15 = []
empty_2 = []
a2a4_14 = [] # let's see how many A2/A4 in 774
other = []
for idx, r in df_31.iterrows():
    vals = r[ami_items]
    var_v = vals.var()
    nans = vals.isna().sum()
    a4 = str(r.get('A4', '')).strip().lower()
    a2 = str(r.get('A2_Desaprobados', '')).strip()
    is_a2a4 = (a4 == 'alto') and (a2 == 'En dos o más')
    if var_v == 0:
        flat_15.append(r['ID_Estudiante'])
    elif nans == 30:
        empty_2.append(r['ID_Estudiante'])
    elif is_a2a4:
        a2a4_14.append(r['ID_Estudiante'])
    else:
        other.append(r['ID_Estudiante'])

print(f"En N=774: Varianza=0: {len(flat_15)}, Escala vacia: {len(empty_2)}, A2/A4: {len(a2a4_14)}, Otro: {len(other)}")

# In the 729 (where IA >= 0.60):
df_729 = df_774[df_774['Indice_Coherencia'] >= 0.60]
df_27 = df_729[df_729['Flag_Inconsistencia'] == True]
print(f"\nEn N=729: Total Flag_Inconsistencia: {len(df_27)}")

# Check missing data in N=702 analytical final
df_702 = pd.read_csv('data/outputs/oe1_caracterizacion_20260802/real_ami_virtu_analytical_final_702.csv')
# But in df_702 the values are already imputed!
# Let's check the pre-imputation missing data in the 702 subjects:
df_702_raw = df_729[df_729['Flag_Inconsistencia'] == False]
miss_702_crit = df_702_raw[critico_cols].isnull().sum().sum()
miss_702_tec = df_702_raw[tecnico_cols].isnull().sum().sum()
miss_702_part = df_702_raw[participativo_cols].isnull().sum().sum()
total_cells_702 = len(df_702_raw) * 30
total_miss_702 = miss_702_crit + miss_702_tec + miss_702_part
print(f"\nMissing pre-imputacion en los N=702 validos:")
print(f"Critico: {miss_702_crit} / {702*10} ({miss_702_crit/(702*10)*100:.2f}%)")
print(f"Tecnico: {miss_702_tec} / {702*10} ({miss_702_tec/(702*10)*100:.2f}%)")
print(f"Participativo: {miss_702_part} / {702*10} ({miss_702_part/(702*10)*100:.2f}%)")
print(f"Total: {total_miss_702} / {total_cells_702} ({total_miss_702/total_cells_702*100:.2f}%)")
