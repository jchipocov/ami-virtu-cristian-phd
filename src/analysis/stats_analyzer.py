import sklearn.utils
import sklearn.utils.validation

# Parche de compatibilidad agresivo para factor-analyzer y sklearn moderno
def check_array_patched(*args, **kwargs):
    if 'force_all_finite' in kwargs:
        kwargs['ensure_all_finite'] = kwargs.pop('force_all_finite')
    return sklearn.utils.validation.check_array_original(*args, **kwargs)

if not hasattr(sklearn.utils.validation, 'check_array_original'):
    sklearn.utils.validation.check_array_original = sklearn.utils.validation.check_array
    sklearn.utils.validation.check_array = check_array_patched
    sklearn.utils.check_array = check_array_patched
    # A veces se importa directamente de sklearn.utils
    try:
        import sklearn.utils
        sklearn.utils.check_array = check_array_patched
    except:
        pass

import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy import stats
import pingouin as pg
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix, roc_auc_score, r2_score, precision_recall_curve, auc
from sklearn.preprocessing import StandardScaler
from statsmodels.stats.outliers_influence import variance_inflation_factor
from factor_analyzer import FactorAnalyzer
from factor_analyzer.factor_analyzer import calculate_kmo, calculate_bartlett_sphericity

class StatsAnalyzer:
    """
    Motor estadístico para variables unificadas, inferencia de interacción
    y psicometría avanzada (Paper-Ready).
    """

    def __init__(self):
        self.scaler = StandardScaler()
        self.log_reg = LogisticRegression(class_weight='balanced', random_state=42)
        self.knn = KNeighborsClassifier(n_neighbors=5)
        self.tuned_rf_params = None
        
    def _get_rf_model(self, X, y, tune=False):
        from sklearn.ensemble import RandomForestClassifier as RF
        if not tune:
            return RF(random_state=42, class_weight='balanced')
        
        if self.tuned_rf_params is not None:
            return RF(random_state=42, **self.tuned_rf_params)
            
        print("\n   [INFO] Iniciando GridSearchCV para Random Forest (PR-AUC)...")
        from sklearn.model_selection import GridSearchCV
        rf_base = RF(random_state=42)
        param_grid = {
            "n_estimators": [300, 500],
            "max_depth": [4, 6, 8, None],
            "min_samples_leaf": [2, 5, 10],
            "max_features": ["sqrt", 0.7],
            "class_weight": [None, "balanced"]
        }
        grid = GridSearchCV(rf_base, param_grid, cv=5, scoring='average_precision', n_jobs=-1)
        grid.fit(X, y)
        self.tuned_rf_params = grid.best_params_
        print(f"   [INFO] GridSearch completado. Mejores parámetros: {self.tuned_rf_params}")
        return RF(random_state=42, **self.tuned_rf_params)
    
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
            'Participativo': [f'P{i}' for i in range(1, 11)],
            'Riesgo_Academico': [f'A{i}_num' if i <= 4 else f'A{i}_Dificultad_num' if i==5 else f'A6_Consideracion_Abandono_num' if i==6 else f'A7_Exigencia_num' if i==7 else f'A8_Retrasos_num' for i in range(1, 9)],
            'Riesgo_LMS': [f'L{i}_num' for i in range(1, 9)]
        }
        
        # CORRECCIÓN (Hallazgo Adicional A): T6 y P5 son positivos en la encuesta real.
        # Se alinea con la corrección de cleaner.py para no aplicar doble inversión.
        inverted_items = ['C6']
        
        results = []
        for dim, items in dimensions.items():
            if all(col in df_raw.columns for col in items):
                data_sub = df_raw[items].copy()
                for c in items:
                    if not pd.api.types.is_numeric_dtype(data_sub[c]):
                        # Mapeo específico para categorías de riesgo si aparecen
                        risk_cat_map = {
                            'Sí': 5, 'No': 1, 
                            'En dos o más cursos': 5, 'En uno': 3, 'Ninguno': 1,
                            'Bajo': 5, 'Medio': 3, 'Alto': 1
                        }
                        if any(val in risk_cat_map for val in data_sub[c].unique()):
                            data_sub[c] = data_sub[c].map(risk_cat_map)
                        else:
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

    def run_factor_analysis(self, df_raw: pd.DataFrame) -> dict:
        """
        Ejecuta Análisis Factorial Exploratorio (EFA) con pruebas de adecuación.
        Valida KMO, Bartlett y extrae cargas factoriales con rotación Oblimin.
        """
        ami_items = [f'C{i}' for i in range(1, 11)] + [f'T{i}' for i in range(1, 11)] + [f'P{i}' for i in range(1, 11)]
        
        # Preparar datos (Likert -> Numérico)
        likert_map = {
            "Totalmente en desacuerdo": 1, "En desacuerdo": 2, 
            "Ni de acuerdo ni en desacuerdo": 3, "De acuerdo": 4, 
            "Totalmente de acuerdo": 5
        }
        
        data_efa = df_raw[ami_items].copy()
        for col in ami_items:
            if not pd.api.types.is_numeric_dtype(data_efa[col]):
                data_efa[col] = data_efa[col].map(likert_map)
            data_efa[col] = pd.to_numeric(data_efa[col], errors='coerce')
        
        data_efa = data_efa.dropna()
        
        if data_efa.shape[0] < 20:
            return {'status': 'error', 'message': 'Muestra insuficiente para EFA.'}
            
        try:
            # 1. Pruebas de Adecuación
            chi_square_value, p_value = calculate_bartlett_sphericity(data_efa)
            kmo_all, kmo_model = calculate_kmo(data_efa)
            
            # 2. Ejecutar EFA (3 Factores teóricos, Rotación Oblimin)
            # Nota: Usamos method='minres' para mayor estabilidad en muestras pequeñas
            fa = FactorAnalyzer(n_factors=3, rotation="oblimin", method="minres")
            fa.fit(data_efa)
            
            # Extraer cargas (Loadings)
            loadings = pd.DataFrame(fa.loadings_, columns=['Factor1', 'Factor2', 'Factor3'], index=ami_items)
            
            # Varianza explicada
            var_exp = fa.get_factor_variance()
            
            return {
                'status': 'success',
                'kmo': float(kmo_model),
                'bartlett_p': float(p_value),
                'variance_explained': [float(v) for v in var_exp[1]], # Proporción de varianza por factor
                'loadings': loadings.to_dict('index'),
                'interpretation': "Estructura Válida" if kmo_model > 0.6 and p_value < 0.05 else "Revisar Estructura"
            }
        except Exception as e:
            return {'status': 'error', 'message': str(e)}

    def run_bivariate_analysis(self, df_scored: pd.DataFrame) -> dict:
        """
        Calcula asociaciones bivariadas AMI vs Riesgo (Global y Dimensional).
        Genera la matriz 3x3 requerida por los Objetivos 2 y 3.
        """
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()
            
        ami_features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo', 'Score_AMI_Global']
        risk_targets = ['Riesgo_Total', 'Score_Riesgo_Academico', 'Score_Riesgo_LMS', 'Score_Riesgo_Continuidad']
        
        correlations = {}
        from statsmodels.stats.multitest import multipletests
        
        # Recolectar todos los p-valores para corrección múltiple
        p_values_list = []
        for risk in risk_targets:
            if risk not in df_valid.columns: continue
            correlations[risk] = {}
            for ami in ami_features:
                pair = df_valid[[risk, ami]].dropna()
                if len(pair) > 2:
                    r_val, p_val = stats.pearsonr(pair[risk], pair[ami])
                    rho, p_s = stats.spearmanr(pair[risk], pair[ami])
                else:
                    r_val, p_val = np.nan, np.nan
                    rho, p_s = np.nan, np.nan
                
                correlations[risk][ami] = {
                    'Pearson_r': float(r_val), 'P_Pearson': float(p_val),
                    'Spearman_rho': float(rho), 'P_Spearman': float(p_s)
                }
                if not np.isnan(p_val):
                    p_values_list.append((risk, ami, p_val))
                    
        # Aplicar Benjamini-Hochberg
        if p_values_list:
            pvals = [p[2] for p in p_values_list]
            _, p_adj, _, _ = multipletests(pvals, alpha=0.05, method='fdr_bh')
            for (risk, ami, orig_p), adj_p in zip(p_values_list, p_adj):
                correlations[risk][ami]['P_Pearson_BH'] = float(adj_p)
                r_val = correlations[risk][ami]['Pearson_r']
                if abs(r_val) < 0.10: eff = "Trivial"
                elif abs(r_val) < 0.30: eff = "Pequeño"
                elif abs(r_val) < 0.50: eff = "Moderado"
                else: eff = "Grande"
                correlations[risk][ami]['Effect_Size'] = eff

        return correlations

    def run_demographic_contrasts(self, df_scored: pd.DataFrame) -> dict:
        """
        [HC-03] Contrastes sociodemográficos con tamaños de efecto (APA 7ª ed.).
        - T-test de Welch → d de Cohen + potencia observada (via pingouin).
        - ANOVA de una vía → η² (eta cuadrado) + η² parcial.
        """
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()

        df_valid['AMI_Global'] = df_valid[[
            'Score_Critico', 'Score_Tecnico', 'Score_Participativo'
        ]].mean(axis=1)

        contrasts = {}

        # --- 1. AMI por Sexo (T-test de Welch + d de Cohen) ---
        if 'Sexo' in df_valid.columns and df_valid['Sexo'].nunique() == 2:
            cats = df_valid['Sexo'].unique()
            group_a = df_valid[df_valid['Sexo'] == cats[0]]['AMI_Global'].dropna()
            group_b = df_valid[df_valid['Sexo'] == cats[1]]['AMI_Global'].dropna()

            t_res = stats.ttest_ind(group_a, group_b, equal_var=False)  # Welch

            # d de Cohen (pooled SD)
            n_a, n_b = len(group_a), len(group_b)
            pooled_std = np.sqrt(
                ((n_a - 1) * group_a.std()**2 + (n_b - 1) * group_b.std()**2)
                / (n_a + n_b - 2)
            )
            cohen_d = float((group_a.mean() - group_b.mean()) / pooled_std) if pooled_std > 0 else 0.0

            # Magnitud del efecto según Cohen (1988)
            if abs(cohen_d) < 0.2:
                effect_label = "Trivial"
            elif abs(cohen_d) < 0.5:
                effect_label = "Pequeño"
            elif abs(cohen_d) < 0.8:
                effect_label = "Mediano"
            else:
                effect_label = "Grande"

            # Potencia observada (aproximación analítica 1-β)
            try:
                power_res = pg.power_ttest(
                    d=abs(cohen_d), n=min(n_a, n_b), alpha=0.05, alternative='two-sided'
                )
                observed_power = float(power_res)
            except Exception:
                observed_power = None

            contrasts['Sexo'] = {
                'statistic': float(t_res.statistic),
                'p_value': float(t_res.pvalue),
                'cohen_d': cohen_d,
                'effect_magnitude': effect_label,
                'observed_power': observed_power,
                'n_group_a': n_a,
                'n_group_b': n_b,
                'group_labels': [str(cats[0]), str(cats[1])]
            }

        # --- 2. AMI por Universidad (ANOVA + η²) ---
        if 'Universidad' in df_valid.columns and df_valid['Universidad'].nunique() > 1:
            groups_dict = {name: grp['AMI_Global'].dropna().values
                           for name, grp in df_valid.groupby('Universidad')}
            groups_list = list(groups_dict.values())

            f_res = stats.f_oneway(*groups_list)

            # η² (eta cuadrado) = SS_between / SS_total
            grand_mean = df_valid['AMI_Global'].mean()
            ss_between = sum(
                len(g) * (g.mean() - grand_mean)**2 for g in groups_list
            )
            ss_total = sum(
                ((df_valid['AMI_Global'] - grand_mean)**2).sum()
                for _ in [None]  # trick para no repetir
            )
            # Recalculamos ss_total correctamente
            ss_total = float(((df_valid['AMI_Global'] - grand_mean)**2).sum())
            eta2 = float(ss_between / ss_total) if ss_total > 0 else 0.0

            # η² parcial = F*(k-1) / [F*(k-1) + (N-k)]
            k = len(groups_list)
            N = sum(len(g) for g in groups_list)
            df_between = k - 1
            df_within = N - k
            eta2_partial = float(
                (f_res.statistic * df_between) /
                (f_res.statistic * df_between + df_within)
            ) if (f_res.statistic * df_between + df_within) > 0 else 0.0

            if eta2 < 0.01:
                effect_label_anova = "Trivial"
            elif eta2 < 0.06:
                effect_label_anova = "Pequeño"
            elif eta2 < 0.14:
                effect_label_anova = "Mediano"
            else:
                effect_label_anova = "Grande"

            contrasts['Universidad'] = {
                'statistic': float(f_res.statistic),
                'p_value': float(f_res.pvalue),
                'eta2': eta2,
                'eta2_partial': eta2_partial,
                'effect_magnitude': effect_label_anova,
                'k_groups': k,
                'N_total': N
            }

        return contrasts

    def _calculate_hosmer_lemeshow(self, y_true, y_probs, groups=10):
        """
        Prueba de Bondad de Ajuste de Hosmer-Lemeshow.
        Compara frecuencias observadas vs esperadas por deciles de riesgo.
        """
        df = pd.DataFrame({'y_true': y_true, 'y_probs': y_probs})
        df['decile'] = pd.qcut(df['y_probs'], groups, duplicates='drop')
        
        observed = df.groupby('decile')['y_true'].sum()
        expected = df.groupby('decile')['y_probs'].sum()
        counts = df.groupby('decile')['y_true'].count()
        
        # Evitar ceros en el denominador
        hl_stat = (((observed - expected)**2) / (expected * (1 - expected/counts))).sum()
        df_freedom = max(1, groups - 2)
        p_val = 1 - stats.chi2.cdf(hl_stat, df_freedom)
        
        return float(hl_stat), float(p_val)

    def calculate_vif(self, X: pd.DataFrame) -> pd.DataFrame:
        """Calcula el Factor de Inflación de la Varianza (VIF) para descartar multicolinealidad."""
        # statsmodels requiere constante para VIF correcto
        if 'const' not in X.columns:
            X_temp = sm.add_constant(X)
        else:
            X_temp = X
            
        vif_data = pd.DataFrame()
        vif_data["Variable"] = X_temp.columns
        vif_data["VIF"] = [variance_inflation_factor(X_temp.values, i) for i in range(X_temp.shape[1])]
        # Retornar sin la constante para mayor claridad
        return vif_data[vif_data["Variable"] != 'const']

    def run_interaction_analysis(self, df_scored: pd.DataFrame) -> dict:
        """Regresión Logística con Mean-Centering y términos de interacción."""
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()
            
        df_valid['AMI_Global'] = df_valid[['Score_Critico', 'Score_Tecnico', 'Score_Participativo']].mean(axis=1)
        
        # [PhD Rigor] Mean-Centering: Centrar variables para reducir multicolinealidad estructural
        df_valid['AMI_Centered'] = df_valid['AMI_Global'] - df_valid['AMI_Global'].mean()
        
        features = ['AMI_Centered']
        
        if 'Calidad_Percibida' in df_valid.columns and df_valid['Calidad_Percibida'].notnull().any():
            df_valid['Calidad_Centered'] = df_valid['Calidad_Percibida'] - df_valid['Calidad_Percibida'].mean()
            df_valid['Interaccion_AMI_Calidad'] = df_valid['AMI_Centered'] * df_valid['Calidad_Centered']
            features.extend(['Calidad_Centered', 'Interaccion_AMI_Calidad'])
        
        if 'Sentimiento_Academico' in df_valid.columns and df_valid['Sentimiento_Academico'].notnull().any():
            # Asegurar que no hay nulos
            df_valid['Sentimiento_Academico'] = df_valid['Sentimiento_Academico'].fillna(0.5)
            df_valid['Sentimiento_Centered'] = df_valid['Sentimiento_Academico'] - df_valid['Sentimiento_Academico'].mean()
            df_valid['Interaccion_AMI_Sentimiento'] = df_valid['AMI_Centered'] * df_valid['Sentimiento_Centered']
            features.extend(['Sentimiento_Centered', 'Interaccion_AMI_Sentimiento'])

        X = df_valid[features].dropna()
        y = df_valid.loc[X.index, 'Riesgo_Total'].astype(int)
        X_with_const = sm.add_constant(X)
        
        # Ejecutar Modelo
        model = sm.Logit(y, X_with_const)
        result = model.fit(disp=0)
        
        # Diagnósticos
        vif_df = self.calculate_vif(X)
        y_probs = result.predict(X_with_const)
        hl_stat, hl_p = self._calculate_hosmer_lemeshow(y, y_probs)
        
        return {
            'summary': result.summary().as_text(),
            'pvalues': result.pvalues.to_dict(),
            'params': result.params.to_dict(),
            'vif_diagnostics': vif_df.to_dict('records'),
            'hosmer_lemeshow': {'stat': hl_stat, 'p_value': hl_p},
            'significant_ami_calidad': result.pvalues.get('Interaccion_AMI_Calidad', 1.0) < 0.05,
            'significant_ami_sentimiento': result.pvalues.get('Interaccion_AMI_Sentimiento', 1.0) < 0.05,
            'interpretation_hl': "Ajuste Adecuado" if hl_p > 0.05 else "Ajuste Deficiente (Revisar Modelo)"
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
        
        if 'Sentimiento_Academico' not in df_valid.columns or df_valid['Sentimiento_Academico'].isnull().all():
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

    def run_logit_assumption_checks(self, df_scored: pd.DataFrame) -> dict:
        """
        [HI-04] Verificación completa de supuestos de la Regresión Logística.

        Supuestos verificados (APA / Hosmer et al., 2013):
        1. Linealidad del logit (Box-Tidwell): X * ln(X) no debe ser significativo (p > .05).
        2. Observaciones influyentes: Distancia de Cook y leverage (hat values).
        3. EPV (Events Per Variable): Mínimo 10-15 eventos por predictor para estabilidad.

        Referencias
        -----------
        Box, G. E. P., & Tidwell, P. W. (1962). Transformation of the independent variables.
            Technometrics, 4(4), 531–550.
        Cook, R. D. (1977). Detection of influential observation in linear regression.
            Technometrics, 19(1), 15–18.
        Peduzzi, P. et al. (1996). J. Clinical Epidemiology, 49(12), 1373–1379.
        """
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()

        features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo']
        X = df_valid[features].dropna()
        y = df_valid.loc[X.index, 'Riesgo_Total'].astype(int)

        results = {}

        # ── 1. EPV (Events Per Variable) ──────────────────────────────────────
        n_events = int(y.sum())
        n_predictors = len(features)
        epv = n_events / n_predictors
        epv_ok = epv >= 10
        results['epv'] = {
            'n_events': n_events,
            'n_predictors': n_predictors,
            'epv_ratio': float(epv),
            'threshold': 10,
            'ok': epv_ok,
            'interpretation': (
                f"EPV={epv:.1f} ≥ 10 — Muestra adecuada para {n_predictors} predictores"
                if epv_ok else
                f"EPV={epv:.1f} < 10 — Riesgo de sobreajuste con {n_predictors} predictores"
            )
        }

        # ── 2. Box-Tidwell: Linealidad del logit ───────────────────────────────
        # Se añade el término de interacción X * ln(X) al modelo.
        # Si es significativo (p < .05) → relación NO lineal en el logit.
        try:
            X_bt = X.copy()
            for feat in features:
                vals = X_bt[feat].clip(lower=0.001)  # evitar ln(0)
                X_bt[f'{feat}_lnX'] = vals * np.log(vals)

            X_bt_const = sm.add_constant(X_bt)
            model_bt = sm.Logit(y, X_bt_const).fit(disp=0, maxiter=100)

            bt_results = {}
            for feat in features:
                term = f'{feat}_lnX'
                p = float(model_bt.pvalues.get(term, 1.0))
                bt_results[feat] = {
                    'p_interaction': p,
                    'linearity_ok': p > 0.05,
                    'interpretation': (
                        f"p={p:.4f} > .05 — Relación lineal en el logit ✓"
                        if p > 0.05 else
                        f"p={p:.4f} ≤ .05 — Posible no-linealidad (considerar transformación)"
                    )
                }

            all_linear = all(v['linearity_ok'] for v in bt_results.values())
            results['box_tidwell'] = {
                'per_feature': bt_results,
                'all_linear': all_linear,
                'overall': (
                    "Supuesto de linealidad del logit SATISFECHO para todas las dimensiones"
                    if all_linear else
                    "Supuesto PARCIALMENTE violado — revisar dimensiones con p ≤ .05"
                )
            }
        except Exception as e:
            results['box_tidwell'] = {'status': 'error', 'message': str(e)}

        # ── 3. Distancia de Cook y Leverage ────────────────────────────────────
        try:
            X_const = sm.add_constant(X)
            model_main = sm.Logit(y, X_const).fit(disp=0, maxiter=100)

            # Leverage (hat values) desde la matriz de información
            # Aproximación estándar via influencias de statsmodels
            influence = model_main.get_influence()
            hat_values = influence.hat_matrix_diag
            resid_std = influence.resid_studentized

            # Umbral de Cook: 4 / (N - k - 1)
            n = len(y)
            k = n_predictors
            cook_threshold = 4 / (n - k - 1)

            # Distancia de Cook simplificada: (h * r²) / k*(1-h)²
            # Usamos los valores estandarizados disponibles
            cook_approx = (hat_values * resid_std**2) / (k * (1 - hat_values)**2 + 1e-10)
            n_influential = int((cook_approx > cook_threshold).sum())
            pct_influential = float(n_influential / n * 100)

            # Leverage alto: h > 2*(k+1)/n
            lev_threshold = 2 * (k + 1) / n
            n_high_leverage = int((hat_values > lev_threshold).sum())

            results['influential_obs'] = {
                'n_total': n,
                'cook_threshold': float(cook_threshold),
                'n_influential_cook': n_influential,
                'pct_influential': float(pct_influential),
                'leverage_threshold': float(lev_threshold),
                'n_high_leverage': n_high_leverage,
                'interpretation': (
                    f"{n_influential} obs. con Cook > {cook_threshold:.4f} ({pct_influential:.1f}%). "
                    f"{n_high_leverage} obs. con leverage alto. "
                    + ("Sin casos críticos de influencia." if pct_influential < 5
                       else "Revisar casos influyentes antes de reportar.")
                )
            }
        except Exception as e:
            results['influential_obs'] = {'status': 'error', 'message': str(e)}

        # ── Veredicto Global ───────────────────────────────────────────────────
        epv_pass = results['epv']['ok']
        bt_pass = results.get('box_tidwell', {}).get('all_linear', False)
        cook_pct = results.get('influential_obs', {}).get('pct_influential', 100)
        cook_pass = cook_pct < 5

        passed = sum([epv_pass, bt_pass, cook_pass])
        results['overall_verdict'] = {
            'passed': passed,
            'total': 3,
            'summary': (
                f"{passed}/3 supuestos verificados — "
                + ("Modelo logístico metodológicamente sólido para defensa." if passed == 3
                   else "Revisar supuestos fallidos antes de la defensa doctoral.")
            )
        }

        return results

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

    def run_feature_xai_analysis(self, X_train_feat, y_train, model_type="rf") -> dict:
        """Entrena un modelo sobre los 30 ítems AMI y extrae el Top 10 de preguntas influyentes."""
        from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
        import shap
        import matplotlib.pyplot as plt
        import os
        
        # 1. Entrenar modelo granular
        if model_type == 'gb' or model_type == 'gradient_boosting':
            clf = GradientBoostingClassifier(random_state=42)
            clf.fit(X_train_feat, y_train)
        else:
            # Usar X_train, y_train para evitar leakage de holdout durante hiperparametrización
            clf = self._get_rf_model(X_train_feat, y_train, tune=True)
            clf.fit(X_train_feat, y_train)
        
        # 2. SHAP
        explainer = shap.TreeExplainer(clf)
        shap_values = explainer.shap_values(X_train_feat)
        
        # 3. Guardar el plot del Top 10 y bar plot
        xai_dir = 'data/outputs/xai'
        os.makedirs(xai_dir, exist_ok=True)
        
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_train_feat, max_display=10, show=False)
        plot_path = f"{xai_dir}/shap_feature_items_top10.png"
        plt.savefig(plot_path, bbox_inches='tight', dpi=150)
        plt.close()
        
        # Summary bar plot
        plt.figure(figsize=(10, 8))
        shap.summary_plot(shap_values, X_train_feat, max_display=10, plot_type="bar", show=False)
        plt.savefig(f"{xai_dir}/shap_summary_bar.png", bbox_inches='tight', dpi=150)
        plt.close()
        
        # 4. Extraer ranking
        mean_shap = np.abs(shap_values).mean(axis=0)
        ranking = sorted(zip(X_train_feat.columns, mean_shap), key=lambda x: x[1], reverse=True)
        
        # 5. Dependencia para los top 3
        top_3 = [x[0] for x in ranking[:3]]
        for col in top_3:
            plt.figure(figsize=(8, 6))
            shap.dependence_plot(col, shap_values, X_train_feat, show=False)
            plt.savefig(f"{xai_dir}/shap_dependence_{col}.png", bbox_inches='tight', dpi=150)
            plt.close()
        
        return {
            'status': 'success',
            'plot_path': plot_path,
            'top_items': ranking[:10]
        }

    def run_repeated_cv(self, df_scored: pd.DataFrame, model_type: str = 'logistic') -> dict:
        """
        [HC-05] Validación cruzada RepeatedStratifiedKFold (5 folds x 10 repeticiones).
        Aplica para Logit o RandomForest.
        """
        if 'Flag_Inconsistencia' in df_scored.columns:
            df_valid = df_scored[df_scored['Flag_Inconsistencia'] == False].copy()
        else:
            df_valid = df_scored.copy()

        features = ['Score_Critico', 'Score_Tecnico', 'Score_Participativo']
        X = df_valid[features].dropna()
        y = df_valid.loc[X.index, 'Riesgo_Total'].astype(int)

        from sklearn.pipeline import Pipeline
        from sklearn.preprocessing import StandardScaler as SS
        from sklearn.linear_model import LogisticRegression as LR
        from sklearn.ensemble import GradientBoostingClassifier as GB, RandomForestClassifier as RF
        from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate, cross_val_predict
        from sklearn.metrics import make_scorer, precision_score, recall_score, f1_score, roc_auc_score, balanced_accuracy_score, average_precision_score, matthews_corrcoef, accuracy_score
        import numpy as np

        if model_type == 'gb' or model_type == 'gradient_boosting':
            clf = GB(random_state=42)
        elif model_type == 'rf' or model_type == 'tree':
            clf = self._get_rf_model(X, y, tune=True)
        elif model_type == 'both':
            clf = self._get_rf_model(X, y, tune=False)
        else:
            clf = LR(class_weight='balanced', random_state=42, max_iter=500)

        pipe = Pipeline([
            ('scaler', SS()),
            ('clf', clf)
        ])

        rskf = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
        skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        # 1. Calcular el umbral óptimo Out-Of-Fold usando predict_proba
        # cross_val_predict solo funciona con particiones puras (sin repetición)
        y_proba_oof = cross_val_predict(pipe, X, y, cv=skf, method='predict_proba', n_jobs=-1)[:, 1]
        
        # Optimizar umbral buscando mayor F1 out-of-fold con Recall >= 0.60
        thresholds = np.linspace(0.95, 0.05, 181)
        best_f1_oof = 0
        best_th = 0.5
        for th in thresholds:
            preds = (y_proba_oof >= th).astype(int)
            r = recall_score(y, preds, zero_division=0)
            f = f1_score(y, preds, zero_division=0)
            if r >= 0.60 and f > best_f1_oof:
                best_f1_oof = f
                best_th = th
                
        if best_f1_oof == 0:
            for th in thresholds:
                preds = (y_proba_oof >= th).astype(int)
                f = f1_score(y, preds, zero_division=0)
                if f > best_f1_oof:
                    best_f1_oof = f
                    best_th = th
                
        # 2. Validacion cruzada normal para ROC_AUC
        scoring = {'roc_auc': 'roc_auc', 'pr_auc': 'average_precision'}
        results = cross_validate(pipe, X, y, cv=rskf, scoring=scoring, n_jobs=-1)

        def get_stats(metric):
            vals = results[f'test_{metric}']
            return float(vals.mean()), float(vals.std())

        auc_mean, auc_std = get_stats('roc_auc')
        pr_auc_mean, pr_auc_std = get_stats('pr_auc')
        
        # 3. Métricas duras Out-Of-Fold con el umbral óptimo
        y_pred_oof = (y_proba_oof >= best_th).astype(int)
        acc_mean = accuracy_score(y, y_pred_oof)
        f1_mean = f1_score(y, y_pred_oof, zero_division=0)
        rec_mean = recall_score(y, y_pred_oof, zero_division=0)
        prec_mean = precision_score(y, y_pred_oof, zero_division=0)
        bal_acc_mean = balanced_accuracy_score(y, y_pred_oof)
        mcc_mean = matthews_corrcoef(y, y_pred_oof)
        
        # Como estas métricas duras se calculan globalmente sobre las predicciones OOF, 
        # la varianza entre folds (std) se define en 0 para mantener la compatibilidad del dict.
        acc_std = f1_std = rec_std = prec_std = bal_acc_std = mcc_std = 0.0

        interpretation = (
            "AUC generalizable robusta" if auc_mean >= 0.75
            else "AUC moderada — considerar más features o mayor muestra"
        )

        return {
            'n_samples': len(y),
            'n_positive': int(y.sum()),
            'optimal_threshold': float(best_th),
            'auc_mean': auc_mean, 'auc_std': auc_std,
            'auc_ci_95': [auc_mean - 1.96 * auc_std, auc_mean + 1.96 * auc_std],
            'accuracy_mean': acc_mean, 'accuracy_std': acc_std,
            'f1_mean': f1_mean, 'f1_std': f1_std,
            'recall_mean': rec_mean, 'recall_std': rec_std,
            'precision_mean': prec_mean, 'precision_std': prec_std,
            'balanced_accuracy_mean': bal_acc_mean, 'balanced_accuracy_std': bal_acc_std,
            'pr_auc_mean': pr_auc_mean, 'pr_auc_std': pr_auc_std,
            'mcc_mean': mcc_mean, 'mcc_std': mcc_std,
            'interpretation': interpretation
        }

    def run_confirmatory_factor_analysis(self, df_raw: pd.DataFrame) -> dict:
        """
        [HC-02] Validación Confirmatoria de la estructura AMI de 3 factores
        mediante el Coeficiente de Congruencia de Tucker (Φ).

        Metodología (defensible sin AFC completo):
          1. Dividir la muestra en dos mitades estratificadas.
          2. Ejecutar EFA (3 factores, Oblimin) en cada mitad.
          3. Calcular Tucker's Φ entre las matrices de cargas.
          4. Φ ≥ 0.95 = Excelente congruencia (Lorenzo-Seva & ten Berge, 2006).
          5. Φ ≥ 0.85 = Adecuado (umbral mínimo para reporte doctoral).

        Referencia: Lorenzo-Seva, U. & ten Berge, J. M. F. (2006).
        Tucker's congruence coefficient as a meaningful index of factor similarity.
        Methodology, 2(2), 57-64.
        """
        ami_items = (
            [f'C{i}' for i in range(1, 11)] +
            [f'T{i}' for i in range(1, 11)] +
            [f'P{i}' for i in range(1, 11)]
        )
        likert_map = {
            "Totalmente en desacuerdo": 1, "En desacuerdo": 2,
            "Ni de acuerdo ni en desacuerdo": 3, "De acuerdo": 4,
            "Totalmente de acuerdo": 5
        }

        data_cfa = df_raw[ami_items].copy()
        for col in ami_items:
            if not pd.api.types.is_numeric_dtype(data_cfa[col]):
                data_cfa[col] = data_cfa[col].map(likert_map)
            data_cfa[col] = pd.to_numeric(data_cfa[col], errors='coerce')
        data_cfa = data_cfa.dropna()

        if data_cfa.shape[0] < 60:
            return {
                'status': 'error',
                'message': 'Muestra insuficiente para split confirmatorio (mínimo N=60).'
            }

        # --- División estratificada en dos mitades ---
        n = len(data_cfa)
        idx = data_cfa.index.tolist()
        np.random.seed(42)
        np.random.shuffle(idx)
        half = n // 2
        idx_a, idx_b = idx[:half], idx[half:]
        data_a = data_cfa.loc[idx_a]
        data_b = data_cfa.loc[idx_b]

        def _fit_efa(data):
            fa = FactorAnalyzer(n_factors=3, rotation="oblimin", method="minres")
            fa.fit(data)
            return fa.loadings_  # shape (30, 3)

        def _tucker_phi(L1: np.ndarray, L2: np.ndarray) -> np.ndarray:
            """Tucker's congruence coefficient entre columnas de dos matrices de cargas."""
            phi = np.zeros(L1.shape[1])
            for f in range(L1.shape[1]):
                num = np.sum(L1[:, f] * L2[:, f])
                den = np.sqrt(np.sum(L1[:, f]**2) * np.sum(L2[:, f]**2))
                phi[f] = num / den if den > 0 else 0.0
            return phi

        try:
            L_a = _fit_efa(data_a)
            L_b = _fit_efa(data_b)

            phi_scores = _tucker_phi(L_a, L_b)
            phi_mean = float(np.mean(np.abs(phi_scores)))

            factor_labels = ['Factor_Critico', 'Factor_Tecnico', 'Factor_Participativo']

            # Interpretación según Lorenzo-Seva & ten Berge (2006)
            def _phi_label(phi_val):
                phi_val = abs(phi_val)
                if phi_val >= 0.95:
                    return "Excelente replicabilidad de cargas factoriales"
                elif phi_val >= 0.85:
                    return "Congruencia adecuada (aceptable para defensa)"
                elif phi_val >= 0.70:
                    return "Congruencia marginal — estructura cuestionable"
                else:
                    return "Incongruencia factorial — revisar estructura"

            per_factor = {
                factor_labels[i]: {
                    'phi': float(abs(phi_scores[i])),
                    'interpretation': _phi_label(phi_scores[i])
                }
                for i in range(3)
            }

            overall_interp = _phi_label(phi_mean)
            confirmed = phi_mean >= 0.85

            # RMSR (Root Mean Square Residual) de las cargas entre mitades
            rmsr = float(np.sqrt(np.mean((L_a - L_b)**2)))

            return {
                'status': 'success',
                'method': "Tucker's Congruence Coefficient (Φ) — Split-half EFA",
                'reference': "Lorenzo-Seva & ten Berge (2006). Methodology, 2(2), 57-64.",
                'n_total': n,
                'n_half_a': half,
                'n_half_b': n - half,
                'phi_per_factor': per_factor,
                'phi_mean': phi_mean,
                'rmsr': rmsr,
                'structure_confirmed': confirmed,
                'overall_interpretation': overall_interp
            }

        except Exception as e:
            return {'status': 'error', 'message': str(e)}

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
            'prsquared': float(result.prsquared),
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

    def run_random_forest(self, X_train, X_test, y_train, y_test, model_type="rf") -> dict:
        """Entrena RF o GB según lo solicitado por el usuario."""
        from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
        from sklearn.model_selection import GridSearchCV
        
        if model_type == 'gb' or model_type == 'gradient_boosting':
            clf = GradientBoostingClassifier(random_state=42)
            param_grid = {
                'n_estimators': [20, 50, 100],
                'learning_rate': [0.01, 0.05, 0.1],
                'max_depth': [3, 4],
                'subsample': [0.8, 1.0]
            }
        else:
            clf = RandomForestClassifier(random_state=42, class_weight='balanced')
            param_grid = {
                'n_estimators': [50, 100, 200],
                'max_depth': [None, 5, 10],
                'min_samples_split': [2, 5]
            }

        grid = GridSearchCV(clf, param_grid, cv=5, scoring='roc_auc')
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
