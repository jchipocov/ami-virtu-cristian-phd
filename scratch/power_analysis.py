import pandas as pd
import numpy as np
from scipy import stats
import warnings
warnings.filterwarnings('ignore')

df = pd.read_csv('data/processed/real_hybrid_analysis_results.csv')
N = len(df)

print('=== ANALISIS DE POTENCIA ESTADISTICA ===')
print()

c_cols = [f'C{i}' for i in range(1,11)]
t_cols = [f'T{i}' for i in range(1,11)]
p_cols = [f'P{i}' for i in range(1,11)]

c_complete = df[c_cols].dropna()
t_complete = df[t_cols].dropna()
p_complete = df[p_cols].dropna()
all_ami = c_cols + t_cols + p_cols
df_ami_complete = df[all_ami].dropna()

print(f'N total muestra: {N}')
print(f'N casos completos dim. Critica (C1-C10):      {len(c_complete)} ({len(c_complete)/N*100:.1f}%)')
print(f'N casos completos dim. Tecnica (T1-T10):      {len(t_complete)} ({len(t_complete)/N*100:.1f}%)')
print(f'N casos completos dim. Participativa (P1-P10):{len(p_complete)} ({len(p_complete)/N*100:.1f}%)')
print(f'N casos con AMI 30 items completos (listwise): {len(df_ami_complete)} ({len(df_ami_complete)/N*100:.1f}%)')
print()

n_risk = (df['Riesgo_Total'] == 1).sum()
n_no_risk = (df['Riesgo_Total'] == 0).sum()
prevalence = n_risk / N
print(f'=== DISTRIBUCION DE LA VARIABLE OBJETIVO ===')
print(f'Sin riesgo (0): {n_no_risk} ({n_no_risk/N*100:.1f}%)')
print(f'Con riesgo (1): {n_risk} ({n_risk/N*100:.1f}%)')
print(f'Prevalencia de riesgo: {prevalence*100:.1f}%')
print()

print(f'=== EPV - EVENTS PER VARIABLE (Regresion Logistica) ===')
for preds in [3, 5, 8, 10, 15]:
    epv = n_risk / preds
    if epv >= 10:
        status = 'OK'
    elif epv >= 5:
        status = 'MARGINAL'
    else:
        status = 'INSUFICIENTE'
    print(f'  {preds} predictores -> EPV={epv:.1f} [{status}]')
print(f'Peduzzi et al. (1996): EPV minimo = 10')
print()

print(f'=== EFA (Hair et al. 2014: min 5:1, rec 10:1) ===')
for n_items in [30, 20, 15, 10]:
    ratio = len(df_ami_complete) / n_items
    if ratio >= 10:
        status = 'OK'
    elif ratio >= 5:
        status = 'MARGINAL'
    else:
        status = 'INSUFICIENTE'
    print(f'  {n_items} items -> ratio = {ratio:.1f}:1 [{status}]')
print()
print(f'MacCallum et al. (1999): N>=200 para EFA comunalidades moderadas')
if len(df_ami_complete) >= 200:
    print(f'  Estado: OK ({len(df_ami_complete)} casos completos)')
else:
    print(f'  Estado: ADVERTENCIA ({len(df_ami_complete)} casos completos, requiere FIML o imputacion)')
print()

print(f'=== MISSING DATA EN ITEMS AMI ===')
missing_c = df[c_cols].isnull().sum()
missing_t = df[t_cols].isnull().sum()
missing_p = df[p_cols].isnull().sum()
print('Dim. Critica (C1-C10):')
for c,m in missing_c.items():
    print(f'  {c}: {m} missing ({m/N*100:.1f}%)')
print('Dim. Tecnica (T1-T10):')
for c,m in missing_t.items():
    print(f'  {c}: {m} missing ({m/N*100:.1f}%)')
print('Dim. Participativa (P1-P10):')
for c,m in missing_p.items():
    print(f'  {c}: {m} missing ({m/N*100:.1f}%)')
print()

# Scores disponibles
print('=== SCORES AMI DISPONIBLES ===')
for sc in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    if sc in df.columns:
        n_valid = df[sc].notna().sum()
        mean_val = df[sc].mean()
        std_val = df[sc].std()
        print(f'  {sc}: N={n_valid}, media={mean_val:.3f}, SD={std_val:.3f}')
print()

# Analisis de outliers
print('=== ANALISIS DE DATOS ATIPICOS (Flag_Inconsistencia) ===')
if 'Flag_Inconsistencia' in df.columns:
    n_flag = df['Flag_Inconsistencia'].sum()
    print(f'  Casos flagged: {n_flag} ({n_flag/N*100:.1f}%)')
    print(f'  N validos para analisis: {N - n_flag} ({(N-n_flag)/N*100:.1f}%)')
print()

# Distribucion Scores AMI por Universidad
print('=== SCORES AMI POR UNIVERSIDAD ===')
for univ in df['Universidad'].unique():
    sub = df[df['Universidad'] == univ]
    sc_mean = sub['Score_AMI_Global'].mean()
    sc_std = sub['Score_AMI_Global'].std()
    n_riesgo = (sub['Riesgo_Total'] == 1).sum()
    print(f'  {univ}: N={len(sub)}, AMI_Global={sc_mean:.2f}(+-{sc_std:.2f}), Riesgo={n_riesgo}({n_riesgo/len(sub)*100:.1f}%)')
print()

# Correlacion bivariada AMI vs Riesgo
print('=== CORRELACIONES BIVARIADAS (AMI vs RIESGO) ===')
for sc in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    if sc in df.columns:
        pair = df[[sc, 'Riesgo_Total']].dropna()
        if len(pair) > 2:
            r, p = stats.pearsonr(pair[sc], pair['Riesgo_Total'])
            rho, p_s = stats.spearmanr(pair[sc], pair['Riesgo_Total'])
            sig = 'SIG' if p < 0.05 else ('TREND' if p < 0.10 else 'NS')
            print(f'  {sc}: Pearson r={r:+.3f} (p={p:.4f} {sig}), Spearman rho={rho:+.3f}')

print()
print('=== ANALISIS DE POTENCIA A PRIORI (estimado) ===')
print('Para Pearson r con N=303:')
from scipy.stats import t as t_dist
for r_target in [0.1, 0.15, 0.2, 0.25, 0.3]:
    t_stat = r_target * np.sqrt(N - 2) / np.sqrt(1 - r_target**2)
    p_val = 2 * (1 - t_dist.cdf(abs(t_stat), df=N-2))
    power_str = 'POTENCIA ALTA' if p_val < 0.05 else 'NS'
    print(f'  r={r_target:.2f} con N={N}: t={t_stat:.2f}, p={p_val:.4f} [{power_str}]')
