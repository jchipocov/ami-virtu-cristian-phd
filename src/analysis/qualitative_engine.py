import os
import pandas as pd
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time
import logging
from datetime import datetime

class QualitativeEngine:
    """
    Motor de Análisis Cualitativo Híbrido.
    Realiza la triangulación entre datos cuantitativos y cualitativos.
    Calcula el Índice de Coherencia y realiza codificación temática automática.
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        
        if not self.api_key:
            raise ValueError("Error: GEMINI_API_KEY no encontrada en .env")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)

        # --- Configuración de Logging Técnico ---
        self.log_file = f"logs/engine_hibrido_{datetime.now().strftime('%Y%m%d')}.log"
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True
        )

    def _generate_analysis_prompt(self, row: pd.Series):
        """Construye el prompt para el análisis de coherencia."""
        # Extraer cuanti
        scores = {
            "Critico": row.get('Score_Critico'),
            "Tecnico": row.get("Score_Tecnico"),
            "Participativo": row.get("Score_Participativo"),
            "Riesgo": "ALTO" if row.get("Riesgo_Total") == 1 else "BAJO"
        }
        
        # Extraer cuali (Sección B)
        respuestas = {
            k: row[k] for k in ["BC1", "BC2", "BC3", "BC4", "BT1", "BT2", "BT3", "BT4", "BP1", "BP2", "BP3", "BP4"]
            if k in row
        }

        prompt = f"""
        Analiza la coherencia de este estudiante en una encuesta de Alfabetización Mediática (AMI).
        
        DATOS CUANTITATIVOS (Scores 1-5):
        {json.dumps(scores, indent=2)}
        
        DATOS CUALITATIVOS (Respuestas abiertas):
        {json.dumps(respuestas, indent=2, ensure_ascii=False)}
        
        TAREAS:
        1. Sentimiento_Academico: Escala 0 (Muy negativo/Frustrado) a 1 (Muy positivo/Empoderado).
        2. Etiquetas_Tematicas: Lista de 3 temas clave mencionados (ej. "Brecha digital", "Autoestima tecnológica").
        3. Indice_Coherencia: Escala 0 a 1. ¿Qué tan alineado está lo que dice con lo que marcó en los números?
           - 1.0 = Coherencia total.
           - 0.5 = Ambivalente o genérico.
           - 0.0 = Contradicción absoluta (ej. dice ser experto pero marcó scores de nivel 1).
        
        Responde ÚNICAMENTE en formato JSON plano:
        {{
            "Sentimiento_Academico": float,
            "Etiquetas_Tematicas": ["tema1", "tema2", "tema3"],
            "Indice_Coherencia": float,
            "Analisis_Breve": "Explicación de 1 párrafo sobre la coherencia encontrada"
        }}
        """
        return prompt

    def analyze_single_student(self, row: pd.Series) -> pd.Series:
        """Procesa un único estudiante y devuelve la fila con métricas cualitativas."""
        prompt = self._generate_analysis_prompt(row)
        res_row = row.copy()
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text.replace('```json', '').replace('```', '').strip()
            analysis = json.loads(text)
            
            res_row["Sentimiento_Academico"] = analysis.get("Sentimiento_Academico")
            res_row["Indice_Coherencia"] = analysis.get("Indice_Coherencia")
            res_row["Etiquetas_Tematicas"] = ", ".join(analysis.get("Etiquetas_Tematicas", []))
            res_row["Analisis_Cuali"] = analysis.get("Analisis_Breve")
            
            logging.info(f"Análisis STU: {row.get('ID_Estudiante')} | Coherencia: {analysis.get('Indice_Coherencia')}")
            time.sleep(1.5) # Rate limit preventivo
            
        except Exception as e:
            logging.error(f"Error en análisis {row.get('ID_Estudiante')}: {str(e)}")
            res_row["Indice_Coherencia"] = 0.5
            res_row["Analisis_Cuali"] = f"Error: {str(e)}"
            
        return res_row

    def run_hybrid_analysis(self, df_hybrid: pd.DataFrame) -> pd.DataFrame:
        """Procesa el dataset completo (Legacy/Atomic Hybrid)."""
        print(f"-> Iniciando análisis de coherencia híbrida para {len(df_hybrid)} registros...")
        results = []
        for index, row in df_hybrid.iterrows():
            analyzed = self.analyze_single_student(row)
            results.append(analyzed)
            print(f"   [OK] {row.get('ID_Estudiante')} analizado.")
            
        return pd.DataFrame(results)

if __name__ == "__main__":
    # Script de prueba rápida
    pass
