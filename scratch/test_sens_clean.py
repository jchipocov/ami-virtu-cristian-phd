import pandas as pd
import numpy as np
from scipy import stats
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

critico_cols = [f'C{i}' for i in range(1, 11)]
tecnico_cols = [f'T{i}' for i in range(1, 11)]
participativo_cols = [f'P{i}' for i in range(1, 11)]
ami_items = critico_cols + tecnico_cols + participativo_cols

df_774 = pd.read_csv('data/processed/real_hybrid_analysis_results_823.csv')
mask_psycho_774 = df_774['Flag_Inconsistencia'] == False
df_743_raw = df_774[mask_psycho_774].copy().reset_index(drop=True)

imputer_774 = IterativeImputer(random_state=42, max_iter=10)
df_743 = df_743_raw.copy()
imputed_743 = imputer_774.fit_transform(df_743_raw[ami_items])
df_743[ami_items] = np.round(imputed_743).clip(1, 5).astype(int)

df_743['Score_Critico'] = df_743[critico_cols].mean(axis=1)
df_743['Score_Tecnico'] = df_743[tecnico_cols].mean(axis=1)
df_743['Score_Participativo'] = df_743[participativo_cols].mean(axis=1)
df_743['Score_AMI_Global'] = (df_743['Score_Critico'] + df_743['Score_Tecnico'] + df_743['Score_Participativo']) / 3.0

df_702 = pd.read_csv('data/outputs/oe1_caracterizacion_20260802/real_ami_virtu_analytical_final_702.csv')

ids_702 = set(df_702['ID_Estudiante'])
df_41 = df_743[~df_743['ID_Estudiante'].isin(ids_702)].copy()

print(f"Total N=743: {len(df_743)}, Total N=702: {len(df_702)}, Total reincorporados: {len(df_41)}")

print("\n--- 1. COMPARACION DE GRUPOS INDEPENDIENTES: N=702 (Retenidos) vs N=41 (Excluidos por IA) ---")
dims = [
    ("Score_Critico", "Crítico"),
    ("Score_Tecnico", "Técnico"),
    ("Score_Participativo", "Participativo"),
    ("Score_AMI_Global", "AMI Global")
]

for col, name in dims:
    x_702 = df_702[col]
    x_41 = df_41[col]
    
    m_702, s_702 = x_702.mean(), x_702.std(ddof=1)
    m_41, s_41 = x_41.mean(), x_41.std(ddof=1)
    diff = m_702 - m_41
    
    # Welch t-test (truly independent groups)
    t_stat, p_val = stats.ttest_ind(x_702, x_41, equal_var=False)
    
    # Cohen's d
    n1, n2 = len(x_702), len(x_41)
    s_pooled = np.sqrt(((n1 - 1)*s_702**2 + (n2 - 1)*s_41**2) / (n1 + n2 - 2))
    d = diff / s_pooled
    
    print(f"{name:15s} | 702: M={m_702:.4f} (SD={s_702:.4f}) | 41: M={m_41:.4f} (SD={s_41:.4f}) | Diff={diff:+.4f} | d={d:.4f} | t_Welch={t_stat:.4f} | p={p_val:.4f}")

print("\n--- 2. COMPARACION DESCRIPTIVA DE SENSIBILIDAD MUESTRAL: N=702 vs N=743 ---")
for col, name in dims:
    m_702 = df_702[col].mean()
    m_743 = df_743[col].mean()
    diff = m_702 - m_743
    pct = (diff / m_702) * 100
    sd_702 = df_702[col].std(ddof=1)
    d_std = diff / sd_702  # Estandarizado respecto al grupo de referencia N=702
    print(f"{name:15s} | M(702)={m_702:.4f} | M(743)={m_743:.4f} | Delta={diff:+.4f} | %Cambio={pct:.2f}% | Delta/SD_702={d_std:.4f}")
