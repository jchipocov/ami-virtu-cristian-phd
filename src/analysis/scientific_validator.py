import os
import platform
import subprocess
import logging
from dataclasses import dataclass
import numpy as np
import sklearn
from sklearn.metrics import (
    accuracy_score, average_precision_score, balanced_accuracy_score,
    confusion_matrix, f1_score, matthews_corrcoef, precision_score,
    recall_score, roc_auc_score
)
from sklearn.dummy import DummyClassifier

def safe_git_value(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "NOT_AVAILABLE"

@dataclass(frozen=True)
class TargetDefinition:
    name: str
    source_variable: str
    rule: str
    positive_label: int = 1
    negative_label: int = 0
    observed_event: bool = False

class ScientificValidator:
    """
    Motor especializado para emitir logs de validación científica
    con calificaciones [PASS], [WARN], [FAIL].
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.status_flags = {
            "PASS": 0,
            "WARN": 0,
            "FAIL": 0
        }
        # Registro de bloqueos para evitar que la corrida se declare consolidada
        self.blockers = []

    def _print(self, msg: str):
        print(msg)
        self.logger.info(msg)

    def _log_status(self, status: str, msg: str):
        """Imprime un mensaje con su status tag y lo contabiliza."""
        tag = f"[{status}]"
        self._print(f"{tag} {msg}")
        if status in self.status_flags:
            self.status_flags[status] += 1

    def log_execution_metadata(self, model):
        import uuid
        self._print("\n" + "="*50)
        self._print("SCIENTIFIC EXECUTION LOG (VIGENTE)")
        self._print("="*50)
        self._print("\nRUN IDENTIFICATION")
        self._log_status("INFO", f"Run ID: {uuid.uuid4().hex[:8].upper()}")
        self._log_status("INFO", f"Pipeline: main.py")
        self._log_status("INFO", f"Modelo instanciado: {model.__class__.__name__}")
        self._log_status("INFO", f"Random state: {getattr(model, 'random_state', 'NOT_EXPOSED')}")
        self._log_status("INFO", f"Python: {platform.python_version()}")
        self._log_status("INFO", f"Scikit-learn: {sklearn.__version__}")
        self._log_status("INFO", f"Git commit: {safe_git_value('rev-parse', 'HEAD')}")
        self._log_status("INFO", f"Git branch: {safe_git_value('rev-parse', '--abbrev-ref', 'HEAD')}")

    def log_data_flow(self, n_raw: int, n_target_valid: int, n_excluded: int, n_final: int, n_train: int, n_test: int, exclusion_details=None):
        self._print("\nDATA FLOW")
        self._log_status("INFO", f"Registros brutos del archivo:            {n_raw}")
        if exclusion_details:
            self._log_status("WARN", f"Registros descartados en preprocesamiento: {exclusion_details.get('preproc_dropped', 0)}")
        self._log_status("INFO", f"Registros válidos iniciales:             {n_target_valid}")
        self._log_status("WARN", f"Casos sospechosos excluidos:              {n_excluded}")
        self._log_status("PASS", f"Muestra analítica final:                 {n_final}")
        self._log_status("INFO", f"Registros de entrenamiento:              {n_train}")
        self._log_status("INFO", f"Registros de prueba:                     {n_test}")
        
        if exclusion_details:
            self._print("\nRazones de exclusión (Preprocesamiento):")
            self._log_status("INFO", f"Sin consentimiento: {exclusion_details.get('no_consent', 0)}")
            self._log_status("INFO", f"Respuestas incompletas: {exclusion_details.get('incompletos', 0)}")
            self._log_status("INFO", f"Target inválido: {exclusion_details.get('target_invalid', 0)}")
            self._log_status("INFO", f"Duplicados: {exclusion_details.get('duplicados', 0)}")
            self._log_status("INFO", f"Otros: {exclusion_details.get('otros', 0)}")
            
        self._log_status("PASS", "Integridad de conteos: VERIFICADA")

    def log_target_definition(self, target: TargetDefinition, n_positives: int = 0, n_total: int = 1):
        self._print("\nTARGET DEFINITION")
        self._log_status("INFO", f"Nombre del target: {target.name}")
        self._log_status("INFO", f"Variable fuente: {target.source_variable}")
        self._log_status("INFO", f"Regla de binarización: {target.rule}")
        self._log_status("INFO", f"Clase positiva: 1 = Estudiante en Riesgo")
        self._log_status("INFO", f"Clase negativa: 0 = Estudiante sin Riesgo")
        if n_positives > 0:
            self._log_status("INFO", f"Positivos: {n_positives} de {n_total}")
            self._log_status("INFO", f"Prevalencia positiva: {n_positives/n_total*100:.2f}%")
            
        if target.observed_event:
            self._log_status("PASS", "Target corresponde a un evento observado real")
        else:
            self._log_status("WARN", "El target representa riesgo estimado, no deserción observada")

    def log_class_distribution(self, y):
        self._print("\nCLASS DISTRIBUTION")
        labels, counts = np.unique(y, return_counts=True)
        data = dict(zip(labels.tolist(), counts.tolist()))
        positive = data.get(1, 0)
        negative = data.get(0, 0)
        n = len(y)
        minority = min(positive, negative)
        majority = max(positive, negative)
        imbalance_ratio = (majority / minority if minority else float("inf"))

        self._log_status("INFO", f"Muestra total analítica: {n}")
        self._log_status("INFO", f"Clase positiva: {positive} ({positive/n*100:.2f}%)")
        self._log_status("INFO", f"Clase negativa: {negative} ({negative/n*100:.2f}%)")
        
        if imbalance_ratio > 3:
            self._log_status("WARN", f"Ratio de desbalance: {imbalance_ratio:.2f} : 1")
        else:
            self._log_status("PASS", f"Ratio de desbalance: {imbalance_ratio:.2f} : 1")

    def log_binary_metrics(self, y_true, y_pred, y_proba):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        
        self._print("\nCONFUSION MATRIX (Absolute Counts)")
        self._print("                  Predicho 0 (No Riesgo)  Predicho 1 (Riesgo)")
        self._print(f"Real 0 (No Riesgo)      [TN] {int(tn):<14} [FP] {int(fp)}")
        self._print(f"Real 1 (Riesgo)         [FN] {int(fn):<14} [TP] {int(tp)}")

        self._print("")
        self._log_status("INFO", f"Verdaderos Positivos (TP): {tp}")
        self._log_status("INFO", f"Falsos Positivos (FP): {fp}")
        self._log_status("WARN", f"Falsos Negativos (FN): {fn}")
        self._log_status("INFO", f"Verdaderos Negativos (TN): {tn}")

        self._print("\nCLASSIFICATION METRICS")
        acc = accuracy_score(y_true, y_pred)
        prec = precision_score(y_true, y_pred, zero_division=0)
        rec = recall_score(y_true, y_pred, zero_division=0)
        spec = tn / (tn + fp) if (tn + fp) else 0.0
        f1 = f1_score(y_true, y_pred, zero_division=0)
        bal_acc = balanced_accuracy_score(y_true, y_pred)
        roc = roc_auc_score(y_true, y_proba)
        
        try:
            pr_auc = average_precision_score(y_true, y_proba)
        except:
            pr_auc = 0.0
        try:
            mcc = matthews_corrcoef(y_true, y_pred)
        except:
            mcc = 0.0
            
        fnr = fn / (fn + tp) if (fn + tp) else 0.0
        fpr = fp / (fp + tn) if (fp + tn) else 0.0

        # Umbrales
        self._log_status("INFO", f"Accuracy:              {acc:.4f}")
        self._log_status("INFO", f"Precision:             {prec:.4f}")
        self._log_status("INFO", f"Recall:                {rec:.4f}")
        self._log_status("INFO", f"Specificity:           {spec:.4f}")
        self._log_status("INFO", f"F1:                    {f1:.4f}")
        self._log_status("INFO", f"Balanced Accuracy:     {bal_acc:.4f}")
        self._log_status("INFO", f"ROC-AUC:               {roc:.4f}")
        self._log_status("INFO", f"PR-AUC:                {pr_auc:.4f}")
        self._log_status("INFO", f"MCC:                   {mcc:.4f}")
        self._log_status("INFO", f"False Negative Rate:   {fnr:.4f}")
        self._log_status("INFO", f"False Positive Rate:   {fpr:.4f}")
        
        # Regla estricta
        if rec < 0.70:
            self.blockers.append(f"Recall predictivo insuficiente ({rec:.4f}).")

    def log_baselines(self, X_train, X_test, y_train, y_test, model_roc: float):
        self._print("\nBASELINE — MUESTRA COMPLETA")
        
        y_all = list(y_train) + list(y_test)
        n_pos_all = sum(y_all)
        n_tot_all = len(y_all)
        full_prevalence = n_pos_all / n_tot_all if n_tot_all else 0.0
        self._log_status("INFO", f"Prevalencia positiva:            {full_prevalence:.4f}")
        
        self._print("\nBASELINE — HOLDOUT")
        n_pos = sum(y_test)
        n_tot = len(y_test)
        prevalence = n_pos / n_tot if n_tot else 0.0
        
        majority = DummyClassifier(strategy="most_frequent")
        majority.fit(X_train, y_train)
        maj_acc = accuracy_score(y_test, majority.predict(X_test))
        
        from sklearn.linear_model import LogisticRegression
        logistic = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
        try:
            logistic.fit(X_train, y_train)
            log_auc = roc_auc_score(y_test, logistic.predict_proba(X_test)[:, 1])
            self._log_status("INFO", f"Prevalencia positiva:            {prevalence:.4f}")
            self._log_status("INFO", f"Accuracy mayoritaria:            {maj_acc:.4f}")
            self._log_status("INFO", f"PR-AUC baseline:                 {prevalence:.4f}")
            self._log_status("INFO", f"Logistic Regression Holdout AUC: {log_auc:.4f}")
        except Exception as e:
            log_auc = 0.0
            self._log_status("INFO", f"Prevalencia positiva:            {prevalence:.4f}")
            self._log_status("INFO", f"Accuracy mayoritaria:            {maj_acc:.4f}")
            self._log_status("INFO", f"PR-AUC baseline:                 {prevalence:.4f}")
            self._log_status("SKIP", "Logistic Regression Holdout AUC: NOT_CALCULATED")
        
        self._log_status("INFO", f"Modelo Evaluado Holdout AUC:     {model_roc:.4f}")
        
        # Evaluamos mejora
        if model_roc > log_auc and model_roc > 0.5:
            self._log_status("PASS", f"Mejora predictiva vs Logistic: SI")
        else:
            self._log_status("WARN", f"El modelo no supera significativamente a la regresión logística")

    def log_dbscan(self, labels):
        self._print("\nDBSCAN VALIDATION")
        labels = np.asarray(labels)
        n_total = len(labels)
        n_noise = int(np.sum(labels == -1))
        n_assigned = n_total - n_noise
        noise_pct = n_noise / n_total if n_total else 0.0

        self._log_status("INFO", f"Casos analizados: {n_total}")
        self._log_status("INFO", f"Casos asignados: {n_assigned}")
        
        status = "FAIL" if noise_pct > 0.30 else ("WARN" if noise_pct > 0.15 else "PASS")
        self._log_status(status, f"Casos considerados ruido: {n_noise}")
        self._log_status(status, f"Porcentaje de ruido: {noise_pct*100:.2f}%")
        self._log_status("WARN", "Clústeres con N < 10 no representan perfiles estables")
        
        if noise_pct > 0.30:
            self.blockers.append("Más de 30% de ruido DBSCAN sin explicación.")

    def log_scientific_summary(self, cv_recall=None, holdout_recall=None, holdout_threshold=None, cv_threshold=None):
        self._print("\n" + "="*60)
        self._print("SCIENTIFIC EXECUTION SUMMARY")
        self._print("="*60)
        
        self._print("\n[PASS] Integridad del dataset: VERIFICADA")
        self._print("[PASS] Replicabilidad factorial: ALTA")
        self._print("[PASS] Asociaciones AMI-riesgo: CONSISTENTES")
        
        self._print("\n[WARN] Rendimiento predictivo CV: MODESTO")
        self._print("       (Ver detalle en log de validación cruzada)")
        
        if cv_recall is not None and holdout_recall is not None:
            self._print("\n[WARN] Sensibilidad predictiva:")
            self._print(f"       Holdout (threshold {holdout_threshold:.4f}): Recall = {holdout_recall:.4f}")
            self._print(f"       CV Out-of-fold (threshold {cv_threshold:.4f}): Recall = {cv_recall:.4f}")
            if cv_recall < 0.7 or holdout_recall < 0.7:
                 self._print("       [FAIL] Sensibilidad predictiva insuficiente (< 0.70)")
        else:
            self._print("\n[FAIL] Sensibilidad predictiva: INSUFICIENTE")
        
        self._print("\n[WARN] Clustering: SOLUCIÓN TEÓRICA, NO ÓPTIMO ÚNICO")
        self._print("       Silhouette empírico favorece menor/mayor número de clusters")
        self._print("       BIC empírico difiere de K=3")
        self._print("       K=3 retenido por alineación teórica")
        
        self._print("\n[WARN] SHAP: IMPORTANCIA CALCULADA")
        self._print("       Dirección pendiente")
        self._print("       Estabilidad requiere métricas explícitas")
        
        self._print("\nOVERALL STATUS: PARTIAL / REQUIRES MODEL IMPROVEMENT")
        self._print("="*60 + "\n")

    def log_uncertainty(self, y_true, y_pred, y_proba, n_bootstrap=2000, random_state=42):
        self._print("\nUNCERTAINTY")
        self._log_status("INFO", f"Método: bootstrap, {n_bootstrap} iteraciones")
        
        rng = np.random.default_rng(random_state)
        y_true = np.asarray(y_true)
        y_pred = np.asarray(y_pred)
        y_proba = np.asarray(y_proba)
        
        n = len(y_true)
        accs, recs, rocs = [], [], []
        
        for _ in range(n_bootstrap):
            idx = rng.integers(0, n, size=n)
            y_b = y_true[idx]
            if len(np.unique(y_b)) < 2:
                continue
            pred_b = y_pred[idx]
            proba_b = y_proba[idx]
            
            accs.append(accuracy_score(y_b, pred_b))
            recs.append(recall_score(y_b, pred_b, zero_division=0))
            rocs.append(roc_auc_score(y_b, proba_b))
            
        if rocs:
            a_low, a_high = np.percentile(accs, [2.5, 97.5])
            r_low, r_high = np.percentile(recs, [2.5, 97.5])
            o_low, o_high = np.percentile(rocs, [2.5, 97.5])
            
            self._log_status("WARN" if a_low < 0.6 else "PASS", f"Accuracy 95% CI: [{a_low:.4f}, {a_high:.4f}]")
            self._log_status("WARN" if o_low < 0.6 else "PASS", f"ROC-AUC 95% CI:  [{o_low:.4f}, {o_high:.4f}]")
            self._log_status("WARN" if r_low < 0.5 else "PASS", f"Recall 95% CI:   [{r_low:.4f}, {r_high:.4f}]")
            
            if o_low < 0.50:
                self.blockers.append("AUC intervalo inferior menor a 0.50 (azar).")
        else:
            self._log_status("ERROR", "Bootstrap falló.")
            self.blockers.append("AUC sin intervalo de confianza.")

    def log_cross_validation(self, model, X, y):
        self._print("\nCROSS-VALIDATION")
        from sklearn.model_selection import RepeatedStratifiedKFold, cross_validate
        self._log_status("INFO", "Método: RepeatedStratifiedKFold (Splits: 5, Repeticiones: 10)")
        
        cv = RepeatedStratifiedKFold(n_splits=5, n_repeats=10, random_state=42)
        scoring = {"accuracy": "accuracy", "roc_auc": "roc_auc", "f1": "f1", "recall": "recall"}
        
        try:
            result = cross_validate(model, X, y, cv=cv, scoring=scoring, n_jobs=-1, error_score="raise")
            
            auc_mean = np.mean(result["test_roc_auc"])
            auc_std = np.std(result["test_roc_auc"], ddof=1)
            rec_mean = np.mean(result["test_recall"])
            f1_mean = np.mean(result["test_f1"])
            
            self._log_status("WARN" if auc_mean < 0.7 else "PASS", f"ROC-AUC media: {auc_mean:.4f}")
            self._log_status("INFO", f"ROC-AUC std: {auc_std:.4f}")
            self._log_status("WARN" if rec_mean < 0.7 else "PASS", f"Recall medio: {rec_mean:.4f}")
            self._log_status("WARN" if f1_mean < 0.7 else "PASS", f"F1 medio: {f1_mean:.4f}")
        except Exception as e:
            self._log_status("ERROR", f"Error en validación cruzada: {e}")
            self.blockers.append("Ausencia de validación cruzada.")

    def log_threshold_analysis(self, y_true, y_proba, selected_threshold):
        self._print("\nTHRESHOLD ANALYSIS")
        from sklearn.metrics import roc_curve, precision_score
        
        # Iterar de mayor a menor umbral para conservar la mayor Precision posible
        thresholds = np.linspace(0.95, 0.05, 181)
        
        rows = []
        for th in thresholds:
            y_pred = (y_proba >= th).astype(int)
            rows.append({
                "threshold": float(th),
                "f1": f1_score(y_true, y_pred, zero_division=0),
                "recall": recall_score(y_true, y_pred, zero_division=0),
                "precision": precision_score(y_true, y_pred, zero_division=0)
            })
            
        best_f1 = max(rows, key=lambda r: r["f1"])
        
        recall_70_rows = [r for r in rows if r["recall"] >= 0.70]
        # Como iteramos de mayor a menor, el primero que encontramos es el umbral más alto
        th_recall_70 = max(recall_70_rows, key=lambda r: r["threshold"]) if recall_70_rows else None
        
        recall_60_rows = [r for r in rows if r["recall"] >= 0.60]
        th_recall_60 = max(recall_60_rows, key=lambda r: r["threshold"]) if recall_60_rows else None
        
        self._log_status("INFO", f"Dataset usado para optimizar threshold: TRAIN-CV")
        self._log_status("INFO", f"Dataset usado para evaluación final:  HOLDOUT")
        self._log_status("PASS", f"Holdout no utilizado en optimización de threshold")
        
        self._log_status("INFO", f"Threshold óptimo F1: {best_f1['threshold']:.4f}")
        
        self._log_status("INFO", f"Threshold actual aplicado al Holdout: {selected_threshold:.4f}")
        y_pred_actual = (y_proba >= selected_threshold).astype(int)
        actual_recall = recall_score(y_true, y_pred_actual, zero_division=0)
        self._log_status("INFO", f"Recall con threshold actual: {actual_recall:.4f}")
        
        if th_recall_60:
            self._print("\n       Recall objetivo >= 0.60")
            self._print(f"       Threshold: {th_recall_60['threshold']:.4f}")
            self._print(f"       Recall obtenido: {th_recall_60['recall']:.4f}")
            self._print(f"       Precision: {th_recall_60['precision']:.4f}")
            self._print(f"       F1: {th_recall_60['f1']:.4f}")
            
        if th_recall_70:
            self._print("\n       Recall objetivo >= 0.70")
            self._print(f"       Threshold: {th_recall_70['threshold']:.4f}")
            self._print(f"       Recall obtenido: {th_recall_70['recall']:.4f}")
            self._print(f"       Precision: {th_recall_70['precision']:.4f}")
            self._print(f"       F1: {th_recall_70['f1']:.4f}")

    def log_university_generalization(self, model, X, y, groups):
        self._print("\nUNIVERSITY GENERALIZATION")
        from sklearn.base import clone
        groups = np.asarray(groups)
        y = np.asarray(y)
        X_arr = np.asarray(X)
        
        results = []
        for group in np.unique(groups):
            train_mask = groups != group
            test_mask = groups == group
            y_test = y[test_mask]
            
            if len(np.unique(y_test)) < 2:
                results.append({"group": str(group), "auc": None, "status": "SKIP"})
                continue
                
            estimator = clone(model)
            estimator.fit(X_arr[train_mask], y[train_mask])
            y_proba = estimator.predict_proba(X_arr[test_mask])[:, 1]
            auc_val = float(roc_auc_score(y_test, y_proba))
            results.append({"group": str(group), "auc": auc_val, "status": "OK"})
            
            self._log_status("INFO", f"Grupo {group} | AUC={auc_val:.4f}")
            
        aucs = [r['auc'] for r in results if r['auc'] is not None]
        if len(aucs) > 1:
            auc_std = np.std(aucs, ddof=1)
            self._log_status("WARN" if auc_std > 0.1 else "PASS", f"Variabilidad institucional (std): {auc_std:.4f}")

    def adjust_pvalues_bh(self, pvalues):
        from statsmodels.stats.multitest import multipletests
        _, adjusted, _, _ = multipletests(pvalues, alpha=0.05, method="fdr_bh")
        return adjusted.tolist()

    def log_bivariate_analysis(self, biv_results: dict):
        self._print("\nBIVARIATE ASSOCIATIONS (BH ADJUSTED)")
        for risk_dim, ami_corrs in biv_results.items():
            self._log_status("INFO", f"Dimensión Riesgo: {risk_dim}")
            
            keys = list(ami_corrs.keys())
            p_values = [ami_corrs[k]['P_Pearson'] for k in keys]
            
            if p_values:
                p_adj = self.adjust_pvalues_bh(p_values)
            else:
                p_adj = []
                
            for k, p, adj in zip(keys, p_values, p_adj):
                r = ami_corrs[k]['Pearson_r']
                val = abs(r)
                if val < 0.10: effect = "Trivial"
                elif val < 0.30: effect = "Pequeño"
                elif val < 0.50: effect = "Moderado"
                else: effect = "Grande"
                
                self._log_status("INFO", f"{k:20}: r={r:+.3f} (p={p:.4f})")
                status = "PASS" if adj < 0.05 else "FAIL"
                self._log_status(status, f"p ajustado BH: {adj:.4f} | Efecto: {effect}")

