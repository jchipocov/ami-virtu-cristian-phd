"""Test de imputacion MICE - version memoria reducida."""
import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'

import pandas as pd
import numpy as np

df = pd.read_csv('data/processed/real_ami_virtu_final_paper_ready.csv')
df_active = df[df['Flag_Inconsistencia'] == False].copy()

ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
ami_present = [c for c in ami_items if c in df_active.columns]

for c in ami_present:
    df_active[c] = pd.to_numeric(df_active[c], errors='coerce')

# Estado ANTES
n_missing = df_active[ami_present].isnull().sum().sum()
listwise_before = df_active[ami_present].dropna().shape[0]
print(f"=== ANTES ===")
print(f"N activos: {len(df_active)}")
print(f"Total NaN: {n_missing}")
print(f"Listwise completos: {listwise_before}")

# IMPUTAR con IterativeImputer (threads limitados)
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

imputer = IterativeImputer(
    random_state=42,
    max_iter=5,
    n_nearest_features=10,
    sample_posterior=False
)
ami_data = df_active[ami_present].values
ami_imputed = imputer.fit_transform(ami_data)

# Redondear a [1, 5]
ami_imputed = np.round(ami_imputed).clip(1, 5).astype(int)
df_active[ami_present] = ami_imputed

# Estado DESPUES
n_missing_after = df_active[ami_present].isnull().sum().sum()
listwise_after = df_active[ami_present].dropna().shape[0]
print(f"\n=== DESPUES ===")
print(f"Total NaN: {n_missing_after}")
print(f"Listwise completos: {listwise_after}")
print(f"Mejora: {listwise_before} -> {listwise_after} ({listwise_after - listwise_before:+d})")

# Recalcular scores
df_active['Score_Critico'] = df_active[[f'C{i}' for i in range(1, 11)]].mean(axis=1)
df_active['Score_Tecnico'] = df_active[[f'T{i}' for i in range(1, 11)]].mean(axis=1)
df_active['Score_Participativo'] = df_active[[f'P{i}' for i in range(1, 11)]].mean(axis=1)
df_active['Score_AMI_Global'] = df_active[['Score_Critico', 'Score_Tecnico', 'Score_Participativo']].mean(axis=1)

print(f"\nScores post-imputacion:")
for s in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    print(f"  {s}: mean={df_active[s].mean():.3f}, std={df_active[s].std():.3f}, N={df_active[s].notna().sum()}")

# Correlaciones
print(f"\nCorrelaciones post-imputacion (N={len(df_active)}):")
for s in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    x = df_active[s]; y = df_active['Riesgo_Total']
    mx = x.mean(); my = y.mean()
    num = ((x - mx) * (y - my)).sum()
    den = (((x - mx)**2).sum() * ((y - my)**2).sum())**0.5
    r = num / den if den > 0 else 0
    print(f"  {s} vs Riesgo: r={r:.4f}")

print(f"\nEFA ratio: {len(df_active)}/30 = {len(df_active)/30:.1f}:1")
