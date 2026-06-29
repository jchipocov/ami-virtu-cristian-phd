import pandas as pd

df = pd.read_csv('data/processed/real_hybrid_analysis_results.csv')
df2 = pd.read_csv('data/processed/real_ami_virtu_final_paper_ready.csv')
active = df2[df2['Flag_Inconsistencia'] == False]

# Exclusion breakdown
print("=== EXCLUSION BREAKDOWN ===")
print(f"Total hybrid: {len(df)}")
flat_count = (df['Flag_Inconsistencia']==True).sum()
low_coh = (df['Indice_Coherencia'] < 0.6).sum()
both = ((df['Flag_Inconsistencia']==True) & (df['Indice_Coherencia'] < 0.6)).sum()
print(f"Flatliners: {flat_count}")
print(f"Low coherence: {low_coh}")
print(f"Both: {both}")
print(f"Excluded from paper ready: {len(df) - len(df2)}")
print(f"Paper ready: {len(df2)}")
print(f"Active: {len(active)}")

# Flatliner score patterns
flat = df[df['Flag_Inconsistencia'] == True]
scores = flat['Score_AMI_Global'].round(2).value_counts().sort_index()
print("\n=== FLATLINER SCORES ===")
for s, n in scores.items():
    print(f"  Score={s}: N={n}")

# EFA in active
ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
exist_items = [c for c in ami_items if c in active.columns]
complete_active = active[exist_items].dropna(how='any')
print(f"\nEFA listwise active: {len(complete_active)}/{len(active)}")

for dim, prefix in [('Critica', 'C'), ('Tecnica', 'T'), ('Participativa', 'P')]:
    cols = [f'{prefix}{i}' for i in range(1, 11)]
    exist = [c for c in cols if c in active.columns]
    if exist:
        complete = active[exist].dropna(how='any')
        print(f"EFA {dim} active: {len(complete)}/{len(active)}")

# Correlations manual (no scipy)
print("\n=== CORRELATIONS (manual) ===")
for s in ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']:
    valid = active[[s, 'Riesgo_Total']].dropna()
    x = valid[s]
    y = valid['Riesgo_Total']
    n = len(valid)
    mx = x.mean()
    my = y.mean()
    num = ((x - mx) * (y - my)).sum()
    den = (((x - mx)**2).sum() * ((y - my)**2).sum())**0.5
    r = num / den if den > 0 else 0
    print(f"  {s} vs Riesgo: r={r:.3f}, N={n}")

# ARD variables
print("\n=== ARD-VIRTU (Paper Ready) ===")
for v in ['A1_Interrupcion', 'A2_Desaprobados', 'A3_Retirados']:
    if v in df2.columns:
        vc = df2[v].value_counts()
        print(f"  {v}: {dict(vc)}")

# Riesgo in active
riesgo = active['Riesgo_Total'].value_counts()
print(f"\nRiesgo active: Sin riesgo={riesgo.get(0,0)} ({riesgo.get(0,0)/len(active)*100:.1f}%), Con riesgo={riesgo.get(1,0)} ({riesgo.get(1,0)/len(active)*100:.1f}%)")

# University AMI means in active
for u in ['UNMSM', 'UNI']:
    sub = active[active['Universidad'] == u]
    print(f"{u}: N={len(sub)}, AMI_Global={sub['Score_AMI_Global'].mean():.3f}")
