import pandas as pd
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.processing.scorer import Scorer

def test_compute_risk_target_expanded():
    scorer = Scorer()
    
    df = pd.DataFrame({
        'A1_Interrupcion': ['No', 'Sí', 'No', 'No', 'No', 'No'],
        'A4_Rendimiento': ['Alto', 'Medio', 'Bajo', 'Medio', 'Medio', 'Medio'],
        'A5_Dificultad': [1, 2, 2, 5, 2, 1], # 5 = Riesgo
        'L1': [1, 1, 1, 1, 4, 1],             # 4 = Riesgo
        'L2_Inactividad': [1, 1, 2, 1, 2, 5]  # 5 = Riesgo
    })
    
    df_scored = scorer.compute_risk_target(df)
    
    assert df_scored['Riesgo_Total'].iloc[0] == 0, "Error: Estudiante sano fue catalogado con Riesgo"
    assert df_scored['Riesgo_Total'].iloc[1] == 1, "Error: Falló al capturar A1 (Interrupción)"
    assert df_scored['Riesgo_Total'].iloc[2] == 1, "Error: Falló al capturar A4 (Rendimiento Bajo)"
    assert df_scored['Riesgo_Total'].iloc[3] == 1, "Error: Falló al capturar Likert Académico (A5)"
    assert df_scored['Riesgo_Total'].iloc[4] == 1, "Error: Falló al capturar Likert Documental (L1)"
    assert df_scored['Riesgo_Total'].iloc[5] == 1, "Error: Falló al capturar Inactividad (L2)"
