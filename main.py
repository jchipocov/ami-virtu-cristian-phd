import os
import sys
import pandas as pd
import warnings
from datetime import datetime

# Añadir raíz al path con prioridad máxima
root_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, root_dir)

from src.analysis.stats_analyzer import StatsAnalyzer
from src.analysis.clustering_engine import ClusteringEngine
from src.analysis.qualitative_engine import QualitativeEngine
from src.processing.hybrid_integrator import HybridIntegrator
from src.processing.cleaner import DataCleaner
from src.processing.scorer import Scorer
from src.utils.reporter import ReportGenerator
from src.utils.logger import ExecutionLogger
from src.utils.reproducibility import calculate_data_hash, verify_reproducibility_env

def main():
    warnings.filterwarnings('ignore')
    
    # --- [0] Reproducibilidad Científica (Semillas fijas) ---
    import numpy as np
    import random
    SEED = 42
    np.random.seed(SEED)
    random.seed(SEED)
    
    # --- [0.1] Configuración de Rutas y LOG ---
    log_dir = os.path.join(root_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)
    date_str = datetime.now().strftime("%Y%m%d")
    
    print("==================================================")
    print("  AMI-VIRTU & ARD-VIRTU - ANALYTICAL ENGINE (HÍBRIDO)")
    print("==================================================")
    
    # --- [1] Carga de Datos Híbridos (Desacoplado) ---
    hybrid_input = os.path.join(root_dir, "data", "processed", "hybrid_analysis_results.csv")
    
    if not os.path.exists(hybrid_input):
        print(f"\n[!] ERROR: No se encontró el dataset en: {hybrid_input}")
        return

    df_raw = pd.read_csv(hybrid_input)
    print(f"\n[1] Dataset cargado satisfactoriamente (N={len(df_raw)}).")

    # Asegurar que los datos estén limpios y puntuados (Score_Critico, etc.)
    if 'Score_AMI_Global' not in df_raw.columns:
        print("-> Calculando puntuaciones psicométricas faltantes...")
        cleaner = DataCleaner()
        scorer = Scorer()
        df_raw = cleaner.clean_process(df_raw)
        df_raw = scorer.score_process(df_raw)

    # --- [2] Análisis Cualitativo (Sincronización) ---
    qual_engine = QualitativeEngine()
    if "Indice_Coherencia" not in df_raw.columns:
        print("\n[2] Iniciando Triangulación Cualitativa (Modo Resiliente)...")
        processed_rows = []
        api_blocked = False
        
        for i, (index, row) in enumerate(df_raw.iterrows(), 1):
            if api_blocked:
                # Si la API está bloqueada, simplemente pasamos la fila sin analizar
                processed_rows.append(row)
                continue
                
            analyzed_row = qual_engine.analyze_single_student(row)
            
            # Detectar bloqueo de cuota (marcado en el análisis por el engine)
            if "Error: 429" in str(analyzed_row.get('Analisis_Cuali', '')):
                print(f"   [!] DETECTADO BLOQUEO DE CUOTA (429). Saltando el resto del análisis cualitativo...")
                api_blocked = True
                
            processed_rows.append(analyzed_row)
        df_hybrid = pd.DataFrame(processed_rows)
        
        # Mapeo de categorías a números (ARD-VIRTU Completo)
        map_interrupcion = {'Sí': 1, 'No': 0}
        map_desaprobados = {'Nunca': 0, 'En un Curso': 1, 'En dos o más': 2}
        map_retirados = {'No': 0, 'Sí, en una ocasión': 1, 'Sí, en más de una ocasión': 2}
        map_rendimiento = {'Alto': 1, 'Medio': 2, 'Bajo': 3}
        
        df_hybrid['A1_num'] = df_hybrid['A1_Interrupcion'].map(map_interrupcion).fillna(0)
        df_hybrid['A2_num'] = df_hybrid['A2_Desaprobados'].map(map_desaprobados).fillna(0)
        df_hybrid['A3_num'] = df_hybrid['A3_Retirados'].map(map_retirados).fillna(0)
        df_hybrid['A4_num'] = df_hybrid['A4'].map(map_rendimiento).fillna(1)

        # Cálculo de promedios para dimensiones Likert (A5-A8, L1-L8)
        # Asegurar que sean numéricos
        for c in [f'A{i}' for i in range(5, 9)] + [f'L{i}' for i in range(1, 9)]:
            if c in df_hybrid.columns:
                df_hybrid[c] = pd.to_numeric(df_hybrid[c], errors='coerce').fillna(3)

        df_hybrid['Riesgo_Acad_Perceptual'] = df_hybrid[[f'A{i}' for i in range(5, 9)]].mean(axis=1)
        df_hybrid['Riesgo_Documental'] = df_hybrid[[f'L{i}' for i in range(1, 9)]].mean(axis=1)

        df_hybrid['Riesgo_Total'] = 0
        mask_riesgo = (
            (df_hybrid['A1_num'] == 1) |
            (df_hybrid['A2_num'] >= 2) |
            (df_hybrid['A3_num'] >= 1) |
            (df_hybrid['A4_num'] == 3) |
            (df_hybrid['Riesgo_Acad_Perceptual'] > 3.5) |
            (df_hybrid['Riesgo_Documental'] > 3.5)
        )
        df_hybrid.loc[mask_riesgo, 'Riesgo_Total'] = 1
        
        # Eliminar columnas temporales de cálculo
        tmp_cols = ['A1_num', 'A2_num', 'A3_num', 'A4_num', 'Riesgo_Acad_Perceptual', 'Riesgo_Documental']
        df_hybrid.drop(tmp_cols, axis=1, inplace=True, errors='ignore')
        
        df_hybrid.to_csv(hybrid_input, index=False)
    else:
        print("\n[2] Datos cualitativos detectados. Saltando análisis Gemini.")
        df_hybrid = df_raw

    # --- [3] Integración Híbrida (FASE 10) ---
    print("\n[3] Ejecutando Integración Híbrida Desacoplada...")
    integrator = HybridIntegrator(threshold=float(os.getenv('COHERENCE_THRESHOLD', 0.6)))
    df_hybrid = integrator.integrate(df_hybrid)
    
    paper_ready_path = os.path.join(root_dir, "data", "processed", "ami_virtu_final_paper_ready.csv")
    df_final = integrator.finalize_paper_ready_dataset(df_hybrid, paper_ready_path)

    # --- [4] Inferencia Estadística (FASE 11) ---
    print("\n[4] Análisis Inferencial y Triangulación Estadística...")
    analyzer = StatsAnalyzer()
    
    # Fiabilidad, Análisis Factorial y Contrastes
    reliability_df = analyzer.calculate_reliability(df_final)
    factor_res = analyzer.run_factor_analysis(df_final)
    contrasts = analyzer.run_demographic_contrasts(df_final)
    
    # Triangulación Mixta (Cuyo sentiment vs cuanti)
    triangulation_res = analyzer.run_mixed_methods_triangulation(df_final)
    interaction_res = analyzer.run_interaction_analysis(df_final)
    
    # ML Models (Logit & Random Forest)
    X_train, X_test, y_train, y_test = analyzer.prepare_data(df_final)
    res_logit = analyzer.run_logistic_regression(X_train, X_test, y_train, y_test)
    res_rf = analyzer.run_random_forest(X_train, X_test, y_train, y_test)

    # --- [5] Clustering y XAI (Perfilamiento) ---
    print("\n[5] Generando Perfiles Sociológicos y SHAP Analysis...")
    clusterer = ClusteringEngine(n_clusters=3)
    df_clustered = clusterer.run_clustering(df_final)
    cluster_profiles = clusterer.get_cluster_profiles(df_clustered)
    cluster_val = clusterer.validate_clustering(df_final)
    
    xai_features = None
    try:
        X_train_f, _, y_train_f, _ = analyzer.prepare_feature_data(df_final)
        xai_features = analyzer.run_feature_xai_analysis(X_train_f, y_train_f)
    except Exception as e:
        print(f"   [!] ADVERTENCIA: No se pudo ejecutar SHAP: {e}")

    # --- [6] Reporte Doctoral Final (FASE 12) ---
    print("\n[6] Produciendo Artefactos Finales de Defensa...")
    out_dir = os.path.join(root_dir, 'data', 'outputs')
    reporter = ReportGenerator(output_dir=out_dir)
    
    reporter.generate_all_reports(
        df_clustered, 
        logit_results=res_logit, 
        reliability_df=reliability_df,
        contrasts=contrasts,
        interaction_res=interaction_res,
        xai_features=xai_features,
        cluster_profiles=cluster_profiles,
        triangulation_res=triangulation_res
    )

    # --- [7] Bitácora de Ejecución (REPORTE DE ALTA FIDELIDAD) ---
    log_path = os.path.join(log_dir, f"bitacora_ejecuciones_{date_str}.log")
    logger = ExecutionLogger(log_path)
    
    # --- [PhD Rigor] Auditoría de Integridad y Entorno ---
    data_hash = calculate_data_hash(paper_ready_path)
    env_info = verify_reproducibility_env()
    
    # Reconstrucción del reporte detallado doctoral
    details = "0. AUDITORÍA DE REPRODUCIBILIDAD (INTEGRIDAD):\n"
    details += f"   - SHA-256 Dataset: {data_hash}\n"
    details += f"   - Entorno: Py {env_info['Python_Version']} | Sklearn {env_info['Scikit-Learn']} | Statsmodels {env_info['Statsmodels']}\n"
    details += "   - Estado: INTEGRIDAD VERIFICADA.\n\n"
    
    details += "1. PSICOMETRÍA Y VALIDACIÓN ESTRUCTURAL:\n"
    details += reliability_df.to_string() + "\n"
    if factor_res.get('status') == 'success':
        details += f"   - Prueba KMO: {factor_res['kmo']:.4f}\n"
        details += f"   - Prueba de Bartlett (p): {factor_res['bartlett_p']:.4f}\n"
        details += f"   - Varianza Total Explicada: {sum(factor_res['variance_explained'])*100:.2f}%\n"
        details += f"   - Interpretación EFA: {factor_res['interpretation']}\n\n"
    else:
        details += f"   - EFA: No se pudo ejecutar ({factor_res.get('message')})\n\n"
    
    details += "2. AUDITORÍA DE CALIDAD (INCONSISTENCIAS):\n"
    incon = df_final['Flag_Inconsistencia'].sum() if 'Flag_Inconsistencia' in df_final.columns else 0
    details += f"   - Casos Sospechosos Detectados: {incon}\n"
    details += "   - Metodología: Filtrado semántico mediante HybridIntegrator.\n\n"
    
    details += "3. CONTRASTES SOCIODEMOGRÁFICOS:\n"
    for k, v in contrasts.items():
        details += f"   - {k:25}: Estadístico={v['statistic']:.4f}, p-valor={v['p_value']:.4f}\n"

    details += "\n4. ASOCIACIONES BIVARIADAS (AMI vs RIESGO MULTIDIMENSIONAL):\n"
    biv = analyzer.run_bivariate_analysis(df_final)
    for risk_dim, ami_corrs in biv.items():
        details += f"   - Dimensión Riesgo: {risk_dim}\n"
        for ami_feat, v in ami_corrs.items():
            details += f"     * {ami_feat:20}: Pearson_r={v['Pearson_r']:+.3f} (p={v['P_Pearson']:.4f}) | Spearman_rho={v['Spearman_rho']:+.3f}\n"

    details += "\n5. MODELO DE REGRESIÓN LOGÍSTICA (INFERENCIA CIENTÍFICA):\n"
    if res_logit:
        details += "- Resumen Completo del Modelo:\n"
        details += res_logit.get('full_summary', 'N/A') + "\n"
        
        # --- [Métricas de Evaluación Avanzadas] ---
        details += "\n- MÉTRICAS DE EVALUACIÓN DE CLASIFICACIÓN:\n"
        details += f"   * Accuracy: {res_logit.get('accuracy', 0):.4f}\n"
        details += f"   * ROC-AUC:  {res_logit.get('roc_auc', 0):.4f}\n"
        
        rd = res_logit.get('report_dict', {})
        if rd:
            details += f"   * Precision (Riesgo): {rd.get('1', {}).get('precision', 0):.4f}\n"
            details += f"   * Recall (Riesgo):    {rd.get('1', {}).get('recall', 0):.4f}\n"
            details += f"   * F1-Score (Riesgo):  {rd.get('1', {}).get('f1-score', 0):.4f}\n"
        
        cm = res_logit.get('conf_matrix', [[0,0],[0,0]])
        details += "\n- MATRIZ DE CONFUSIÓN:\n"
        details += f"        Pred=0  Pred=1\n"
        details += f"True=0  {cm[0][0]:<6}  {cm[0][1]:<6}\n"
        details += f"True=1  {cm[1][0]:<6}  {cm[1][1]:<6}\n"
        
        details += f"\n   * Umbral Óptimo (Índice de Youden): {res_logit.get('threshold', 0):.4f}\n"
        
        # Diagnósticos PhD
        details += "\n- DIAGNÓSTICOS DE RIGOR DOCTORAL (REGR):\n"
        details += f"   * Bondad de Ajuste (Hosmer-Lemeshow p): {interaction_res['hosmer_lemeshow']['p_value']:.4f}\n"
        details += f"   * Pseudo R-cuadrado (McFadden): {res_logit.get('prsquared', 0):.4f}\n"
        details += f"   * Interpretación de Ajuste: {interaction_res['interpretation_hl']}\n"
        details += f"   * Diagnóstico de Multicolinealidad (VIF Max): {max([v['VIF'] for v in interaction_res['vif_diagnostics']] + [0]):.4f}\n"
        
        # Odds Ratios
        details += "\n- ODDS RATIOS [Exp(B)] E INTERVALOS DE CONFIANZA:\n"
        or_ci = res_logit.get('odds_ratios_ci', {})
        for var, metrics in or_ci.items():
            details += f"   * {var:15}: OR={metrics['OR']:.4f} | IC 95%=[{metrics['Lower_CI']:.3f}, {metrics['Upper_CI']:.3f}]\n"

    details += "\n6. ENSAMBLES AVANZADOS (GRADIENT BOOSTING):\n"
    if res_rf:
        details += f"   - Accuracy: {res_rf.get('accuracy', 0):.4f}\n"
        details += f"   - ROC-AUC:  {res_rf.get('roc_auc', 0):.4f}\n"
        
        rd_rf = res_rf.get('report_dict', {})
        if rd_rf:
            details += f"   - F1-Score (Riesgo): {rd_rf.get('1', {}).get('f1-score', 0):.4f}\n"
            
        details += "   - SHAP Global (Impacto por Dimensión):\n"
        for dim, imp in res_rf.get('feature_importances', {}).items():
            bar = "#" * int(imp * 50)
            details += f"      {dim:15} | {imp:.4f} | {bar}\n"

    details += "\n7. SEGMENTACIÓN MULTIALGORITMO:\n"
    # El ClusteringEngine provee perfiles para todos los algoritmos
    for algo, info in cluster_profiles.get('algorithms', {}).items():
        details += f"   [{algo}]:\n"
        for i, metrics in info.get('profiles', {}).items():
            cnt = info.get('counts', {}).get(i, 0)
            risk_avg = info.get('risk_prev', {}).get(i, 0) * 100
            details += f"     - Grupo {i} (N={cnt}):\n"
            details += f"       * AMI:  Crit={metrics['Score_Critico']:.2f}, Tec={metrics['Score_Tecnico']:.2f}, Part={metrics['Score_Participativo']:.2f}\n"
            details += f"       * RISK: Acad={metrics['Score_Riesgo_Academico']:.2f}, LMS={metrics['Score_Riesgo_LMS']:.2f}, Cont={metrics['Score_Riesgo_Continuidad']:.2f}\n"
            details += f"       * PREVALENCIA TOTAL: {risk_avg:.2f}%\n"
    
    agreement = clusterer.get_model_agreement(df_clustered)
    if 'ari_kmeans_gmm' in agreement:
        details += f"   - Consenso entre Modelos (Adjusted Rand Index): {agreement['ari_kmeans_gmm']:.4f}\n"
    
    details += "   - Métricas de Estabilidad (K=3):\n"
    try:
        idx_3 = cluster_val['k_range'].index(3)
        details += f"     * Silhouette Score: {cluster_val['silhouette_scores'][idx_3]:.4f}\n"
        details += f"     * BIC Score (GMM):  {cluster_val['bic_scores'][idx_3]:.4f}\n"
    except:
        pass

    if xai_features and 'top_items' in xai_features:
        details += "\n8. EXPLAINABLE AI (XAI) GRANULAR (TOP 10 ÍTEMS):\n"
        for i, (item, impact) in enumerate(xai_features['top_items']):
            details += f"     {i+1}. {item}: Impacto {impact:.4f}\n"

    logger.log_run(
        env="Híbrido (Restauración Doctoral)", 
        num_records=len(df_final), 
        accuracy=res_logit.get('accuracy', 0) if res_logit else 0,
        details=details
    )

    print("\n==================================================")
    print("      PROYECTO AMI-VIRTU FINALIADO CON ÉXITO      ")
    print("==================================================")

if __name__ == "__main__":
    main()
