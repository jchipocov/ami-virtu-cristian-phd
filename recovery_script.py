
import pandas as pd
import re
import os

def recover_data():
    log_path = r'c:\Users\jchip\OneDrive\Desktop\MAC_DESKTOP\2026\Asesorias\Cristian\Proyecto\learning_analytics_ami\logs\auditoria_cualitativa.md'
    csv_output = r'c:\Users\jchip\OneDrive\Desktop\MAC_DESKTOP\2026\Asesorias\Cristian\Proyecto\learning_analytics_ami\data\processed\hybrid_analysis_results.csv'
    
    if not os.path.exists(log_path):
        print("Log not found.")
        return

    with open(log_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Split by student sections
    sections = re.split(r'## Auditoría Estudiante:', content)[1:]
    
    recovered_rows = []
    
    for section in sections:
        # Extract Student ID
        id_match = re.search(r'^(STU_\d+)', section.strip())
        if not id_match: continue
        stu_id = id_match.group(1)
        
        # Extract Section B responses
        # Format: | BC1 | ... | Respuesta |
        answers = {}
        rows = re.findall(r'\| (B[C|T|P]\d) \| .*? \| (.*?) \|', section)
        for code, text in rows:
            answers[code] = text.strip()
            
        if len(answers) == 12:
            row = {'ID_Estudiante': stu_id}
            row.update(answers)
            recovered_rows.append(row)

    df_recovered = pd.DataFrame(recovered_rows)
    
    # Sort and remove duplicates (in case of multiple runs in same log)
    df_recovered = df_recovered.drop_duplicates(subset=['ID_Estudiante'], keep='last')
    df_recovered = df_recovered.sort_values('ID_Estudiante')
    
    print(f"Recuperados {len(df_recovered)} registros cualitativos.")
    
    # Join with numerical data (if possible)
    # Since we don't have the full DF here, we'll save this as a partial recovery
    df_recovered.to_csv(csv_output.replace('.csv', '_RECOVERY_QUAL.csv'), index=False)
    print(f"Dataset cualitativo guardado en: {csv_output.replace('.csv', '_RECOVERY_QUAL.csv')}")

if __name__ == "__main__":
    recover_data()
