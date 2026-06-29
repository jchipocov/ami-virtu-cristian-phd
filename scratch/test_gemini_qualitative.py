import sys
import os
import pandas as pd

# Añadir directorio raíz al path para poder importar src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.analysis.qualitative_engine import QualitativeEngine

def test_qualitative_engine():
    print("Inicializando QualitativeEngine con la configuración actual...")
    try:
        engine = QualitativeEngine()
        print(f"-> Clave API cargada (primeros 5 caracteres): {engine.api_key[:5] if engine.api_key else 'None'}...")
        print(f"-> Modelo configurado: {engine.model_name}")
        
        # Fila de prueba que contiene datos cuantitativos y cualitativos
        mock_student = pd.Series({
            "ID_Estudiante": "STU_TEST_CONEXION",
            "Score_Critico": 4.5,
            "Score_Tecnico": 4.0,
            "Score_Participativo": 3.5,
            "Riesgo_Total": 0,
            "BC1": "Siempre verifico que las páginas de internet tengan fuentes institucionales o autores reconocidos.",
            "BC2": "Comparo las noticias entre diferentes diarios para ver si hay inconsistencias.",
            "BC3": "Busco información científica en portales académicos como Scielo.",
            "BC4": "Identifico si la información está sesgada por intereses políticos.",
            "BT1": "Utilizo la plataforma Teams y el aula virtual del campus sin problemas.",
            "BT2": "Suelo adaptarme rápido a las nuevas herramientas que introduce la universidad.",
            "BT3": "Sé cómo resolver incidencias básicas cuando la plataforma se cae.",
            "BT4": "Envío mis tareas dentro del plazo establecido.",
            "BP1": "Comparto materiales y lecturas en los grupos de estudio de WhatsApp.",
            "BP2": "Participo activamente en los foros de debate del curso virtual.",
            "BP3": "Prefiero realizar trabajos grupales a través de herramientas colaborativas.",
            "BP4": "Publico mis opiniones y aportes académicos en redes sociales."
        })
        
        print("\nEnviando fila de prueba a Gemini...")
        result = engine.analyze_single_student(mock_student)
        
        print("\n--- RESULTADO DE LA API DE GEMINI ---")
        print(f"ID: {result.get('ID_Estudiante')}")
        print(f"Sentimiento Académico (0-1): {result.get('Sentimiento_Academico')}")
        print(f"Índice de Coherencia (0-1): {result.get('Indice_Coherencia')}")
        print(f"Etiquetas Temáticas: {result.get('Etiquetas_Tematicas')}")
        print(f"Análisis Cualitativo: {result.get('Analisis_Cuali')}")
        print("-------------------------------------")
        
        if result.get("Analisis_Cuali") and not str(result.get("Analisis_Cuali")).startswith("Error:"):
            print("\n[OK] La API respondio exitosamente y el formato JSON fue parseado correctamente!")
        else:
            print("\n[ERROR] La llamada fallo o devolvio un error en el campo Analisis_Cuali.")
            
    except Exception as e:
        print(f"\n[ERROR] Error al inicializar o ejecutar el motor: {e}")

if __name__ == "__main__":
    test_qualitative_engine()
