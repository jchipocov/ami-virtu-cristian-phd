import pandas as pd
df_729 = pd.read_csv('data/processed/real_ami_virtu_final_paper_ready_823.csv')
items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]

cases_27 = df_729[df_729['Flag_Inconsistencia'] == True]
print(f"Total cases with Flag_Inconsistencia=True: {len(cases_27)}")

mentira_count = 0
flatliner_count = 0
empty_count = 0
other_count = 0

for idx, r in cases_27.iterrows():
    stu = r['ID_Estudiante']
    a4 = str(r.get('A4', '')).strip().lower()
    a2 = str(r.get('A2_Desaprobados', '')).strip()
    is_mentira = (a4 == 'alto') and (a2 == 'En dos o más')
    
    vals = r[items]
    num_nans = vals.isna().sum()
    var_val = vals.var()
    
    cat = []
    if is_mentira:
        cat.append("Inconsistencia A4/A2")
        mentira_count += 1
    if var_val == 0:
        cat.append(f"Varianza=0 (unique={vals.dropna().unique()})")
        flatliner_count += 1
    elif num_nans == 30:
        cat.append("Escala vacía (30 NaNs)")
        empty_count += 1
    elif not is_mentira:
        cat.append(f"Otro (var={var_val:.4f}, NaNs={num_nans}, vals={vals.dropna().unique()[:4]})")
        other_count += 1
        
    print(f"{stu}: {', '.join(cat)}")

print(f"\nResumen: Inconsistencia A4/A2={mentira_count}, Varianza=0={flatliner_count}, Escala vacía={empty_count}, Otro={other_count}")
