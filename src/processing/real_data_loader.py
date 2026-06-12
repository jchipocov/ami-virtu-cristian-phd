import os
import pandas as pd
import numpy as np

class RealDataLoader:
    """
    Cargador e Ingestador de Datos Reales de Campo para AMI-VIRTU & ARD-VIRTU.
    Carga el archivo Excel de encuestas de campo, aplica exclusiones éticas/metodológicas,
    limpia prefijos numéricos Likert y formatea las columnas al esquema esperado.
    """

    def __init__(self, excel_path: str):
        self.excel_path = excel_path

    def clean_likert_string(self, val) -> str:
        """Limpia los prefijos numéricos de las escalas Likert (ej. '4 = De acuerdo' -> 'De acuerdo')."""
        if pd.isnull(val):
            return "Ni de acuerdo ni en desacuerdo"
        val_str = str(val).strip()
        if "=" in val_str:
            return val_str.split("=", 1)[1].strip()
        return val_str

    def clean_a1(self, val) -> str:
        """Normaliza la respuesta de interrupción de matrícula."""
        if pd.isnull(val):
            return "No"
        v = str(val).strip().lower()
        if v in ['yes', 'sí', 'si', 'y']:
            return 'Sí'
        return 'No'

    def clean_a2(self, val) -> str:
        """Normaliza la respuesta de cursos desaprobados."""
        if pd.isnull(val):
            return "Nunca"
        v = str(val).strip().lower()
        if "nunca" in v or "ningun" in v:
            return "Nunca"
        if "un curso" in v or "uno" in v:
            return "En un Curso"
        if "dos o mas" in v or "dos o más" in v:
            return "En dos o más"
        return "Nunca"

    def clean_a3(self, val) -> str:
        """Normaliza la respuesta de asignaturas retiradas."""
        if pd.isnull(val):
            return "No"
        v = str(val).strip().lower()
        if "no" in v:
            return "No"
        if "una ocasion" in v or "uno" in v:
            return "Sí, en una ocasión"
        if "mas de una" in v or "más de una" in v:
            return "Sí, en más de una ocasión"
        return "No"

    def clean_university(self, val) -> str:
        """Normaliza los nombres largos de universidad a las siglas canónicas."""
        if pd.isnull(val):
            return "UNMSM"
        v = str(val).strip().lower()
        if "marcos" in v or "unmsm" in v:
            return "UNMSM"
        if "ingenieria" in v or "uni" in v:
            return "UNI"
        if "tecnologica" in v or "untels" in v:
            return "UNTELS"
        return "UNMSM"

    def load_and_process(self) -> pd.DataFrame:
        """Carga el Excel real, filtra y mapea los datos al formato del pipeline."""
        if not os.path.exists(self.excel_path):
            raise FileNotFoundError(f"No se encontró el archivo de datos reales en: {self.excel_path}")

        print(f"-> Cargando Excel real desde: {self.excel_path}")
        df_raw = pd.read_excel(self.excel_path, sheet_name="Sheet1")
        print(f"   [OK] Respuestas crudas leídas: {len(df_raw)} registros.")

        # --- 1. Filtros Éticos y Metodológicos ---
        # Filtro 1: Consentimiento informado
        consent_col = df_raw.columns[5]
        df_filtered = df_raw[df_raw[consent_col].str.strip() == "ACEPTO PARTICIPAR"].copy()
        n_consented = len(df_filtered)
        print(f"   [FILTRO] Excluidos {len(df_raw) - n_consented} participantes sin consentimiento informado.")

        # Filtro 2: Actividad virtual en universidad
        virtual_col = df_raw.columns[7]
        df_filtered = df_filtered[df_filtered[virtual_col].str.strip().str.upper().isin(["SÍ", "SI"])].copy()
        n_virtual = len(df_filtered)
        print(f"   [FILTRO] Excluidos {n_consented - n_virtual} participantes sin clases virtuales universitarias.")
        print(f"   [OK] Muestra real válida de campo seleccionada: N={n_virtual}")

        # reset index to avoid alignment mismatch when building df_proc
        df_filtered = df_filtered.reset_index(drop=True)

        # --- 2. Mapeo y Construcción de DataFrame Preprocesado ---
        df_proc = pd.DataFrame()

        # Identificadores y Demográficas (con placeholders para las ausentes)
        df_proc['ID_Estudiante'] = [f'STU_{str(i).zfill(4)}' for i in range(1, len(df_filtered) + 1)]
        df_proc['Universidad'] = df_filtered.iloc[:, 6].apply(self.clean_university)
        df_proc['Edad'] = np.nan
        df_proc['Sexo'] = np.nan
        df_proc['Semestre'] = np.nan

        # Ítems Likert de Alfabetización Mediática (C1-C10, T1-T10, P1-P10)
        # Se encuentran en las columnas del índice 8 al 37
        for i in range(1, 11):
            df_proc[f'C{i}'] = df_filtered.iloc[:, 8 + (i - 1)].apply(self.clean_likert_string)
        for i in range(1, 11):
            df_proc[f'T{i}'] = df_filtered.iloc[:, 18 + (i - 1)].apply(self.clean_likert_string)
        for i in range(1, 11):
            df_proc[f'P{i}'] = df_filtered.iloc[:, 28 + (i - 1)].apply(self.clean_likert_string)

        # Variables de Riesgo Académico (A1_Interrupcion, A2_Desaprobados, A3_Retirados, A4)
        df_proc['A1_Interrupcion'] = df_filtered.iloc[:, 50].apply(self.clean_a1)
        df_proc['A2_Desaprobados'] = df_filtered.iloc[:, 51].apply(self.clean_a2)
        df_proc['A3_Retirados'] = df_filtered.iloc[:, 52].apply(self.clean_a3)
        df_proc['A4'] = df_filtered.iloc[:, 53] # Bajo, Medio, Alto se mantiene directamente

        # Variables de Autoinforme y LMS Likert (A5-A8, L1-L8)
        # Se encuentran en las columnas del índice 54 al 65
        # CORRECCIÓN (Hallazgo 2.2): Se usan los nombres largos para alinear con scorer.py
        df_proc['A5_Dificultad'] = df_filtered.iloc[:, 54].apply(self.clean_likert_string)
        df_proc['A6_Consideracion_Abandono'] = df_filtered.iloc[:, 55].apply(self.clean_likert_string)
        df_proc['A7_Exigencia'] = df_filtered.iloc[:, 56].apply(self.clean_likert_string)
        df_proc['A8_Retrasos'] = df_filtered.iloc[:, 57].apply(self.clean_likert_string)

        df_proc['L1'] = df_filtered.iloc[:, 58].apply(self.clean_likert_string)
        df_proc['L2'] = df_filtered.iloc[:, 59].apply(self.clean_likert_string)
        df_proc['L3'] = df_filtered.iloc[:, 60].apply(self.clean_likert_string)
        df_proc['L4'] = df_filtered.iloc[:, 61].apply(self.clean_likert_string)
        df_proc['L5'] = df_filtered.iloc[:, 62].apply(self.clean_likert_string)
        df_proc['L6'] = df_filtered.iloc[:, 63].apply(self.clean_likert_string)
        df_proc['L7'] = df_filtered.iloc[:, 64].apply(self.clean_likert_string)
        df_proc['L8'] = df_filtered.iloc[:, 65].apply(self.clean_likert_string)

        # Marcadores ausentes en Excel real
        df_proc['Calidad_Percibida'] = np.nan

        # Mapear las 12 columnas cualitativas (del índice 38 al 49)
        # BC1-BC4, BT1-BT4, BP1-BP4
        qual_col_names = [
            'BC1', 'BC2', 'BC3', 'BC4',
            'BT1', 'BT2', 'BT3', 'BT4',
            'BP1', 'BP2', 'BP3', 'BP4'
        ]
        for idx, col_name in enumerate(qual_col_names):
            df_proc[col_name] = df_filtered.iloc[:, 38 + idx].fillna("Sin respuesta.").astype(str)

        return df_proc

if __name__ == "__main__":
    # Prueba rápida unitaria de carga
    loader = RealDataLoader(r"data\raw\Formulario de Investigación Académica Doctoral - BIU (2).xlsx")
    df = loader.load_and_process()
    print("\n[TEST] Primeros 3 registros procesados:")
    print(df[['ID_Estudiante', 'Universidad', 'C1', 'A1_Interrupcion', 'BC1']].head(3))
    print(f"Total registros: {len(df)}")
