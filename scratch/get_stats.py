import pandas as pd

df = pd.read_csv('data/processed/real_hybrid_analysis_results.csv')

# Flatliners detail
flat = df[df['Flag_Inconsistencia'] == True]
print(f'=== FLATLINERS (Flag_Inconsistencia=True): {len(flat)} ===')
for _, r in flat.iterrows():
    sid = r.get('ID', 'N/A')
    score = r.get('Score_AMI_Global', 'N/A')
    print(f'  {sid}: Score_AMI_Global={score}')

# Coherence filter
print(f'\n=== COHERENCE FILTER ===')
print(f'Indice_Coherencia stats:')
print(df['Indice_Coherencia'].describe())
low_coh = df[df['Indice_Coherencia'] < 0.6]
print(f'Rows with Indice_Coherencia < 0.6: {len(low_coh)}')

# Check which flatliners are also low coherence
flat_and_low = df[(df['Flag_Inconsistencia'] == True) & (df['Indice_Coherencia'] < 0.6)]
print(f'Flatliners AND low coherence: {len(flat_and_low)}')

# Only low coherence (not flatliner)
only_low_coh = df[(df['Flag_Inconsistencia'] == False) & (df['Indice_Coherencia'] < 0.6)]
print(f'Only low coherence (not flatliner): {len(only_low_coh)}')

# Missing data
for dim, prefix in [('Critica', 'C'), ('Tecnica', 'T'), ('Participativa', 'P')]:
    cols = [f'{prefix}{i}' for i in range(1, 11)]
    exist = [c for c in cols if c in df.columns]
    if exist:
        complete = df[exist].dropna(how='any')
        avg_miss = df[exist].isnull().mean().mean() * 100
        print(f'{dim}: {len(complete)}/{len(df)} complete, avg missing={avg_miss:.1f}%')

# Listwise for 30 items
ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
exist_items = [c for c in ami_items if c in df.columns]
complete_all = df[exist_items].dropna(how='any')
print(f'\nListwise complete (30 items): {len(complete_all)}/{len(df)}')

# Paper ready scores
df2 = pd.read_csv('data/processed/real_ami_virtu_final_paper_ready.csv')
active = df2[df2['Flag_Inconsistencia'] == False]
print(f'\n=== ACTIVE CASES (paper ready, no flag) ===')
print(f'N_active: {len(active)}')
for s in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    vals = active[s].dropna()
    print(f'{s}: mean={vals.mean():.3f}, std={vals.std():.3f}, N_valid={len(vals)}')

# Riesgo in active
print(f'Riesgo in active:')
print(active['Riesgo_Total'].value_counts())

# University in active
print(f'Universidad in active:')
print(active['Universidad'].value_counts())

# Sentimiento stats
print(f'\nSentimiento_Academico stats (active):')
print(active['Sentimiento_Academico'].describe())

# Qualitative fields check
for col in ['Analisis_Cuali', 'Sentimiento_Academico', 'Indice_Coherencia', 'Etiquetas_Tematicas']:
    if col in active.columns:
        non_null = active[col].notna().sum()
        print(f'{col}: {non_null}/{len(active)} non-null')

# Scores for full hybrid (N=303) 
print(f'\n=== SCORES in HYBRID (N=303) ===')
for s in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    vals = df[s].dropna()
    print(f'{s}: mean={vals.mean():.3f}, std={vals.std():.3f}, N_valid={len(vals)}')
