import pandas as pd
import numpy as np

class DataCleaner:
    """
    Clase encargada de limpiar y preprocesar el DataFrame crudo.
    Transforma texto a numérico, invierte escalas negativas,
    e implementa detectores de anomalías (Ocultamiento/Deseabilidad Social).
    """

    def __init__(self):
        self.likert_map = {
            "Totalmente en desacuerdo": 1,
            "En desacuerdo": 2,
            "Ni de acuerdo ni en desacuerdo": 3,
            "De acuerdo": 4,
            "Totalmente de acuerdo": 5
        }
        # CORRECCIÓN (Hallazgo 3.1): T6 y P5 son ítems POSITIVOS en la encuesta real.
        # T6 = "Manejo plataformas virtuales con facilidad" (autoeficacia positiva)
        # P5 = "Contribuyo a la solución de problemas en equipo" (colaboración positiva)
        # Solo C6 es genuinamente negativo (trampa de aquiescencia).
        self.inverted_items = ['C6']
        
    def transform_likert_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convierte las cadenas de texto del Likert a números del 1 al 5."""
        df_clean = df.copy()
        
        # Identificar columnas que deberian estar en Likert
        ami_cols = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
        # CORRECCIÓN (Hallazgo 2.1): A4 se excluye porque contiene texto cualitativo
        # ('Alto', 'Medio', 'Bajo') que NO es una escala Likert de acuerdo.
        # El transform_likert_to_numeric lo convertiría a 100% NaN si se incluye.
        # CORRECCIÓN (Hallazgo 2.2 + Adicional 1): Se usan nombres largos para A5-A8
        # para alinear con real_data_loader.py post-corrección.
        # CORRECCIÓN (Hallazgo 2.3): Se incluye L2 (inactividad en aula virtual).
        ard_likert_cols = [
            'A5_Dificultad', 'A6_Consideracion_Abandono', 'A7_Exigencia', 'A8_Retrasos'
        ] + [f'L{i}' for i in range(1, 9)]
        
        target_cols = ami_cols + ard_likert_cols + ['Calidad_Percibida']
        
        for col in target_cols:
            if col in df_clean.columns:
                # Reemplazar usando el mapa y forzar a numérico (maneja texto y números mezclados)
                df_clean[col] = df_clean[col].replace(self.likert_map)
                df_clean[col] = pd.to_numeric(df_clean[col], errors='coerce')
                
        return df_clean

    def reverse_negative_items(self, df: pd.DataFrame) -> pd.DataFrame:
        """Aplica la regla '6 - Valor' a los ítems trampa para alinear la dirección semántica."""
        df_clean = df.copy()
        for col in self.inverted_items:
            if col in df_clean.columns:
                # Solo invierte si el valor no es nulo
                df_clean[col] = df_clean[col].apply(lambda x: 6 - x if pd.notnull(x) else x)
        return df_clean

    def anomaly_detector(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Detector de Ocultamiento y Deseabilidad Social.
        Crea la columna 'Flag_Inconsistencia' si detecta un comportamiento anómalo.
        """
        df_clean = df.copy()
        df_clean['Flag_Inconsistencia'] = False
        
        # 1. Detector de Flatliners (Aquiescencia Absoluta)
        # Revisa si respondió "5" en todos los ítems de AMI (varianza 0 antes de invertir)
        ami_cols = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
        if all(col in df_clean.columns for col in ami_cols):
            # Asegurar que sean numericos antes de calcular varianza
            subset = df_clean[ami_cols].apply(pd.to_numeric, errors='coerce')
            variances = subset.var(axis=1)
            df_clean.loc[variances == 0, 'Flag_Inconsistencia'] = True
            
        # 2. Detector Semántico (Ocultamiento de Riesgo)
        # Condición: Rendimiento 'Alto' pero con 2 o más cursos desaprobados.
        # CORRECCIÓN (Hallazgo 3.2): A4 conserva texto cualitativo ('Alto','Medio','Bajo')
        # porque se excluyó de ard_likert_cols. A2_Desaprobados normalizado por
        # RealDataLoader contiene 'En dos o más' (sin la palabra 'cursos').
        if 'A4' in df_clean.columns and 'A2_Desaprobados' in df_clean.columns:
            mask_mentira = (
                (df_clean['A4'].astype(str).str.strip().str.lower() == 'alto') &
                (df_clean['A2_Desaprobados'].astype(str).str.strip() == 'En dos o más')
            )
            df_clean.loc[mask_mentira, 'Flag_Inconsistencia'] = True

        return df_clean

    def pii_filter(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Elimina columnas que puedan contener información sensible (PII).
        Asegura que el análisis sea anónimo por diseño.
        """
        pii_cols = [
            'DNI', 'Nombre', 'Apellidos', 'Email', 'Correo', 
            'Telefono', 'Celular', 'Direccion', 'ID_Matricula',
            'Codigo_Alumno', 'UID'
        ]
        to_drop = [c for c in pii_cols if c in df.columns]
        if to_drop:
            df = df.drop(columns=to_drop)
            print(f"-> [SECURITY] Columnas sensibles eliminadas: {to_drop}")
        return df

    def clean_process(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        """Ejecuta el pipeline de limpieza completo."""
        df = df_raw.copy()
        df = self.pii_filter(df) # Filtro de privacidad primero
        df = self.transform_likert_to_numeric(df)
        df = self.anomaly_detector(df) # Anomalias basadas en las raw variables numericas
        df = self.reverse_negative_items(df) # Para el calculo limpio
        
        return df
