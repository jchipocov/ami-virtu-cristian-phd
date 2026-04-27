import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

class ReportGenerator:
    def __init__(self, output_dir: str):
        print(f"DEBUG: ReportGenerator ACTIVE at {output_dir}")
        self.output_dir = output_dir
        os.makedirs(self.output_dir, exist_ok=True)
        self.tables_dir = os.path.join(self.output_dir, "academic_tables")
        self.reports_dir = os.path.join(self.output_dir, "reports")
        os.makedirs(self.tables_dir, exist_ok=True)
        os.makedirs(self.reports_dir, exist_ok=True)
        sns.set_theme(style="whitegrid", palette="muted")

    def save_raw_table(self, df: pd.DataFrame, filename: str):
        if df is not None:
            df.to_csv(os.path.join(self.tables_dir, filename + ".csv"), index=False)

    def plot_correlation_matrix(self, df: pd.DataFrame, filename="01_matriz_correlacion.png"):
        plt.figure(figsize=(10, 8))
        cols = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Sentimiento_Academico', 'Riesgo_Total']
        exist_cols = [c for c in cols if c in df.columns]
        corr = df[exist_cols].corr(method='spearman')
        mask = np.triu(np.ones_like(corr, dtype=bool))
        sns.heatmap(corr, mask=mask, annot=True, cmap="Spectral", vmin=-1, vmax=1, fmt=".2f")
        plt.title("Triangulación: Cuanti x Cuali x Riesgo", weight="bold")
        plt.tight_layout()
        plt.savefig(os.path.join(self.output_dir, filename), dpi=300)
        plt.close()

    def generate_narrative_reports(self, reliability_df, contrasts, logit_results, interaction_res, xai_features=None, cluster_profiles=None, triangulation_res=None):
        print(f"DEBUG: Generando reportes narrativos en {self.reports_dir}")
        
        # 1. Triangulación Mixta
        tri_path = os.path.join(self.reports_dir, "04_triangulacion_mixta_FINAL.md")
        with open(tri_path, "w", encoding="utf-8") as f:
            f.write("# [FASE 11] Reporte de Triangulación\n\n")
            if triangulation_res:
                f.write(f"Correlation: {triangulation_res.get('correlation_r', 0):.3f}\n")
                f.write(f"Interpretation: {triangulation_res.get('interpretation', 'N/A')}\n")
        
        # 2. Reporte de Fiabilidad
        with open(os.path.join(self.reports_dir, "01_fiabilidad_v2.md"), "w", encoding="utf-8") as f:
            f.write("# Fiabilidad Psicométrica Profesional\n\n")
            if reliability_df is not None:
                f.write(reliability_df.to_markdown())

    def generate_generative_synthesis(self, df_clustered: pd.DataFrame, cluster_profiles: dict):
        print(f"DEBUG: Generando síntesis generativa (Modo Resiliente)")
        report_path = os.path.join(self.reports_dir, "06_sintesis_ejecutiva_FINAL.md")
        with open(report_path, "w", encoding="utf-8") as f:
            f.write("# Síntesis Ejecutiva Doctoral\n\n")
            f.write("> Generado en modo resiliente (Citas + IA si hay cuota).\n\n")
            # Citas
            for cid in [0, 1, 2]:
                f.write(f"## Grupo {cid}\n")
                sample = df_clustered[df_clustered['Cluster_KMeans'] == cid]['BC1'].dropna().head(2).tolist()
                for q in sample: f.write(f"- *\"{q}\"*\n")
                f.write("\n")

    def generate_all_reports(self, df_clustered, logit_results=None, reliability_df=None, contrasts=None, interaction_res=None, xai_features=None, cluster_profiles=None, triangulation_res=None):
        self.plot_correlation_matrix(df_clustered)
        self.generate_narrative_reports(reliability_df, contrasts, logit_results, interaction_res, xai_features, cluster_profiles, triangulation_res)
        self.generate_generative_synthesis(df_clustered, cluster_profiles)
        print(f"SUCCESS: Reportes finales generados.")
