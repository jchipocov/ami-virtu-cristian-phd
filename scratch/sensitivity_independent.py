import pandas as pd
import numpy as np
from scipy import stats
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# Reconstruct N=743 as done in generate_oe1_descriptives.py
df_raw = pd.read_excel('data/raw/Formulario de Investigación Académica Doctoral - BIU(823).xlsx')
consent_col = df_raw.columns[6]
virtual_col = df_raw.columns[8]
df_filt = df_raw[(df_raw[consent_col].astype(str).str.upper().str.strip() == "ACEPTO PARTICIPAR") & 
                 (df_raw[virtual_col].astype(str).str.strip().str.upper().isin(["SÍ", "SI"]))].copy().reset_index(drop=True)
df_filt['ID_Estudiante'] = [f'STU_{str(i).zfill(4)}' for i in range(1, len(df_filt) + 1)]

# Map Likert items
raw_likert_cols = df_filt.columns[9:39]
mapping = {
    'Totalmente en desacuerdo': 1, 'En desacuerdo': 2, 'Neutral': 3,
    'De acuerdo': 4, 'Totalmente de acuerdo': 5,
    'Nunca': 1, 'Raramente': 2, 'A veces': 3, 'Frecuentemente': 4, 'Siempre': 5,
    '1': 1, '2': 2, '3': 3, '4': 4, '5': 5
}
ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
df_likert = df_filt[raw_likert_cols].apply(lambda col: col.map(mapping))
df_likert.columns = ami_items

# Invert C6 (f(x) = 6 - x)
df_likert['C6'] = 6 - df_likert['C6']

df_sens = pd.concat([df_filt[['ID_Estudiante']], df_likert], axis=1)

# Flag inconsistencies on df_sens (774 cases)
# A2 and A4 from raw
df_sens['A4'] = df_filt.iloc[:, 42].astype(str).str.strip()
df_sens['A2_Desaprobados'] = df_filt.iloc[:, 40].astype(str).str.strip()

flags = []
for idx, r in df_sens.iterrows():
    vals = r[ami_items]
    var_v = vals.var()
    nan_c = vals.isna().sum()
    a4 = str(r['A4']).lower()
    a2 = str(r['A2_Desaprobados'])
    is_flat = (var_v == 0)
    is_empty = (nan_c == 30)
    is_disc = (a4 == 'alto') and (a2 == 'En dos o más')
    flags.append(is_flat or is_empty or is_disc)

df_sens['Flag_Inconsistencia'] = flags
df_743 = df_sens[df_sens['Flag_Inconsistencia'] == False].copy().reset_index(drop=True)

# Impute df_743
imputer = IterativeImputer(random_state=42, max_iter=10)
imp_vals_743 = imputer.fit_transform(df_743[ami_items])
df_743_imp = df_743.copy()
df_743_imp[ami_items] = np.round(imp_vals_743).clip(1, 5).astype(int)

crit_cols = [f'C{i}' for i in range(1, 11)]
tec_cols = [f'T{i}' for i in range(1, 11)]
part_cols = [f'P{i}' for i in range(1, 11)]

df_743_imp['Score_Critico'] = df_743_imp[crit_cols].mean(axis=1)
df_743_imp['Score_Tecnico'] = df_743_imp[tec_cols].mean(axis=1)
df_743_imp['Score_Participativo'] = df_743_imp[part_cols].mean(axis=1)
df_743_imp['Score_AMI_Global'] = (df_743_imp['Score_Critico'] + df_743_imp['Score_Tecnico'] + df_743_imp['Score_Participativo']) / 3.0

# Load N=702 analytical final
df_702 = pd.read_csv('data/outputs/oe1_caracterizacion_20260802/real_ami_virtu_analytical_final_702.csv')

# Find the 41 reincorporated cases
ids_702 = set(df_702['ID_Estudiante'])
df_41 = df_743_imp[~df_743_imp['ID_Estudiante'].isin(ids_702)].copy()
print(f"Total N=743: {len(df_743_imp)}, Total N=702: {len(df_702)}, Total reincorporados: {len(df_41)}")

print("\n--- COMPARACION DE GRUPOS INDEPENDIENTES: N=702 (Retenidos) vs N=41 (Excluidos por IA) ---")
for dim, col in [('Crítico', 'Score_Critico'), ('Técnico', 'Score_Tecnico'), ('Participativo', 'Score_Participativo'), ('AMI Global', 'Score_AMI_Global')]:
    x_702 = df_702[col]
    x_41 = df_41[col]
    
    m_702, s_702 = x_702.mean(), x_702.std()
    m_41, s_41 = x_41.mean(), x_41.std()
    diff = m_702 - m_41
    
    # Welch t-test between independent groups
    t_stat, p_val = stats.ttest_ind(x_702, x_41, equal_var=False)
    
    # Cohen's d between independent groups
    n1, n2 = len(x_702), len(x_41)
    s_pooled = np.sqrt(((n1 - 1)*s_702**2 + (n2 - 1)*s_41**2) / (n1 + n2 - 2))
    d = (m_702 - m_41) / s_pooled
    
    print(f"{dim:15s} | 702: M={m_702:.4f} (SD={s_702:.4f}) | 41: M={m_41:.4f} (SD={s_41:.4f}) | Diff={diff:+.4f} | d={d:.4f} | t={t_stat:.4f} | p={p_val:.4f}")

print("\n--- COMPARACION DESCRIPTIVA DE SENSIBILIDAD: N=702 vs N=743 ---")
for dim, col in [('Crítico', 'Score_Critico'), ('Técnico', 'Score_Tecnico'), ('Participativo', 'Score_Participativo'), ('AMI Global', 'Score_AMI_Global')]:
    m_702 = df_702[col].mean()
    m_743 = df_743_imp[col].mean()
    delta = m_702 - m_743
    pct_change = (delta / m_702) * 100
    print(f"{dim:15s} | M(702)={m_702:.4f} | M(743)={m_743:.4f} | Delta={delta:+.4f} | %Delta={pct_change:.2f}%")
