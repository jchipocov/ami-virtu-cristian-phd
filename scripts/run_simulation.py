
import os
import sys
import pandas as pd
from datetime import datetime

# Añadir raíz al path
root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(root_dir)

from src.simulation.data_simulator import DataSimulator
from src.simulation.qualitative_generator import QualitativeGenerator
from src.processing.cleaner import DataCleaner
from src.processing.scorer import Scorer

def generate_full_dataset(num_students=300):
    print("==================================================")
    print(f"  GENERADOR HÍBRIDO AMI-VIRTU (Standalone) N={num_students} ")
    print("==================================================")
    
    # 1. Simulación Cuantitativa
    print("\n[1/4] Generando base cuantitativa (Cópulas)...")
    simulator = DataSimulator(num_records=num_students, risk_ratio=0.33)
    df_raw = simulator.generate_dataset()
    
    # 2. Limpieza y Scorer Base (necesario para que Gemini vea los scores)
    print("[2/4] Limpiando y calculando scores base...")
    cleaner = DataCleaner()
    scorer = Scorer()
    df_clean = cleaner.clean_process(df_raw)
    df_scored = scorer.score_process(df_clean)
    
    # 3. Generación Cualitativa (Gemini)
    print("[3/4] Generando respuestas abiertas (Gemini API)...")
    qual_gen = QualitativeGenerator()
    df_hybrid = qual_gen.generate_qualitative_data(df_scored)
    
    # 4. Guardado Permanente
    output_path = os.path.join(root_dir, "data", "processed", "hybrid_analysis_results.csv")
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df_hybrid.to_csv(output_path, index=False, encoding='utf-8-sig')
    
    print("\n==================================================")
    print(f" PROCESO COMPLETADO EXIOTOSAMENTE ")
    print(f" Archivo generado: {output_path}")
    print("==================================================")

if __name__ == "__main__":
    # Podemos pasar el número de alumnos por argumento
    n = 300
    if len(sys.argv) > 1:
        n = int(sys.argv[1])
    generate_full_dataset(n)
