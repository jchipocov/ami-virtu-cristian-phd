import os
import pandas as pd
import numpy as np
import google.generativeai as genai
from dotenv import load_dotenv
import json
import time
import logging
from datetime import datetime

class QualitativeGenerator:
    """
    Generador de Respuestas Cualitativas Sintéticas (Sección B).
    Utiliza Gemini AI para crear narrativas coherentes con los puntajes Likert,
    permitiendo la simulación de un estudio de Métodos Mixtos.
    """

    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-flash-latest")
        self.p_incoherence = float(os.getenv("P_INCOHERENCE", 0.1))
        
        if not self.api_key:
            raise ValueError("Error: GEMINI_API_KEY no encontrada en .env")
        
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(self.model_name)
        
        # --- Configuración de Logging Técnico ---
        self.log_file = f"logs/generador_cuali_{datetime.now().strftime('%Y%m%d')}.log"
        os.makedirs("logs", exist_ok=True)
        logging.basicConfig(
            filename=self.log_file,
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            force=True
        )
        
        self.questions = {
            "BC1": "¿Cómo decide si la información que encuentra en internet es confiable para utilizarla en sus trabajos académicos?",
            "BC2": "¿Qué dificultades ha tenido al evaluar la calidad o veracidad de la información digital utilizada en sus cursos virtuales?",
            "BC3": "¿Considera que su capacidad para analizar críticamente la información digital ha influido en su desempeño académico o en su decisión de continuar o abandonar algún curso virtual? Explique.",
            "BC4": "¿En qué situaciones se ha sentido más seguro o más inseguro al evaluar contenidos digitales para sus estudios universitarios?",
            "BT1": "¿Cómo describiría su experiencia utilizando las plataformas virtuales (LMS) y las herramientas digitales empleadas en sus cursos universitarios?",
            "BT2": "¿Ha enfrentado problemas técnicos que hayan afectado su participación o rendimiento en cursos virtuales? ¿Cómo los resolvió?",
            "BT3": "¿Considera que sus habilidades tecnológicas han facilitado o dificultado su permanencia en la modalidad virtual? Explique.",
            "BT4": "¿Qué tipo de apoyo técnico o formativo considera que habría mejorado su experiencia de aprendizaje en cursos virtuales?",
            "BP1": "¿Cómo ha sido su experiencia de participación en foros, trabajos grupales u otras actividades colaborativas en entornos virtuales?",
            "BP2": "¿Se ha sentido acompañado o aislado durante sus cursos virtuales? ¿A qué factores lo atribuye?",
            "BP3": "¿Cree que la interacción con compañeros y docentes influyó en su motivación para continuar estudiando en modalidad virtual? ¿Por qué?",
            "BP4": "¿De qué manera su forma de participar en los entornos virtuales ha impactado en su compromiso con los cursos o con su carrera universitaria?"
        }
        
        self.likert_questions = {
            "C1": "Identifico la fuente o el autor de la información que encuentro en internet.",
            "C2": "Evalúo la credibilidad y veracidad de los contenidos digitales antes de utilizarlos.",
            "C3": "Comparo diferentes fuentes digitales para verificar que la información sea exacta.",
            "C4": "Reconozco si la información en internet tiene algún sesgo o intención comercial o política.",
            "C5": "Distingo entre hechos y opiniones en los contenidos que consumo digitalmente.",
            "C6": "Evito compartir información digital si tengo dudas sobre su veracidad.",
            "C7": "Reflexiono sobre cómo los algoritmos de las redes sociales influyen en la información que recibo.",
            "C8": "Analizo críticamente los mensajes publicitarios o promocionales en entornos virtuales.",
            "C9": "Cuestiono la información que contradice mis conocimientos previos hasta verificar su origen.",
            "C10": "Comprendo las implicaciones éticas y legales del uso de la información digital (ej. derechos de autor).",
            "T1": "Uso eficientemente los motores de búsqueda para encontrar información académica.",
            "T2": "Domino las funciones principales de la plataforma virtual (LMS) utilizada en mis cursos.",
            "T3": "Creo y edito recursos digitales para mis actividades académicas.",
            "T4": "Integro correctamente fuentes digitales y referencias académicas utilizando herramientas tecnológicas.",
            "T5": "Resuelvo problemas técnicos básicos que surgen durante mis actividades académicas virtuales.",
            "T6": "Evito utilizar nuevas herramientas digitales, aunque podrían facilitar mi aprendizaje (Inverso).",
            "T7": "Aplico buenas prácticas de seguridad digital en el uso de plataformas y recursos académicos.",
            "T8": "Utilizo herramientas digitales colaborativas para el trabajo académico en equipo.",
            "T9": "Utilizo funciones de accesibilidad digital cuando las necesito para aprender mejor.",
            "T10": "Selecciono herramientas digitales adecuadas según los objetivos de cada actividad académica.",
            "P1": "Participo activamente en foros u otras actividades colaborativas del aula virtual.",
            "P2": "Respeto las normas de convivencia y netiqueta en los espacios virtuales de aprendizaje.",
            "P3": "Aporto ideas propias y cito adecuadamente materiales digitales de terceros en mis participaciones académicas.",
            "P4": "Interactúo con mis compañeros y docentes a través de medios digitales para resolver dudas académicas.",
            "P5": "Prefiero no participar en actividades grupales virtuales si puedo evitarlas (Inverso).",
            "P6": "Comparto recursos o información digital que considero útil para el aprendizaje de mis compañeros.",
            "P7": "Colaboro en la creación de contenidos digitales conjuntos (ej. documentos compartidos).",
            "P8": "Expreso mis opiniones de manera clara y fundamentada en los espacios virtuales de comunicación.",
            "P9": "Utilizo las redes sociales u otras plataformas digitales con fines de aprendizaje y formación.",
            "P10": "Participo en comunidades académicas digitales relacionadas con mis estudios."
        }

    def _generate_prompt(self, scores: dict, force_incoherent: bool = False):
        """Construye el prompt para Gemini basado en el perfil del estudiante."""
        perfil = (
            f"- Dimensión Crítica: {scores['Score_Critico']:.1f}/5\n"
            f"- Dimensión Técnica: {scores['Score_Tecnico']:.1f}/5\n"
            f"- Dimensión Participativa: {scores['Score_Participativo']:.1f}/5\n"
            f"- Riesgo de Deserción: {'ALTO' if scores['Riesgo_Total'] == 1 else 'BAJO'}"
        )
        
        instruccion_coherencia = (
            "Tus respuestas DEBEN SER COHERENTES con este perfil numérico." 
            if not force_incoherent else 
            "Tus respuestas DEBEN CONTRADECIR este perfil numérico de forma sutil pero detectable (ej. si tiene score bajo, di que te sientes muy experto)."
        )

        prompt = f"""
        Actúa como un estudiante universitario peruano respondiendo una encuesta de Alfabetización Mediática e Informacional (AMI).
        
        PERFIL DEL ESTUDIANTE (en escala Likert 1-5):
        {perfil}
        
        {instruccion_coherencia}
        
        Genera respuestas breves (2-3 líneas por pregunta) para las siguientes 12 preguntas de la 'Sección B'.
        Responde en formato JSON puro, donde las llaves sean los códigos de las preguntas (BC1, BC2, ..., BP4).
        Usa lenguaje natural, a veces un poco informal o académico según el nivel, pero siempre realista.
        
        Preguntas:
        {json.dumps(self.questions, indent=2, ensure_ascii=False)}
        """
        return prompt

    def _log_quality_audit(self, student_row: pd.Series, answers: dict, forced: bool):
        """Genera un archivo Markdown para auditoría humana de calidad."""
        log_dir = "logs"
        os.makedirs(log_dir, exist_ok=True)
        log_path = os.path.join(log_dir, "auditoria_cualitativa.md")
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"\n## Auditoría Estudiante: {student_row['ID_Estudiante']} {'[INCOHERENCIA FORZADA]' if forced else ''}\n")
            f.write(f"**Perfil Cuanti (Dimensiones):** Crit={student_row['Score_Critico']:.1f}, Tec={student_row['Score_Tecnico']:.1f}, Part={student_row['Score_Participativo']:.1f}\n")
            f.write(f"**Riesgo:** {'ALTO' if student_row['Riesgo_Total'] == 1 else 'BAJO'}\n\n")
            
            # Nueva sección: Detalle de Ítems Likert
            f.write("### Sección A: Puntajes Likert (Detalle)\n")
            f.write("| Código | Ítem / Pregunta | Puntaje (1-5) |\n")
            f.write("|:---:|:---|:---:|\n")
            
            for code, q_text in self.likert_questions.items():
                score = int(student_row[code])
                f.write(f"| {code} | {q_text} | **{score}** |\n")
            
            f.write("\n### Sección B: Respuestas Abiertas\n")
            f.write("| Código | Pregunta | Respuesta Gemini |\n")
            f.write("|:---:|:---|:---|\n")
            for q_code, resp in answers.items():
                q_text = self.questions.get(q_code, "N/A")
                f.write(f"| {q_code} | {q_text} | {resp} |\n")
            f.write("\n---\n")

    def generate_qualitative_data(self, df_scored: pd.DataFrame, limit: int = None) -> pd.DataFrame:
        """Agrega las 12 columnas cualitativas al DataFrame utilizando Gemini."""
        df = df_scored.copy()
        if limit:
            df = df.head(limit)
            
        print(f"-> Iniciando generación cualitativa para {len(df)} estudiantes...")
        
        # Inicializar columnas con strings vacíos
        for q_code in self.questions.keys():
            df[q_code] = ""
        
        for index, row in df.iterrows():
            force_incoherent = np.random.random() < self.p_incoherence
            prompt = self._generate_prompt(row, force_incoherent)
            
            try:
                response = self.model.generate_content(prompt)
                # Extraer JSON de la respuesta (manejar posibles markdowns de Gemini)
                text = response.text.replace('```json', '').replace('```', '').strip()
                answers = json.loads(text)
                
                for q_code, answer in answers.items():
                    if q_code in df.columns:
                        df.at[index, q_code] = answer
                
                print(f"   [OK] Estudiante {row['ID_Estudiante']} procesado {'(Incoherencia Inyectada)' if force_incoherent else ''}")
                logging.info(f"Estudiante {row['ID_Estudiante']} procesado exitosamente {'(Incoherencia)' if force_incoherent else ''}")
                
                # --- LOG DE AUDITORÍA DE CALIDAD ---
                self._log_quality_audit(row, answers, force_incoherent)
                
                # Rate limit safety (free tier usually has limits)
                time.sleep(2) 
                
            except Exception as e:
                print(f"   [ERROR] Estudiante {row['ID_Estudiante']}: {str(e)}")
                logging.error(f"Error procesando {row['ID_Estudiante']}: {str(e)}")
                # Llenar con placeholders en caso de fallo para no romper el pipeline
                for q_code in self.questions.keys():
                    df.at[index, q_code] = "Sin respuesta por error técnico."
        
        return df

if __name__ == "__main__":
    # Ajustar path para ejecución directa
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

    # Prueba rápida desacoplada
    from src.simulation.data_simulator import DataSimulator
    from src.processing.cleaner import DataCleaner
    from src.processing.scorer import Scorer
    
    sim = DataSimulator(num_records=5) # Solo 5 para probar
    df_raw = sim.generate_dataset()
    cleaner = DataCleaner()
    scorer = Scorer()
    df_p = scorer.score_process(cleaner.clean_process(df_raw))
    
    gen = QualitativeGenerator()
    df_final = gen.generate_qualitative_data(df_p)
    print("\nDataset Híbrido Final (Muestra):")
    print(df_final[['ID_Estudiante', 'BC1', 'BT1', 'BP1']].head())
    
    # Guardar muestra
    os.makedirs('data/raw', exist_ok=True)
    df_final.to_csv('data/raw/synthetic_hybrid_data.csv', index=False, encoding='utf-8-sig')
    print("-> Dataset guardado en data/raw/synthetic_hybrid_data.csv")
