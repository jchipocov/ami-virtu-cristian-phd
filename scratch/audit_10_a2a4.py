import pandas as pd
import numpy as np

df_729 = pd.read_csv('data/processed/real_ami_virtu_final_paper_ready_823.csv')
ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]

cases_27 = df_729[df_729['Flag_Inconsistencia'] == True].copy()

# Find the 10 A2/A4 cases
a4_cases = []
for idx, r in cases_27.iterrows():
    a4 = str(r.get('A4', '')).strip().lower()
    a2 = str(r.get('A2_Desaprobados', '')).strip()
    vals = r[ami_items]
    var_val = vals.var()
    if (a4 == 'alto') and (a2 == 'En dos o más') and var_val > 0:
        a4_cases.append(r)

df_10 = pd.DataFrame(a4_cases)
print(f"Total casos A4='alto' y A2='En dos o más' con var > 0: {len(df_10)}")
print(df_10[['ID_Estudiante', 'Universidad', 'A4', 'A2_Desaprobados', 'Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']])

print("\nVarianzas de los 10 casos en los 30 items:")
for idx, r in df_10.iterrows():
    vals = r[ami_items]
    print(f"{r['ID_Estudiante']}: var={vals.var():.3f}, mean={vals.mean():.3f}, min={vals.min()}, max={vals.max()}, nans={vals.isna().sum()}")

# What if we include them? N = 712
df_valid_702 = df_729[df_729['Flag_Inconsistencia'] == False]
df_712 = pd.concat([df_valid_702, df_10])

print(f"\nComparacion descriptivos N=702 vs N=712:")
for score_col in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    m_702 = df_valid_702[score_col].mean()
    m_712 = df_712[score_col].mean()
    s_702 = df_valid_702[score_col].std()
    s_712 = df_712[score_col].std()
    diff = m_712 - m_702
    print(f"{score_col}: M(702)={m_702:.4f}, M(712)={m_712:.4f}, diff={diff:+.4f}")
