import pandas as pd
import numpy as np
import os
import sys

# Agregar src al path temporalmente para importar modulos durante pruebas
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.processing.cleaner import DataCleaner

def test_reverse_negative_items():
    cleaner = DataCleaner()
    # Mock de datos donde C6, T6 y P5 tienen respuestas que deben invertirse (Score = 6 - Valor)
    df = pd.DataFrame({
        'C6': [5, 2, 1],
        'T6': [1, 4, 3],
        'P5': [1, 5, np.nan]
    })
    
    df_clean = cleaner.reverse_negative_items(df)
    
    # Validaciones matemáticas precisas
    assert df_clean['C6'].iloc[0] == 1, "Error: C6 con valor 5 debió invertirse a 1."
    assert df_clean['C6'].iloc[2] == 5, "Error: C6 con valor 1 debió invertirse a 5."
    assert df_clean['T6'].iloc[0] == 5, "Error: T6 con valor 1 debió invertirse a 5."
    assert pd.isna(df_clean['P5'].iloc[2]), "Error: Los valores nulos (NaN) no deben ser modificados."

def test_anomaly_detector_flatliner():
    cleaner = DataCleaner()
    # Mock de un encuestado "Flatliner" que no lee y marca 5 en las 30 preguntas AMI
    ami_cols = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
    data = {col: [5] for col in ami_cols}
    df = pd.DataFrame(data)
    
    df_clean = cleaner.anomaly_detector(df)
    
    # La varianza es 0 en todos los items, debe saltar la alarma de ocultismo
    assert df_clean['Flag_Inconsistencia'].iloc[0] == True, "Fallo grave: El bot flatliner no fue detectado por el analizador."

def test_anomaly_detector_semantic():
    cleaner = DataCleaner()
    # Mock: Estudiante dice tener nivel ALTO en A4, pero en A2 dice haber reprobado "En dos o más cursos"
    df = pd.DataFrame({
        'A4': [5],  # 5 = Alto
        'A2_Desaprobados': ['En dos o más cursos']
    })
    
    df_clean = cleaner.anomaly_detector(df)
    assert df_clean['Flag_Inconsistencia'].iloc[0] == True, "Fallo: No se detectó la contradicción semántica (Alto rendimiento vs 2 reprobados)."
