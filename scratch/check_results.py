import pandas as pd

def check_real_data():
    try:
        print("Cargando dataset depurado final (real_ami_virtu_final_paper_ready.csv)...")
        df = pd.read_csv("data/processed/real_ami_virtu_final_paper_ready.csv")
        
        print(f"-> Total de registros cargados: {len(df)}")
        
        qual_cols = ["Sentimiento_Academico", "Indice_Coherencia", "Analisis_Cuali", "Etiquetas_Tematicas"]
        
        print("\n--- Verificación de campos cualitativos ---")
        for col in qual_cols:
            if col in df.columns:
                null_count = df[col].isnull().sum()
                unique_values = df[col].nunique()
                print(f"Columna: '{col}'")
                print(f"  - Datos nulos: {null_count} / {len(df)}")
                print(f"  - Valores únicos: {unique_values}")
                if df[col].dtype in ['float64', 'int64']:
                    print(f"  - Rango: [{df[col].min()} a {df[col].max()}]")
                    print(f"  - Promedio: {df[col].mean():.4f}")
            else:
                print(f"Columna: '{col}' -> ❌ NO ENCONTRADA EN EL DATASET")
                
        # Mostrar los primeros 3 estudiantes
        print("\n--- Muestra de los primeros 3 estudiantes procesados ---")
        sample = df[["ID_Estudiante", "Score_AMI_Global", "Riesgo_Total"] + qual_cols].head(3)
        for idx, row in sample.iterrows():
            print(f"\nID: {row['ID_Estudiante']}")
            print(f"  - Score AMI: {row['Score_AMI_Global']:.3f}")
            print(f"  - Riesgo: {'SÍ' if row['Riesgo_Total'] == 1 else 'NO'}")
            print(f"  - Sentimiento: {row['Sentimiento_Academico']}")
            print(f"  - Coherencia: {row['Indice_Coherencia']}")
            print(f"  - Temas: {row['Etiquetas_Tematicas']}")
            print(f"  - Análisis: {row['Analisis_Cuali'][:120]}...")
            
    except Exception as e:
        print(f"Error al verificar la data: {e}")

if __name__ == "__main__":
    check_real_data()
