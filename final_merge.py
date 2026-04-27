
import pandas as pd
import os

def final_merge():
    # Paths
    qual_path = r'c:\Users\jchip\OneDrive\Desktop\MAC_DESKTOP\2026\Asesorias\Cristian\Proyecto\learning_analytics_ami\data\processed\hybrid_analysis_results_RECOVERY_QUAL.csv'
    raw_path = r'c:\Users\jchip\OneDrive\Desktop\MAC_DESKTOP\2026\Asesorias\Cristian\Proyecto\learning_analytics_ami\data\raw\simulated_raw_data.csv'
    final_output = r'c:\Users\jchip\OneDrive\Desktop\MAC_DESKTOP\2026\Asesorias\Cristian\Proyecto\learning_analytics_ami\data\processed\hybrid_analysis_results.csv'
    
    if not os.path.exists(qual_path) or not os.path.exists(raw_path):
        print("Required files for merge not found.")
        return

    # Load data
    df_qual = pd.read_csv(qual_path)
    df_num = pd.read_csv(raw_path)
    
    # Rename key column in numerical data to match recovered data
    df_num = df_num.rename(columns={'Estudiante_ID': 'ID_Estudiante'})
    
    # Merge on ID_Estudiante
    df_final = pd.merge(df_num, df_qual, on='ID_Estudiante', how='inner')
    
    # --- RIGOR METODOLÓGICO: CONVERSIÓN Y INVERSIÓN ---
    likert_map = {
        "Totalmente en desacuerdo": 1, "En desacuerdo": 2, 
        "Ni de acuerdo ni en desacuerdo": 3, "De acuerdo": 4, 
        "Totalmente de acuerdo": 5
    }
    
    inverted_items = ['C6', 'T6', 'P5']
    all_ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
    
    for item in all_ami_items:
        if item in df_final.columns:
            # Si es texto, mapear. Si ya es número, dejarlo.
            if df_final[item].dtype == 'object':
                df_final[item] = df_final[item].map(likert_map)
            df_final[item] = pd.to_numeric(df_final[item], errors='coerce')

    for item in inverted_items:
        if item in df_final.columns:
            # Escala Likert 1-5: Invertir es 6 - X
            df_final[item] = 6 - df_final[item]
            print(f"   [!] Ítem {item} invertido metodológicamente.")

    # Calculate dimension scores
    crit_cols = [f'C{i}' for i in range(1, 11)]
    tec_cols = [f'T{i}' for i in range(1, 11)]
    part_cols = [f'P{i}' for i in range(1, 11)]
    
    df_final['Score_Critico'] = df_final[crit_cols].mean(axis=1)
    df_final['Score_Tecnico'] = df_final[tec_cols].mean(axis=1)
    df_final['Score_Participativo'] = df_final[part_cols].mean(axis=1)
    df_final['Score_AMI_Global'] = df_final[['Score_Critico', 'Score_Tecnico', 'Score_Participativo']].mean(axis=1)
    
    # Riesgo Total (Proxy basado en la simulación original si no está presente)
    if 'Riesgo_Total' not in df_final.columns:
        # Si no está, lo calculamos como un umbral (ej. AMI bajo = Riesgo alto)
        # Pero usualmente simulated_raw_data ya trae variables de riesgo.
        pass

    # Save final
    df_final.to_csv(final_output, index=False)
    print(f"Dataset FINAL generado con {len(df_final)} estudiantes en: {final_output}")

if __name__ == "__main__":
    final_merge()
