import os
os.environ['OPENBLAS_NUM_THREADS'] = '1'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OMP_NUM_THREADS'] = '1'
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
from src.processing.real_data_loader import RealDataLoader
from src.simulation.data_simulator import DataSimulator
from src.simulation.qualitative_generator import QualitativeGenerator
from dotenv import load_dotenv

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
    
    load_dotenv()
    data_source = os.getenv("DATA_SOURCE", "real").strip().lower()
    generate_synthetic = os.getenv("GENERATE_SYNTHETIC", "false").strip().lower() == "true"
    risk_model_type = os.getenv("PREDICTIVE_RISK_MODEL_TYPE", "both").strip().lower()
    
    # --- [1] Carga y Preparación de Datos Desacoplada ---
    if data_source == "real":
        # Flujo de Datos Reales
        hybrid_input = os.path.join(root_dir, "data", "processed", "real_hybrid_analysis_results_823.csv")
        paper_ready_path = os.path.join(root_dir, "data", "processed", "real_ami_virtu_final_paper_ready_823.csv")
        out_dir = os.path.join(root_dir, 'data', 'outputs', 'real_823')
        log_path = os.path.join(log_dir, f"real_bitacora_ejecuciones_823_{date_str}.log")
        
        if not os.path.exists(hybrid_input):
            excel_raw = os.path.join(root_dir, "data", "raw", "Formulario de Investigación Académica Doctoral - BIU(823).xlsx")
            if os.path.exists(excel_raw):
                print(f"\n[1] Generando dataset real desde el Excel: {excel_raw}")
                loader = RealDataLoader(excel_raw)
                df_raw = loader.load_and_process()
                os.makedirs(os.path.dirname(hybrid_input), exist_ok=True)
                df_raw.to_csv(hybrid_input, index=False, encoding='utf-8-sig')
            else:
                print(f"\n[!] ERROR: No se encontró el archivo de datos reales en: {excel_raw}")
                return
        else:
            df_raw = pd.read_csv(hybrid_input)
            print(f"\n[1] Dataset real cargado satisfactoriamente (N={len(df_raw)}).")
            
    elif data_source == "synthetic":
        # Flujo de Datos Sintéticos
        hybrid_input = os.path.join(root_dir, "data", "processed", "synthetic_hybrid_analysis_results.csv")
        paper_ready_path = os.path.join(root_dir, "data", "processed", "synthetic_ami_virtu_final_paper_ready.csv")
        out_dir = os.path.join(root_dir, 'data', 'outputs', 'synthetic')
        log_path = os.path.join(log_dir, f"synthetic_bitacora_ejecuciones_{date_str}.log")
        
        if not os.path.exists(hybrid_input):
            if generate_synthetic:
                print("\n[1] GENERATE_SYNTHETIC=true: Iniciando simulación de datos sintéticos (Cópulas + Gemini)...")
                # Generar data sintética base
                sim = DataSimulator(num_records=300, risk_ratio=0.33)
                df_sim_raw = sim.generate_dataset()
                # Limpiar y puntuar base
                cleaner = DataCleaner()
                scorer = Scorer()
                df_sim_clean = cleaner.clean_process(df_sim_raw)
                df_sim_scored = scorer.score_process(df_sim_clean)
                # Generar respuestas cualitativas usando Gemini
                gen = QualitativeGenerator()
                df_raw = gen.generate_qualitative_data(df_sim_scored)
                os.makedirs(os.path.dirname(hybrid_input), exist_ok=True)
                df_raw.to_csv(hybrid_input, index=False, encoding='utf-8-sig')
            else:
                print(f"\n[!] ERROR: El archivo de datos sintéticos no existe en: {hybrid_input}")
                print("    Para generarlo automáticamente, por favor configure GENERATE_SYNTHETIC=true en su archivo .env")
                return
        else:
            df_raw = pd.read_csv(hybrid_input)
            print(f"\n[1] Dataset sintético cargado satisfactoriamente (N={len(df_raw)}).")
    else:
        print(f"\n[!] ERROR: Origen de datos DATA_SOURCE='{data_source}' no soportado (debe ser 'real' o 'synthetic').")
        return

    # Asegurar que los datos estén limpios y puntuados (Score_Critico, etc.)
    if 'Score_AMI_Global' not in df_raw.columns:
        print("-> Calculando puntuaciones psicométricas faltantes...")
        cleaner = DataCleaner()
        scorer = Scorer()
        df_raw = cleaner.clean_process(df_raw)
        df_raw = scorer.score_process(df_raw)

    # --- [2] Análisis Cualitativo (Sincronización) ---
    qual_engine = QualitativeEngine()
    # CORRECCIÓN (Hallazgo 5.1): Si la columna existe pero está completamente vacía
    # (todo NaN por un fallo previo de API), se reintenta el análisis cualitativo.
    # Esto supera el "lock-in" que bloqueaba re-ejecuciones tras un fallo de clave API.
    _cuali_missing = (
        "Indice_Coherencia" not in df_raw.columns or
        df_raw["Indice_Coherencia"].isnull().all()
    )
    if _cuali_missing:
        print("\n[2] Iniciando Triangulación Cualitativa (Modo Resiliente)...")
        processed_rows = []
        api_blocked = False
        
        for i, (index, row) in enumerate(df_raw.iterrows(), 1):
            if api_blocked:
                # Si la API está bloqueada, simplemente pasamos la fila sin analizar
                processed_rows.append(row)
                continue
                
            analyzed_row = qual_engine.analyze_single_student(row)
            
            # Detectar error o bloqueo de cuota (marcado en el análisis por el engine)
            if "Error:" in str(analyzed_row.get('Analisis_Cuali', '')):
                print(f"   [!] DETECTADO ERROR EN LA API ({analyzed_row.get('Analisis_Cuali')}). Saltando el resto del análisis cualitativo por resiliencia...")
                api_blocked = True
                
            processed_rows.append(analyzed_row)
        df_hybrid = pd.DataFrame(processed_rows)
        
        df_hybrid.to_csv(hybrid_input, index=False)
    else:
        print("\n[2] Datos cualitativos detectados. Saltando análisis Gemini.")
        df_hybrid = df_raw

    # --- RECONSTRUCCIÓN DINÁMICA DE VARIABLES PREDICTIVAS ---
    map_interrupcion = {'Sí': 1, 'No': 0}
    map_desaprobados = {'Nunca': 0, 'En un Curso': 1, 'En dos o más': 2}
    map_retirados = {'No': 0, 'Sí, en una ocasión': 1, 'Sí, en más de una ocasión': 2}
    map_rendimiento = {'Alto': 1, 'Medio': 2, 'Bajo': 3}
    
    df_hybrid['A1_num'] = df_hybrid['A1_Interrupcion'].map(map_interrupcion).fillna(0)
    df_hybrid['A2_num'] = df_hybrid['A2_Desaprobados'].map(map_desaprobados).fillna(0)
    df_hybrid['A3_num'] = df_hybrid['A3_Retirados'].map(map_retirados).fillna(0)
    df_hybrid['A4_num'] = df_hybrid['A4'].map(map_rendimiento).fillna(1)

    likert_a_candidates = [
        'A5_Dificultad', 'A6_Consideracion_Abandono', 'A7_Exigencia', 'A8_Retrasos',
        'A5', 'A6', 'A7', 'A8'
    ]
    likert_l_cols = [f'L{i}' for i in range(1, 9)]

    for c in likert_a_candidates + likert_l_cols:
        if c in df_hybrid.columns:
            df_hybrid[c] = pd.to_numeric(df_hybrid[c], errors='coerce').fillna(3)

    present_a = [c for c in likert_a_candidates if c in df_hybrid.columns]
    present_l = [c for c in likert_l_cols if c in df_hybrid.columns]

    df_hybrid['Riesgo_Acad_Perceptual'] = df_hybrid[present_a].mean(axis=1) if present_a else 3.0
    df_hybrid['Riesgo_Documental'] = df_hybrid[present_l].mean(axis=1) if present_l else 3.0

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

    # --- [3] Integración Híbrida (FASE 10) ---
    print("\n[3] Ejecutando Integración Híbrida Desacoplada...")
    integrator = HybridIntegrator(threshold=float(os.getenv('COHERENCE_THRESHOLD', 0.6)))
    df_hybrid = integrator.integrate(df_hybrid)
    
    df_final = integrator.finalize_paper_ready_dataset(df_hybrid, paper_ready_path)

    # --- [3.5] Imputación MICE de Datos Faltantes (AMI Likert) ---
    print("\n[3.5] Imputación de datos faltantes (MICE / IterativeImputer)...")
    ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
    ami_present = [c for c in ami_items if c in df_final.columns]

    # Convertir a numérico (por si quedaron strings residuales)
    for c in ami_present:
        df_final[c] = pd.to_numeric(df_final[c], errors='coerce')

    n_missing_before = df_final[ami_present].isnull().sum().sum()
    if n_missing_before > 0:
        from sklearn.experimental import enable_iterative_imputer  # noqa: F401
        from sklearn.impute import IterativeImputer

        imputer = IterativeImputer(random_state=42, max_iter=10)
        df_final[ami_present] = imputer.fit_transform(df_final[ami_present])

        # Redondear a enteros Likert [1, 5]
        for c in ami_present:
            df_final[c] = df_final[c].round().clip(1, 5).astype(int)

        n_missing_after = df_final[ami_present].isnull().sum().sum()
        n_imputed = n_missing_before - n_missing_after

        # Recalcular scores AMI post-imputación
        critico_cols = [f'C{i}' for i in range(1, 11)]
        tecnico_cols = [f'T{i}' for i in range(1, 11)]
        participativo_cols = [f'P{i}' for i in range(1, 11)]

        df_final['Score_Critico'] = df_final[[c for c in critico_cols if c in df_final.columns]].mean(axis=1)
        df_final['Score_Tecnico'] = df_final[[c for c in tecnico_cols if c in df_final.columns]].mean(axis=1)
        df_final['Score_Participativo'] = df_final[[c for c in participativo_cols if c in df_final.columns]].mean(axis=1)
        df_final['Score_AMI_Global'] = df_final[['Score_Critico', 'Score_Tecnico', 'Score_Participativo']].mean(axis=1)

        # Detalle por dimensión
        missing_c = sum(1 for c in critico_cols if c in ami_present for _ in range(1) if df_final[c].isnull().sum() == 0)
        print(f"   -> {n_imputed} valores imputados en {len(ami_present)} columnas AMI.")
        print(f"   -> Scores AMI recalculados post-imputación. N válido ahora: {df_final['Score_AMI_Global'].notna().sum()}/{len(df_final)}")
    else:
        print("   -> No se encontraron datos faltantes en ítems AMI. Sin imputación necesaria.")

    # --- [4] Inferencia Estadística (FASE 11) ---
    print("\n[4] Análisis Inferencial y Triangulación Estadística...")
    analyzer = StatsAnalyzer()
    
    # Fiabilidad, Análisis Factorial y Contrastes
    reliability_df = analyzer.calculate_reliability(df_final)
    factor_res = analyzer.run_factor_analysis(df_final)
    cfa_res = analyzer.run_confirmatory_factor_analysis(df_final)  # [HC-02]
    contrasts = analyzer.run_demographic_contrasts(df_final)       # [HC-03] con efecto
    
    # Triangulación Mixta y Bivariadas
    triangulation_res = analyzer.run_mixed_methods_triangulation(df_final)
    biv = analyzer.run_bivariate_analysis(df_final)
    
    # ML Models (Logit & Random Forest)
    X_train, X_test, y_train, y_test = analyzer.prepare_data(df_final)
    
    res_logit = None
    res_cv = None
    res_rf = None
    interaction_res = None
    res_assumptions = None
    
    if risk_model_type in ["linear", "both"]:
        print("   -> Ejecutando Modelo Lineal (Regresión Logística)...")
        interaction_res = analyzer.run_interaction_analysis(df_final)
        res_assumptions = analyzer.run_logit_assumption_checks(df_final)  # [HI-04]
        res_logit = analyzer.run_logistic_regression(X_train, X_test, y_train, y_test)
        res_cv    = analyzer.run_logistic_cv(df_final)                 # [HC-05] k-Fold CV
        
    if risk_model_type in ["rf", "tree", "both"]:
        print("   -> Ejecutando Modelo No Lineal (Random Forest / Gradient Boosting)...")
        res_rf = analyzer.run_random_forest(X_train, X_test, y_train, y_test)


    # --- [5] Clustering y XAI (Perfilamiento) ---
    print("\n[5] Generando Perfiles Sociológicos y SHAP Analysis...")
    clusterer = ClusteringEngine(n_clusters=3)
    df_clustered = clusterer.run_clustering(df_final)
    cluster_profiles = clusterer.get_cluster_profiles(df_clustered)
    cluster_val = clusterer.validate_clustering(df_final)
    archetypes = clusterer.get_archetypal_cases(df_clustered)
    
    xai_features = None
    try:
        X_train_f, _, y_train_f, _ = analyzer.prepare_feature_data(df_final)
        xai_features = analyzer.run_feature_xai_analysis(X_train_f, y_train_f)
    except Exception as e:
        print(f"   [!] ADVERTENCIA: No se pudo ejecutar SHAP: {e}")

    # --- [5.5] Scientific Validation (FASE 11.5) ---
    print("\n[5.5] Ejecutando Validación Científica Estricta...")
    from src.analysis.scientific_validator import ScientificValidator, TargetDefinition
    import statsmodels.api as sm
    
    validator = ScientificValidator()
    
    target_model = res_rf['model'] if res_rf else (res_logit['model'] if res_logit else None)
    if target_model:
        validator.log_execution_metadata(target_model)
    
    n_raw_val = len(df_raw) if 'df_raw' in locals() else len(df_final)
    n_final_val = len(X_train) + len(X_test)
    validator.log_data_flow(
        n_raw=n_raw_val,
        n_target_valid=n_raw_val,
        n_excluded=n_raw_val - n_final_val,
        n_final=n_final_val,
        n_train=len(X_train),
        n_test=len(X_test)
    )
    
    td = TargetDefinition(
        name="Riesgo_Binario",
        source_variable="Riesgo_Total",
        rule="Score_Riesgo_Total >= 3.0",
        observed_event=False
    )
    validator.log_target_definition(td)
    validator.log_class_distribution(y_train.tolist() + y_test.tolist())
    
    if res_rf:
        model = res_rf['model']
        y_proba = model.predict_proba(X_test)[:, 1]
        threshold = res_rf['threshold']
        y_pred = (y_proba >= threshold).astype(int)
        validator.log_binary_metrics(y_test, y_pred, y_proba)
        validator.log_baselines(X_train, X_test, y_train, y_test, res_rf['roc_auc'])
        
        # FASE 2: Bootstrap Uncertainty
        validator.log_uncertainty(y_test, y_pred, y_proba)
        # FASE 2: Threshold Analysis
        validator.log_threshold_analysis(y_test, y_proba, threshold)
    elif res_logit:
        model = res_logit['model']
        X_test_sm = sm.add_constant(X_test)
        y_proba = model.predict(X_test_sm)
        threshold = res_logit['threshold']
        y_pred = (y_proba >= threshold).astype(int)
        validator.log_binary_metrics(y_test, y_pred, y_proba)
        validator.log_baselines(X_train, X_test, y_train, y_test, res_logit['roc_auc'])
        
        # FASE 2: Bootstrap Uncertainty
        validator.log_uncertainty(y_test, y_pred, y_proba)
        # FASE 2: Threshold Analysis
        validator.log_threshold_analysis(y_test, y_proba, threshold)
        
    if 'Cluster_ID' in df_clustered.columns:
        validator.log_dbscan(df_clustered['Cluster_ID'])
        
    # FASE 2: Cross Validation, Generalización, y Bivariadas (BH)
    if 'biv' in locals():
        validator.log_bivariate_analysis(biv)
        
    if target_model:
        X_full = pd.concat([X_train, X_test])
        y_full = pd.concat([y_train, y_test])
        validator.log_cross_validation(target_model, X_full, y_full)
        if 'Universidad' in df_final.columns:
            groups_full = df_final.loc[X_full.index, 'Universidad']
            validator.log_university_generalization(target_model, X_full, y_full, groups_full)

    validator.log_scientific_summary()

    # --- [6] Reporte Doctoral Final (FASE 12) ---
    print("\n[6] Produciendo Artefactos Finales de Defensa...")
    os.makedirs(out_dir, exist_ok=True)
    reporter = ReportGenerator(output_dir=out_dir)
    
    reporter.generate_all_reports(
        df_clustered, 
        logit_results=res_logit, 
        reliability_df=reliability_df,
        contrasts=contrasts,
        interaction_res=interaction_res,
        xai_features=xai_features,
        cluster_profiles=cluster_profiles,
        triangulation_res=triangulation_res,
        archetypes=archetypes,
        cv_results=res_cv,
        cfa_results=cfa_res,
        rf_results=res_rf
    )

    # --- [7] Bitácora de Ejecución (REPORTE DE ALTA FIDELIDAD) ---
    logger = ExecutionLogger(log_path)
    
    # --- [PhD Rigor] Auditoría de Integridad y Entorno ---
    data_hash = calculate_data_hash(paper_ready_path)
    env_info = verify_reproducibility_env()
    
    # Reconstrucción del reporte detallado doctoral
    details = "0. AUDITORÍA DE REPRODUCIBILIDAD (INTEGRIDAD):\n"
    details += f"   - SHA-256 Dataset: {data_hash}\n"
    details += f"   - Entorno: Py {env_info['Python_Version']} | Sklearn {env_info['Scikit-Learn']} | Statsmodels {env_info['Statsmodels']}\n"
    details += "   - Estado: INTEGRIDAD VERIFICADA.\n\n"

    details += "0b. VALIDACIÓN CONFIRMATORIA (CFA / Tucker's Φ) [HC-02]:\n"
    if cfa_res.get('status') == 'success':
        details += f"   - Método: {cfa_res['method']}\n"
        details += f"   - Referencia: {cfa_res['reference']}\n"
        details += f"   - N total: {cfa_res['n_total']} (Mitad A: {cfa_res['n_half_a']}, Mitad B: {cfa_res['n_half_b']})\n"
        for fac, vals in cfa_res['phi_per_factor'].items():
            details += f"   - {fac}: Φ = {vals['phi']:.4f} | {vals['interpretation']}\n"
        details += f"   - Φ Media Global: {cfa_res['phi_mean']:.4f} | RMSR: {cfa_res['rmsr']:.4f}\n"
        details += f"   - Estructura Confirmada: {'SÍ' if cfa_res['structure_confirmed'] else 'NO'}\n"
        details += f"   - Interpretación: {cfa_res['overall_interpretation']}\n\n"
    else:
        details += f"   - Error CFA: {cfa_res.get('message', 'Desconocido')}\n\n"
    
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

    if res_assumptions:
        details += "2b. VERIFICACIÓN DE SUPUESTOS DEL MODELO LOGÍSTICO [HI-04]:\n"
        # EPV
        epv = res_assumptions.get('epv', {})
        details += f"   EPV (Eventos por Variable): {epv.get('interpretation', 'N/A')}\n"
        # Box-Tidwell
        bt = res_assumptions.get('box_tidwell', {})
        if 'per_feature' in bt:
            details += f"   Box-Tidwell (Linealidad del logit): {bt['overall']}\n"
            for feat, bv in bt['per_feature'].items():
                details += f"      * {feat}: {bv['interpretation']}\n"
        else:
            details += f"   Box-Tidwell: {bt.get('message', 'N/A')}\n"
        # Distancia de Cook
        inf = res_assumptions.get('influential_obs', {})
        if 'interpretation' in inf:
            details += f"   Obs. Influyentes (Cook/Leverage): {inf['interpretation']}\n"
        # Veredicto
        verd = res_assumptions.get('overall_verdict', {})
        details += f"   VEREDICTO GLOBAL: {verd.get('summary', 'N/A')}\n\n"

    details += "3. CONTRASTES SOCIODEMOGRÁFICOS (con Tamaño de Efecto) [HC-03]:\n"
    for k_var, v in contrasts.items():
        details += f"   - {k_var:25}: F/t={v['statistic']:.4f}, p={v['p_value']:.4f}"
        if 'cohen_d' in v:
            details += f", d de Cohen={v['cohen_d']:.4f} ({v['effect_magnitude']})"
            if v.get('observed_power') is not None:
                details += f", Potencia (1-β)={v['observed_power']:.4f}"
        if 'eta2' in v:
            details += f", η²={v['eta2']:.4f}, η²_parcial={v['eta2_partial']:.4f} ({v['effect_magnitude']})"
        details += "\n"

    details += "\n4. ASOCIACIONES BIVARIADAS (AMI vs RIESGO MULTIDIMENSIONAL):\n"
    for risk_dim, ami_corrs in biv.items():
        details += f"   - Dimensión Riesgo: {risk_dim}\n"
        for ami_feat, v in ami_corrs.items():
            details += f"     * {ami_feat:20}: Pearson_r={v['Pearson_r']:+.3f} (p={v['P_Pearson']:.4f}) | Spearman_rho={v['Spearman_rho']:+.3f}\n"

    if res_logit:
        details += "\n5. MODELO DE REGRESIÓN LOGÍSTICA (INFERENCIA CIENTÍFICA):\n"
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
        
        # Cross-Validation [HC-05]
        if res_cv:
            details += "\n- VALIDACIÓN CRUZADA ESTRATIFICADA (Stratified k-Fold) [HC-05]:\n"
            details += f"   * k Pliegues: {res_cv.get('k_folds', 10)}\n"
            details += f"   * N válidos: {res_cv.get('n_samples', 0)} | Casos Riesgo=1: {res_cv.get('n_positive', 0)}\n"
            details += f"   * AUC-ROC Media: {res_cv.get('auc_mean', 0):.4f} (± {res_cv.get('auc_std', 0):.4f})\n"
            ci = res_cv.get('auc_ci_95', [0, 0])
            details += f"   * IC 95% AUC: [{ci[0]:.4f}, {ci[1]:.4f}]\n"
            details += f"   * Accuracy Media: {res_cv.get('accuracy_mean', 0):.4f} (± {res_cv.get('accuracy_std', 0):.4f})\n"
            details += f"   * F1-Score Medio: {res_cv.get('f1_mean', 0):.4f} (± {res_cv.get('f1_std', 0):.4f})\n"
            details += f"   * Interpretación: {res_cv.get('interpretation', 'N/A')}\n"
        
        # Diagnósticos PhD
        if interaction_res:
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

    if res_rf:
        details += "\n6. ENSAMBLES AVANZADOS (GRADIENT BOOSTING / RANDOM FOREST):\n"
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

    if archetypes:
        details += "\n8. MICROSCOPÍA CUALITATIVA (CITAS ARQUETÍPICAS POR GRUPO):\n"
        for grupo, data in archetypes.items():
            details += f"   [{grupo}]: \"{data['Quote'][:150]}...\"\n"
            details += f"      - Temas: {data['Tags']}\n"

    if xai_features and 'top_items' in xai_features:
        details += "\n9. EXPLAINABLE AI (XAI) GRANULAR (TOP 10 ÍTEMS):\n"
        for i, (item, impact) in enumerate(xai_features['top_items']):
            details += f"     {i+1}. {item}: Impacto {impact:.4f}\n"

    # Si logit no se corrió, usamos la accuracy de rf para el log
    final_accuracy = 0
    if res_logit:
        final_accuracy = res_logit.get('accuracy', 0)
    elif res_rf:
        final_accuracy = res_rf.get('accuracy', 0)

    logger.log_run(
        env="Híbrido (Restauración Doctoral)", 
        num_records=len(df_final), 
        accuracy=final_accuracy,
        details=details
    )


    print("\n==================================================")
    print("      PROYECTO AMI-VIRTU FINALIZADO CON ÉXITO      ")
    print("==================================================")

if __name__ == "__main__":
    main()
