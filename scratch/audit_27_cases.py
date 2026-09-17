import pandas as pd
import numpy as np

df_729 = pd.read_csv('data/processed/real_ami_virtu_final_paper_ready_823.csv')
items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]

cases_27 = df_729[df_729['Flag_Inconsistencia'] == True]

# Check each case
print("Detailed breakdown of the 27 cases:")
for idx, r in cases_27.iterrows():
    stu_id = r['ID_Estudiante']
    raw_vals = r[items]
    num_nans = raw_vals.isna().sum()
    var_val = raw_vals.var()
    unique_vals = raw_vals.dropna().unique()
    a4 = r.get('A4', 'N/A')
    a2 = r.get('A2', 'N/A')
    print(f"{stu_id}: NaNs={num_nans}/30, var={var_val}, unique={unique_vals}, A4={a4}, A2={a2}")
