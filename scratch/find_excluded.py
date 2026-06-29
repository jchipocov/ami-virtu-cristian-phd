import pandas as pd

def find_excluded_students():
    try:
        # Cargar ambos datasets
        df_results = pd.read_csv("data/processed/real_hybrid_analysis_results.csv")
        df_final = pd.read_csv("data/processed/real_ami_virtu_final_paper_ready.csv")
        
        # Estudiantes en results pero no en final
        excluded_ids = set(df_results["ID_Estudiante"]) - set(df_final["ID_Estudiante"])
        
        print(f"Total de estudiantes en la base híbrida: {len(df_results)}")
        print(f"Total de estudiantes en la base final: {len(df_final)}")
        print(f"Cantidad de estudiantes excluidos por coherencia (< 0.6): {len(excluded_ids)}")
        
        if len(excluded_ids) > 0:
            df_excluded = df_results[df_results["ID_Estudiante"].isin(excluded_ids)]
            print("\n--- Lista de estudiantes excluidos en esta corrida (Índice de Coherencia < 0.6) ---")
            for idx, row in df_excluded.iterrows():
                print(f"ID: {row['ID_Estudiante']}")
                print(f"  - Coherencia: {row['Indice_Coherencia']}")
                print(f"  - Sentimiento: {row['Sentimiento_Academico']}")
                print(f"  - Score AMI Global: {row['Score_AMI_Global']:.3f}")
                print(f"  - Cuali (BC1): \"{str(row.get('BC1', ''))[:100]}...\"")
                print(f"  - Análisis IA: \"{str(row.get('Analisis_Cuali', ''))[:150]}...\"")
                print("-" * 50)
        else:
            print("\nNo se excluyó a ningún estudiante en esta corrida.")
            
    except Exception as e:
        print(f"Error al buscar estudiantes excluidos: {e}")

if __name__ == "__main__":
    find_excluded_students()
