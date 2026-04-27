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
        self.inverted_items = ['C6', 'T6', 'P5']
        
    def transform_likert_to_numeric(self, df: pd.DataFrame) -> pd.DataFrame:
        """Convierte las cadenas de texto del Likert a números del 1 al 5."""
        df_clean = df.copy()
        
        # Identificar columnas que deberian estar en Likert
        ami_cols = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
        ard_likert_cols = [f'A{i}' for i in range(4, 9)] + [f'L{i}' for i in [1, 3, 4, 5, 6, 7, 8]]
        
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
        # Por ejemplo, si dice tener rendimiento Alto pero tiene 2 o más cursos desaprobados
        if 'A4' in df_clean.columns and 'A2_Desaprobados' in df_clean.columns:
            # Acondicionando un mapeo heurístico:
            mask_mentira = (df_clean['A4'] == 5) & (df_clean['A2_Desaprobados'] == 'En dos o más cursos')
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
