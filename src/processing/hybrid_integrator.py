import pandas as pd
import os

class HybridIntegrator:
    """
    Módulo para la integración y normalización de datos mixtos.
    Permite limpiar el dataset híbrido y marcar inconsistencias para auditoría.
    """

    def __init__(self, threshold=0.6):
        self.threshold = threshold

    def integrate(self, df: pd.DataFrame) -> pd.DataFrame:
        """Centraliza la normalización y el filtrado por coherencia."""
        df = df.copy()
        
        # 1. Normalización de Sentimiento (Tag -> Num)
        if 'Sentimiento_Academico' in df.columns:
            # Asegurar que sea numérico
            df['Sentimiento_Academico'] = pd.to_numeric(df['Sentimiento_Academico'], errors='coerce').fillna(0.5)
            
        # 2. Marcado de Inconsistencia (Solo si hay datos de IA)
        if 'Indice_Coherencia' in df.columns:
            # Validar si hay datos reales o si falló el proceso
            valid_coherence = df['Indice_Coherencia'].notnull().sum()
            if valid_coherence > 0:
                df['Flag_Inconsistencia_IA'] = df['Indice_Coherencia'] < self.threshold
            else:
                df['Flag_Inconsistencia_IA'] = False
        else:
            df['Flag_Inconsistencia_IA'] = False
            
        return df

    def finalize_paper_ready_dataset(self, df: pd.DataFrame, output_path: str) -> pd.DataFrame:
        """Genera el dataset limpio para publicaciones científicas."""
        # Solo eliminar si tenemos certeza de inconsistencia
        if 'Flag_Inconsistencia_IA' in df.columns and df['Flag_Inconsistencia_IA'].any():
            mask_out = df['Flag_Inconsistencia_IA'] == True
            df_final = df[~mask_out].copy()
            print(f"-> Paper-Ready: {mask_out.sum()} registros excluidos por baja coherencia.")
        else:
            df_final = df.copy()
            print("-> Paper-Ready: No se aplicó filtro de coherencia (Data insuficiente o API offline).")
            
        df_final.to_csv(output_path, index=False)
        return df_final
