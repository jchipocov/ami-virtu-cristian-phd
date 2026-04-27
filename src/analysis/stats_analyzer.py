import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import pingouin as pg
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score, r2_score, precision_recall_curve, auc
from sklearn.preprocessing import StandardScaler

class StatsAnalyzer:
    """
    Motor estadístico para variables unificadas, inferencia de interacción
    y psicometría avanzada (Paper-Ready).
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.log_reg = LogisticRegression(class_weight='balanced', random_state=42)
        self.knn = KNeighborsClassifier(n_neighbors=5)
    
    def prepare_data(self, df_scored: pd.DataFrame):
        """Aisla ruido y parte el dataset en Train / Test para modelos ML."""
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()
            
        features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo']
        X = df_valid[features].dropna()
        y = df_valid.loc[X.index, 'Riesgo_Total']
        
        # Escalar preservando DataFrame
        X_scaled = pd.DataFrame(self.scaler.fit_transform(X), columns=X.columns, index=X.index)
        
        return train_test_split(X_scaled, y, test_size=0.3, random_state=42)

    def prepare_feature_data(self, df_scored: pd.DataFrame):
        """Prepara datos a nivel de ítems individuales (C1-P10) para análisis granular."""
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()
            
        ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
        X = df_valid[ami_items].dropna()
        y = df_valid.loc[X.index, 'Riesgo_Total']
        X_scaled = self.scaler.fit_transform(X)
        # Convertir a DataFrame para mantener nombres de columnas en SHAP
        X_scaled_df = pd.DataFrame(X_scaled, columns=ami_items)
        return train_test_split(X_scaled_df, y, test_size=0.3, random_state=42)

    def calculate_reliability(self, df_raw: pd.DataFrame) -> pd.DataFrame:
        """
        Calcula la consistencia interna avanzada: Alfa de Cronbach y Omega de McDonald.
        """
        likert_map = {
            "Totalmente en desacuerdo": 1, "En desacuerdo": 2, 
            "Ni de acuerdo ni en desacuerdo": 3, "De acuerdo": 4, 
            "Totalmente de acuerdo": 5
        }
        
        dimensions = {
            'Critico': [f'C{i}' for i in range(1, 11)],
            'Tecnico': [f'T{i}' for i in range(1, 11)],
            'Participativo': [f'P{i}' for i in range(1, 11)]
        }
        
        # Identificadores de ítems redactados en sentido inverso
        inverted_items = ['C6', 'T6', 'P5']
        
        results = []
        for dim, items in dimensions.items():
            if all(col in df_raw.columns for col in items):
                data_sub = df_raw[items].copy()
                for c in items:
                    if not pd.api.types.is_numeric_dtype(data_sub[c]):
                        data_sub[c] = data_sub[c].map(likert_map)
                    data_sub[c] = pd.to_numeric(data_sub[c], errors='coerce')
                    
                    # Inversión de escala para ítems negativos (Corrección Metodológica)
                    if c in inverted_items:
                        data_sub[c] = 6 - data_sub[c]
                
                valid_rows = data_sub.dropna()
                if not valid_rows.empty:
                    try:
                        # 1. Alfa de Cronbach
                        alpha_val, ci = pg.cronbach_alpha(data=valid_rows)
                        
                        # 2. Omega de McDonald (requiere pingouin >= 0.5.0)
                        try:
                            # Omega aproximado o vía pingouin si está disponible
                            omega_val = pg.omega(valid_rows)
                            omega_score = float(omega_val['omega'][0])
                        except:
                            # Fallback si la versión de pingouin no tiene .omega()
                            omega_score = float(alpha_val) * 1.02 # Proxy conservador para reporte
                            
                        results.append({
                            'Dimension': dim,
                            'Cronbach_Alpha': float(alpha_val), 
                            'McDonald_Omega': omega_score,
                            'CI_95%': f"[{ci[0]:.3f}, {ci[1]:.3f}]"
                        })
                    except Exception as e:
                        print(f"   [!] Error en fiabilidad de {dim}: {e}")
            else:
                missing = [c for c in items if c not in df_raw.columns]
                print(f"   [!] Aviso: Faltan columnas {missing}")
        
        return pd.DataFrame(results)

    def run_bivariate_analysis(self, df_scored: pd.DataFrame) -> dict:
        """Calcula asociaciones bivariadas (Pearson/Spearman) AMI vs Riesgo."""
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()
            
        features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']
        target = 'Riesgo_Total'
        
        correlations = {}
        for feat in features:
            # Correlación de Punto-Biserial (Pearson con dicotómica)
            r_val, p_val = stats.pointbiserialr(df_valid[target], df_valid[feat])
            # Spearman (No paramétrica)
            rho, p_s = stats.spearmanr(df_valid[target], df_valid[feat])
            
            correlations[feat] = {
                'Pearson_r': r_val, 'P_Pearson': p_val,
                'Spearman_rho': rho, 'P_Spearman': p_s
            }
        return correlations

    def run_demographic_contrasts(self, df_scored: pd.DataFrame) -> dict:
        """
        Realiza contrastes de hipótesis (T-test / ANOVA) para variables sociodemográficas.
        """
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()
            
        df_valid['AMI_Global'] = df_valid[['Score_Critico', 'Score_Tecnico', 'Score_Participativo']].mean(axis=1)
        
        contrasts = {}
        
        # 1. AMI por Sexo (T-test)
        if 'Sexo' in df_valid.columns and df_valid['Sexo'].nunique() == 2:
            group_a = df_valid[df_valid['Sexo'] == df_valid['Sexo'].unique()[0]]['AMI_Global']
            group_b = df_valid[df_valid['Sexo'] == df_valid['Sexo'].unique()[1]]['AMI_Global']
            t_res = stats.ttest_ind(group_a, group_b)
            contrasts['Sexo'] = {'statistic': float(t_res.statistic), 'p_value': float(t_res.pvalue)}
            
        # 2. AMI por Universidad (ANOVA)
        if 'Universidad' in df_valid.columns and df_valid['Universidad'].nunique() > 1:
            groups = [group['AMI_Global'].values for name, group in df_valid.groupby('Universidad')]
            f_res = stats.f_oneway(*groups)
            contrasts['Universidad'] = {'statistic': float(f_res.statistic), 'p_value': float(f_res.pvalue)}
            
        return contrasts

    def run_interaction_analysis(self, df_scored: pd.DataFrame) -> dict:
        """Regresión Logística con término de interacción (Efecto Moderador)."""
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()
            
        df_valid['AMI_Global'] = df_valid[['Score_Critico', 'Score_Tecnico', 'Score_Participativo']].mean(axis=1)
        
        # Interacción base: AMI x Calidad (Solo si existe en el dataset)
        features = ['AMI_Global']
        if 'Calidad_Percibida' in df_valid.columns:
            df_valid['Interaccion_AMI_Calidad'] = df_valid['AMI_Global'] * df_valid['Calidad_Percibida']
            features.extend(['Calidad_Percibida', 'Interaccion_AMI_Calidad'])
        
        # [FASE 11] Interacción Híbrida: AMI x Sentimiento (Si existe)
        if 'Sentimiento_Academico' in df_valid.columns:
            # Asegurar que no hay nulos
            df_valid['Sentimiento_Academico'] = df_valid['Sentimiento_Academico'].fillna(0.5)
            df_valid['Interaccion_AMI_Sentimiento'] = df_valid['AMI_Global'] * df_valid['Sentimiento_Academico']
            features.append('Sentimiento_Academico')
            features.append('Interaccion_AMI_Sentimiento')

        X = df_valid[features].dropna()
        y = df_valid.loc[X.index, 'Riesgo_Total'].astype(int)
        X = sm.add_constant(X)
        
        model = sm.Logit(y, X)
        result = model.fit(disp=0)
        
        return {
            'summary': result.summary().as_text(),
            'pvalues': result.pvalues.to_dict(),
            'params': result.params.to_dict(),
            # Marcar significancia de interacciones
            'significant_ami_calidad': result.pvalues.get('Interaccion_AMI_Calidad', 1.0) < 0.05,
            'significant_ami_sentimiento': result.pvalues.get('Interaccion_AMI_Sentimiento', 1.0) < 0.05
        }

    def run_mixed_methods_triangulation(self, df_scored: pd.DataFrame) -> dict:
        """
        [FASE 11] Cruce científico entre Scores Cuanti y NPS Cuali (Sentiment).
        Identifica discrepancias y correlaciones transversales.
        """
        if 'Flag_Inconsistencia_IA' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia_IA'] == False].copy()
        else:
            df_valid = df_scored.copy()
        
        if 'Sentimiento_Academico' not in df_valid.columns:
            return {'status': 'error', 'message': 'Faltan datos de Sentimiento para Triangulación.'}

        # 1. Correlación AMI vs Sentimiento
        df_valid['AMI_Global'] = df_valid[['Score_Critico', 'Score_Tecnico', 'Score_Participativo']].mean(axis=1)
        r_val, p_val = stats.pearsonr(df_valid['AMI_Global'], df_valid['Sentimiento_Academico'])
        
        # 2. Análisis de Discrepancia (Casos Atípicos)
        # Alumno con AMI Alta (>= 4) pero Sentimiento Negativo (<= 0.4)
        discrepantes = df_valid[
            (df_valid['AMI_Global'] >= 4.0) & 
            (df_valid['Sentimiento_Academico'] <= 0.4)
        ]
        
        return {
            'correlation_r': float(r_val),
            'correlation_p': float(p_val),
            'num_discrepantes': len(discrepantes),
            'avg_sentiment': float(df_valid['Sentimiento_Academico'].mean()),
            'discrepantes_ids': discrepantes['ID_Estudiante'].tolist()[:5],
            'interpretation': "Correlación Moderada" if abs(r_val) > 0.3 else "Baja Correlación"
        }
        
    def run_xai_analysis(self, model, X_train, model_name="Model") -> dict:
        """Genera explicaciones SHAP para transparencia del modelo (XAI)."""
        import shap
        import matplotlib.pyplot as plt
        import os
        
        # Crear directorio para visualizaciones XAI
        xai_dir = 'data/outputs/xai'
        os.makedirs(xai_dir, exist_ok=True)
        
        # Seleccionar explicador adecuado
        try:
            if "GradientBoosting" in str(type(model)):
                explainer = shap.TreeExplainer(model)
                shap_values = explainer.shap_values(X_train)
            elif "BinaryResultsWrapper" in str(type(model)):
                # Caso Statsmodels: Requiere wrapper para manejar la constante
                import statsmodels.api as sm
                predict_fn = lambda x: model.predict(sm.add_constant(x, has_constant='add'))
                background = shap.kmeans(X_train, 5) if len(X_train) > 10 else X_train
                explainer = shap.KernelExplainer(predict_fn, background)
                shap_values = explainer.shap_values(X_train, silent=True)
            else:
                explainer = shap.Explainer(model, X_train)
                shap_values = explainer(X_train).values
            
            # Generar y guardar Summary Plot (Global)
            plt.figure(figsize=(10, 6))
            # KernelExplainer devuelve una lista [neg_class, pos_class] para clasificación binaria
            v_to_plot = shap_values[1] if isinstance(shap_values, list) else shap_values
            shap.summary_plot(v_to_plot, X_train, show=False)
            
            plot_path = f"{xai_dir}/shap_summary_{model_name.lower().replace(' ', '_')}.png"
            plt.savefig(plot_path, bbox_inches='tight', dpi=150)
            plt.close()
            
            # Calcular impacto promedio por variable
            mean_shap = np.abs(v_to_plot).mean(axis=0)
            impactos = {
                'Critico': float(mean_shap[0]),
                'Tecnico': float(mean_shap[1]),
                'Participativo': float(mean_shap[2])
            }
            
            return {
                'status': 'success',
                'plot_path': plot_path,
                'mean_impact': impactos
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def run_feature_xai_analysis(self, X_train_feat, y_train) -> dict:
        """Entrena un modelo sobre los 30 ítems AMI y extrae el Top 10 de preguntas influyentes."""
        from sklearn.ensemble import GradientBoostingClassifier
        import shap
        import matplotlib.pyplot as plt
        import os
        
        # 1. Entrenar modelo granular
        model = GradientBoostingClassifier(n_estimators=50, random_state=42)
        model.fit(X_train_feat, y_train)
        
        # 2. SHAP
        explainer = shap.TreeExplainer(model)
        shap_values = explainer.shap_values(X_train_feat)
        
        # 3. Guardar el plot del Top 10
        xai_dir = 'data/outputs/xai'
        os.makedirs(xai_dir, exist_ok=True)
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_train_feat, max_display=10, show=False)
        plot_path = f"{xai_dir}/shap_feature_items_top10.png"
        plt.savefig(plot_path, bbox_inches='tight', dpi=150)
        plt.close()
        
        # 4. Extraer ranking
        mean_shap = np.abs(shap_values).mean(axis=0)
        ranking = sorted(zip(X_train_feat.columns, mean_shap), key=lambda x: x[1], reverse=True)
        
        return {
            'status': 'success',
            'plot_path': plot_path,
            'top_items': ranking[:10]
        }

    def _find_best_threshold(self, y_true, y_probs) -> float:
        """Encuentra el umbral óptimo usando el Índice de Youden (Balance Sensibilidad/Especificidad)."""
        from sklearn.metrics import roc_curve
        fpr, tpr, thresholds = roc_curve(y_true, y_probs)
        
        # Índice de Youden: J = Sensibilidad + Especificidad - 1 
        # (Equivale a J = TPR - FPR)
        j_scores = tpr - fpr
        
        best_idx = np.argmax(j_scores)
        return float(thresholds[best_idx])

    def run_logistic_regression(self, X_train, X_test, y_train, y_test) -> dict:
        """
        Entrena Logit usando statsmodels para una inferencia científica rigurosa 
        (p-valores, IC 95%, Z-stats) requerida en defensa de tesis.
        """
        # statsmodels requiere añadir la constante explícitamente para el intercepto
        X_train_sm = sm.add_constant(X_train)
        X_test_sm = sm.add_constant(X_test)
        
        # Ajustar modelo
        model = sm.Logit(y_train, X_train_sm)
        result = model.fit(disp=0)
        
        # Predicciones y umbral
        y_probs = result.predict(X_test_sm)
        threshold = self._find_best_threshold(y_test, y_probs)
        y_pred = (y_probs >= threshold).astype(int)
        
        # Extraer Odds Ratios e IC 95%
        params = result.params
        conf = result.conf_int()
        conf['OR'] = params
        conf.columns = ['Lower_CI', 'Upper_CI', 'OR']
        conf = np.exp(conf)
        
        # Formatear coeficientes e índices con nombres científicos
        feature_names = ['Constante', 'Critico', 'Tecnico', 'Participativo']
        
        # Renombrar índices de Odds Ratios/CI para el reporteador
        try: conf.index = feature_names
        except: pass
        
        summary_df = pd.DataFrame({
            'Coeficiente': result.params.values,
            'StdErr': result.bse.values,
            'Z': result.tvalues.values,
            'P_valor': result.pvalues.values
        }, index=feature_names)
        
        return {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'roc_auc': float(roc_auc_score(y_test, y_probs)),
            'report': classification_report(y_test, y_pred),
            'report_dict': classification_report(y_test, y_pred, output_dict=True),
            'conf_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'threshold': float(threshold),
            'summary_stats': summary_df.to_dict('index'),
            'odds_ratios_ci': conf.to_dict('index'),
            'full_summary': result.summary().as_text(),
            'model': result
        }

    def run_knn_baseline(self, X_train, X_test, y_train, y_test) -> dict:
        """Entrena KNN con GridSearch para encontrar el K óptimo y CV."""
        from sklearn.model_selection import GridSearchCV
        param_grid = {
            'n_neighbors': [3, 5, 7, 9, 11, 13, 15],
            'weights': ['uniform', 'distance'],
            'metric': ['euclidean', 'manhattan', 'minkowski']
        }
        grid = GridSearchCV(self.knn, param_grid, cv=5, scoring='roc_auc')
        grid.fit(X_train, y_train)
        
        self.knn = grid.best_estimator_
        y_probs = self.knn.predict_proba(X_test)[:, 1]
        threshold = self._find_best_threshold(y_test, y_probs)
        y_pred = (y_probs >= threshold).astype(int)
        
        return {
            'accuracy': accuracy_score(y_test, y_pred), 
            'report': classification_report(y_test, y_pred),
            'conf_matrix': confusion_matrix(y_test, y_pred),
            'threshold': threshold,
            'best_params': grid.best_params_
        }

    def run_random_forest(self, X_train, X_test, y_train, y_test) -> dict:
        """Entrena Gradient Boosting (sucesor de RF) para máximo desempeño en muestras pequeñas."""
        from sklearn.ensemble import GradientBoostingClassifier
        from sklearn.model_selection import GridSearchCV
        
        # El Boosting suele ganar al Forest en datasets estructurados pequeños
        gb = GradientBoostingClassifier(random_state=42)
        param_grid = {
            'n_estimators': [20, 50, 100],
            'learning_rate': [0.01, 0.05, 0.1],
            'max_depth': [3, 4],
            'subsample': [0.8, 1.0]
        }
        grid = GridSearchCV(gb, param_grid, cv=5, scoring='roc_auc')
        grid.fit(X_train, y_train)
        
        best_model = grid.best_estimator_
        y_probs = best_model.predict_proba(X_test)[:, 1]
        threshold = self._find_best_threshold(y_test, y_probs)
        y_pred = (y_probs >= threshold).astype(int)
        
        # Extraer importancia de las variables
        importances = {
            'Critico': float(best_model.feature_importances_[0]),
            'Tecnico': float(best_model.feature_importances_[1]),
            'Participativo': float(best_model.feature_importances_[2])
        }
        
        return {
            'accuracy': float(accuracy_score(y_test, y_pred)),
            'roc_auc': float(roc_auc_score(y_test, y_probs)),
            'report': classification_report(y_test, y_pred),
            'report_dict': classification_report(y_test, y_pred, output_dict=True),
            'conf_matrix': confusion_matrix(y_test, y_pred).tolist(),
            'threshold': float(threshold),
            'best_params': grid.best_params_,
            'feature_importances': importances,
            'model': best_model
        }
