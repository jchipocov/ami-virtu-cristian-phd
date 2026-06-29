import pandas as pd

def count_flags():
    try:
        df_raw = pd.read_csv("data/processed/real_hybrid_analysis_results.csv")
        df_final = pd.read_csv("data/processed/real_ami_virtu_final_paper_ready.csv")
        
        print("=== ANÁLISIS DE FILTROS APLICADOS ===")
        print(f"1. Muestra cargada desde el loader (post-filtros de consentimiento y virtualidad): {len(df_raw)} casos")
        
        flatliners_raw = df_raw[df_raw["Flag_Inconsistencia"] == True]
        print(f"2. Casos sospechosos cuantitativos (Flatliners, var=0) detectados: {len(flatliners_raw)} casos")
        
        excluded_ia = len(df_raw) - len(df_final)
        print(f"3. Casos excluidos por coherencia IA (< 0.6): {excluded_ia} casos")
        
        print(f"4. Muestra final en 'real_ami_virtu_final_paper_ready.csv': {len(df_final)} casos")
        
        flatliners_in_final = df_final[df_final["Flag_Inconsistencia"] == True]
        print(f"5. De los {len(df_final)} casos finales, ¿cuántos son Flatliners? {len(flatliners_in_final)} casos")
        
        active_for_analysis = len(df_final) - len(flatliners_in_final)
        print(f"6. Casos activos para análisis estadístico (final - flatliners): {active_for_analysis} casos")
        
        # ¿Qué flatliners se eliminaron por coherencia y cuáles quedan?
        flatliner_ids_raw = set(flatliners_raw["ID_Estudiante"])
        flatliner_ids_final = set(flatliners_in_final["ID_Estudiante"])
        flatliners_deleted_by_ia = flatliner_ids_raw - flatliner_ids_final
        print(f"  - Flatliners eliminados automáticamente por filtro de coherencia IA: {len(flatliners_deleted_by_ia)}")
        print(f"  - Flatliners que aún quedan en el archivo final (marcados como Flag_Inconsistencia=True): {len(flatliner_ids_final)}")
        print(f"    IDs de flatliners que quedan: {sorted(list(flatliner_ids_final))}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    count_flags();
