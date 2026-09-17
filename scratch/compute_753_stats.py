import pandas as pd
import numpy as np
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

df_774 = pd.read_csv('data/processed/real_hybrid_analysis_results_823.csv')
ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
critico_cols = [f'C{i}' for i in range(1, 11)]
tecnico_cols = [f'T{i}' for i in range(1, 11)]
participativo_cols = [f'P{i}' for i in range(1, 11)]

# Excluir solo los 21 flatliners (var == 0 pre-inversion)
df_pre = df_774.copy()
df_pre['C6'] = 6.0 - df_pre['C6']
is_flat = df_pre[ami_items].var(axis=1) == 0

df_753_raw = df_774[~is_flat].copy().reset_index(drop=True)
print(f"Total df_753_raw: {len(df_753_raw)}")

# Missing data en N=753
miss_crit = df_753_raw[critico_cols].isnull().sum().sum()
miss_tec = df_753_raw[tecnico_cols].isnull().sum().sum()
miss_part = df_753_raw[participativo_cols].isnull().sum().sum()
tot_miss = miss_crit + miss_tec + miss_part
tot_cells = len(df_753_raw) * 30

print(f"\nMissing data en N=753:")
print(f"Critico: {miss_crit} / {len(df_753_raw)*10} ({miss_crit/(len(df_753_raw)*10)*100:.2f}%)")
print(f"Tecnico: {miss_tec} / {len(df_753_raw)*10} ({miss_tec/(len(df_753_raw)*10)*100:.2f}%)")
print(f"Participativo: {miss_part} / {len(df_753_raw)*10} ({miss_part/(len(df_753_raw)*10)*100:.2f}%)")
print(f"Total: {tot_miss} / {tot_cells} ({tot_miss/tot_cells*100:.2f}%)")

# Imputacion iterativa multivariada
imputer = IterativeImputer(random_state=42, max_iter=10)
imp_matrix = imputer.fit_transform(df_753_raw[ami_items])
df_753 = df_753_raw.copy()
df_753[ami_items] = np.round(imp_matrix).clip(1, 5).astype(int)

df_753['Score_Critico'] = df_753[critico_cols].mean(axis=1)
df_753['Score_Tecnico'] = df_753[tecnico_cols].mean(axis=1)
df_753['Score_Participativo'] = df_753[participativo_cols].mean(axis=1)
df_753['Score_AMI_Global'] = (df_753['Score_Critico'] + df_753['Score_Tecnico'] + df_753['Score_Participativo']) / 3.0

print("\n--- DESCRIPTIVOS OE1 EN MUESTRA CUANTITATIVA OFICIAL N=753 ---")
for col, name in [('Score_Critico', 'Crítico'), ('Score_Tecnico', 'Técnico'), ('Score_Participativo', 'Participativo'), ('Score_AMI_Global', 'AMI Global')]:
    s = df_753[col]
    print(f"{name:15s} | Media={s.mean():.4f} | DE={s.std():.4f} | Mediana={s.median():.4f} | Min={s.min():.1f} | Max={s.max():.1f} | Asim={s.skew():.4f} | Curt={s.kurt():.4f}")

# Cronbach alphas en N=753
def alpha(df_sub):
    k = df_sub.shape[1]
    item_vars = df_sub.var(axis=0, ddof=1).sum()
    tot_var = df_sub.sum(axis=1).var(ddof=1)
    return (k / (k - 1)) * (1 - item_vars / tot_var)

print("\n--- ALFA DE CRONBACH EN N=753 ---")
print(f"Critico: {alpha(df_753[critico_cols]):.4f}")
print(f"Tecnico: {alpha(df_753[tecnico_cols]):.4f}")
print(f"Participativo: {alpha(df_753[participativo_cols]):.4f}")
print(f"AMI Global: {alpha(df_753[ami_items]):.4f}")

# Comparacion con N=702
df_702 = pd.read_csv('data/outputs/oe1_caracterizacion_20260802/real_ami_virtu_analytical_final_702.csv')
print("\n--- COMPARACION DE MEDIAS N=702 vs N=753 ---")
for col, name in [('Score_Critico', 'Crítico'), ('Score_Tecnico', 'Técnico'), ('Score_Participativo', 'Participativo'), ('Score_AMI_Global', 'AMI Global')]:
    m_702 = df_702[col].mean()
    m_753 = df_753[col].mean()
    diff = m_702 - m_753
    pct = (diff / m_702) * 100
    sd_702 = df_702[col].std()
    print(f"{name:15s} | M(702)={m_702:.4f} | M(753)={m_753:.4f} | Delta={diff:+.4f} | %Delta={pct:.2f}% | Delta/SD={diff/sd_702:.4f}")
