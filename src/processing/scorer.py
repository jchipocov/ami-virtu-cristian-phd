import pandas as pd
import numpy as np

class Scorer:
    """
    Clase encargada de condensar las dimensionalidades.
    Calcula los promedios globales/dimensionales de AMI y asigna el target (Riesgo_Total)
    basado en las reglas de Ground Truth / Fallback Autoreportado.
    """

    def compute_ami_scores(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calcula el promedio de las tres dimensiones AMI y el Global."""
        df_scored = df.copy()
        
        c_cols = [f'C{i}' for i in range(1, 11)]
        t_cols = [f'T{i}' for i in range(1, 11)]
        p_cols = [f'P{i}' for i in range(1, 11)]
        
        if all(col in df.columns for col in c_cols + t_cols + p_cols):
            df_scored['Score_Critico'] = df_scored[c_cols].mean(axis=1)
            df_scored['Score_Tecnico'] = df_scored[t_cols].mean(axis=1)
            df_scored['Score_Participativo'] = df_scored[p_cols].mean(axis=1)
            
            all_ami_cols = c_cols + t_cols + p_cols
            df_scored['Score_AMI_Global'] = df_scored[all_ami_cols].mean(axis=1)
            
        return df_scored

    def compute_risk_target(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Aplica la estrategia 'Fallback' computando Riesgo=1 si se cumple la compuerta OR.
        Si hubiera data institucional fuerte, aqui se le daria prioridad.
        """
        df_scored = df.copy()
        df_scored['Riesgo_Total'] = 0  # Inicializar en 0 (No Riesgo)
        
        # --- [REGLAS ACADÉMICAS (A1-A8)] ---
        cond_a1 = df_scored.get('A1_Interrupcion', pd.Series(index=df.index)) == 'Sí'
        cond_a2 = df_scored.get('A2_Desaprobados', pd.Series(index=df.index)) == 'En dos o más cursos'
        cond_a3 = df_scored.get('A3_Retirados', pd.Series("", index=df.index)).astype(str).str.contains('Sí', na=False)
        cond_a4 = df_scored.get('A4_Rendimiento', pd.Series(index=df.index)) == 'Bajo'
        
        # Items Likert (A5-A8): 4 o 5 indican riesgo
        likert_a = ['A5_Dificultad', 'A6_Consideracion_Abandono', 'A7_Exigencia', 'A8_Retrasos']
        cond_likert_a = pd.Series([False] * len(df), index=df.index)
        for col in likert_a:
            if col in df_scored.columns:
                # Asegurar que sea numérico para la comparación
                cond_likert_a |= pd.to_numeric(df_scored[col], errors='coerce') >= 4

        # --- [REGLAS DOCUMENTALES/LABORALES (L1-L8)] ---
        actual_l_cols = [col for col in df_scored.columns if col.startswith('L')]
        cond_likert_l = pd.Series([False] * len(df), index=df.index)
        for col in actual_l_cols:
            if col != 'Riesgo_Total':
                cond_likert_l |= pd.to_numeric(df_scored[col], errors='coerce') >= 4
        
        mask_riesgo = cond_a1 | cond_a2 | cond_a3 | cond_a4 | cond_likert_a | cond_likert_l
        df_scored.loc[mask_riesgo, 'Riesgo_Total'] = 1
        
        return df_scored

    def score_process(self, df_clean: pd.DataFrame) -> pd.DataFrame:
        """Ejecuta el pipeline de scoring completo."""
        df = df_clean.copy()
        df = self.compute_ami_scores(df)
        df = self.compute_risk_target(df)
        return df
