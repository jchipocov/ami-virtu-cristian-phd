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
        Mantiene la compatibilidad con modelos predictivos binarios y añade desglose dimensional.
        """
        df_scored = df.copy()
        df_scored['Riesgo_Total'] = 0
        
        # Mapeos numéricos para el cálculo dimensional (Objetivos 2 y 3)
        map_a1 = {'Sí': 5, 'No': 1}
        map_a2 = {'En dos o más cursos': 5, 'En uno': 3, 'Ninguno': 1}
        map_a4 = {'Bajo': 5, 'Medio': 3, 'Alto': 1}
        
        # 1. Reglas Académicas (A1-A8)
        if 'A1_Interrupcion' in df_scored.columns:
            df_scored['A1_num'] = df_scored['A1_Interrupcion'].map(map_a1).fillna(1)
        else:
            df_scored['A1_num'] = 1
            
        if 'A2_Desaprobados' in df_scored.columns:
            df_scored['A2_num'] = df_scored['A2_Desaprobados'].map(map_a2).fillna(1)
        else:
            df_scored['A2_num'] = 1
            
        if 'A3_Retirados' in df_scored.columns:
            df_scored['A3_num'] = df_scored['A3_Retirados'].astype(str).apply(lambda x: 5 if 'Sí' in x else 1)
        else:
            df_scored['A3_num'] = 1
            
        if 'A4_Rendimiento' in df_scored.columns:
            df_scored['A4_num'] = df_scored['A4_Rendimiento'].map(map_a4).fillna(1)
        else:
            df_scored['A4_num'] = 1
        
        likert_a = ['A5_Dificultad', 'A6_Consideracion_Abandono', 'A7_Exigencia', 'A8_Retrasos']
        for col in likert_a:
            if col in df_scored.columns:
                df_scored[f'{col}_num'] = pd.to_numeric(df_scored[col], errors='coerce').fillna(3)
            else:
                df_scored[f'{col}_num'] = 3
        
        # 2. Reglas LMS (L1-L8)
        l_cols = [f'L{i}' for i in range(1, 9)]
        for col in l_cols:
            if col in df_scored.columns:
                df_scored[f'{col}_num'] = pd.to_numeric(df_scored[col], errors='coerce').fillna(3)
            else:
                df_scored[f'{col}_num'] = 3
        
        # 3. Cálculo de Dimensiones de Riesgo (Desglose PhD)
        a_num_cols = ['A1_num', 'A2_num', 'A3_num', 'A4_num'] + [f'{c}_num' for c in likert_a]
        l_num_cols = [f'L{i}_num' for i in range(1, 9)]
        
        df_scored['Score_Riesgo_Academico'] = df_scored[a_num_cols].mean(axis=1)
        df_scored['Score_Riesgo_LMS'] = df_scored[l_num_cols].mean(axis=1)
        # Continuidad: Síntesis de historia (A1) e intención (A6)
        df_scored['Score_Riesgo_Continuidad'] = df_scored[['A1_num', 'A6_Consideracion_Abandono_num']].mean(axis=1)
        
        # 4. Target Binario (OR Gate - Umbral conservador 3.5)
        mask_riesgo = (df_scored['Score_Riesgo_Academico'] >= 3.5) | (df_scored['Score_Riesgo_LMS'] >= 3.5)
        df_scored.loc[mask_riesgo, 'Riesgo_Total'] = 1
        
        return df_scored

    def score_process(self, df_clean: pd.DataFrame) -> pd.DataFrame:
        """Ejecuta el pipeline de scoring completo."""
        df = df_clean.copy()
        df = self.compute_ami_scores(df)
        df = self.compute_risk_target(df)
        return df
