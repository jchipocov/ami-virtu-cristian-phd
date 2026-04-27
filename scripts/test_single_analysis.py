
import os
import sys
import pandas as pd
import json

# Raíz
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.analysis.qualitative_engine import QualitativeEngine

def test_single():
    csv_path = r'c:\Users\jchip\OneDrive\Desktop\MAC_DESKTOP\2026\Asesorias\Cristian\Proyecto\learning_analytics_ami\data\processed\hybrid_analysis_results.csv'
    if not os.path.exists(csv_path):
        print("CSV not found.")
        return
        
    df = pd.read_csv(csv_path)
    # Tomar el primero
    row = df.iloc[0]
    
    print(f"--- PROBANDO ANÁLISIS (GEMINI 3 FLASH) PARA: {row['ID_Estudiante']} ---")
    os.environ["GEMINI_MODEL"] = "gemini-3-flash-preview"
    engine = QualitativeEngine()
    
    try:
        result = engine.analyze_single_student(row)
        print("\n[RESULTADO DE LA IA]:")
        print(f"- Sentimiento: {result.get('Sentimiento_Academico')}")
        print(f"- Coherencia: {result.get('Indice_Coherencia')}")
        print(f"- Etiquetas: {result.get('Etiquetas_Tematicas')}")
        print(f"- Análisis: {result.get('Analisis_Cuali')}")
    except Exception as e:
        print(f"\n[!] ERROR DE API: {str(e)}")

if __name__ == "__main__":
    test_single()
