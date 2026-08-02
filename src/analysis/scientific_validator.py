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
        self._print("\n" + "="*50)
        self._print("SCIENTIFIC EXECUTION LOG")
        self._print("="*50)
        self._print("\nRUN IDENTIFICATION")
        self._log_status("INFO", f"Pipeline: main.py")
        self._log_status("INFO", f"Modelo instanciado: {model.__class__.__name__}")
        self._log_status("INFO", f"Random state: {getattr(model, 'random_state', 'NOT_EXPOSED')}")
        self._log_status("INFO", f"Python: {platform.python_version()}")
        self._log_status("INFO", f"Scikit-learn: {sklearn.__version__}")
        self._log_status("INFO", f"Git commit: {safe_git_value('rev-parse', 'HEAD')}")
        self._log_status("INFO", f"Git branch: {safe_git_value('rev-parse', '--abbrev-ref', 'HEAD')}")

    def log_data_flow(self, n_raw: int, n_target_valid: int, n_excluded: int, n_final: int, n_train: int, n_test: int):
        self._print("\nDATA FLOW")
        self._log_status("INFO", f"Registros originales:          {n_raw}")
        self._log_status("INFO", f"Registros con target válido:   {n_target_valid}")
        self._log_status("INFO", f"Casos excluidos:               {n_excluded}")
        self._log_status("PASS", f"Muestra analítica final:       {n_final}")
        self._log_status("INFO", f"Train:                         {n_train}")
        self._log_status("INFO", f"Test:                          {n_test}")
        
        errors = []
        if n_target_valid > n_raw:
            errors.append("n_target_valid no puede superar n_raw")
        if n_final != n_target_valid - n_excluded:
            errors.append("n_final debe ser n_target_valid - n_excluded")
        if n_train + n_test != n_final:
            errors.append("n_train + n_test debe ser igual a n_final")

        if errors:
            self._log_status("FAIL", "Integridad de conteos: ROTA (" + " | ".join(errors) + ")")
        else:
            self._log_status("PASS", "Integridad de conteos: VERIFICADA")

    def log_target_definition(self, target: TargetDefinition):
        self._print("\nTARGET DEFINITION")
        self._log_status("INFO", f"Variable objetivo: {target.name}")
        self._log_status("INFO", f"Variable fuente: {target.source_variable}")
        self._log_status("INFO", f"Regla: {target.rule}")
        self._log_status("INFO", f"Positivo: {target.positive_label} = estudiante en riesgo")
        self._log_status("INFO", f"Negativo: {target.negative_label} = estudiante sin riesgo")
        if target.observed_event:
            self._log_status("PASS", "Target corresponde a un evento observado")
        else:
            self._log_status("WARN", "El target es un proxy de riesgo, no deserción observada")

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

        self._log_status("INFO", f"Positivos: {positive} ({positive/n*100:.2f}%)")
        self._log_status("INFO", f"Negativos: {negative} ({negative/n*100:.2f}%)")
        
        if imbalance_ratio > 3:
            self._log_status("WARN", f"Ratio de desbalance: {imbalance_ratio:.2f} : 1")
        else:
            self._log_status("PASS", f"Ratio de desbalance: {imbalance_ratio:.2f} : 1")

    def log_binary_metrics(self, y_true, y_pred, y_proba):
        tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
        
        self._print("\nCONFUSION MATRIX")
        self._print("                 Predicho 0    Predicho 1")
        self._print(f"Real 0                {int(tn):<14} {int(fp)}")
        self._print(f"Real 1                {int(fn):<14} {int(tp)}")

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
        self._log_status("PASS" if acc >= 0.70 else ("WARN" if acc >= 0.60 else "FAIL"), f"Accuracy:              {acc:.4f}")
        self._log_status("PASS" if prec >= 0.70 else "WARN", f"Precision:             {prec:.4f}")
        self._log_status("PASS" if rec >= 0.70 else ("WARN" if rec >= 0.50 else "FAIL"), f"Recall:                {rec:.4f}")
        self._log_status("PASS" if spec >= 0.70 else "WARN", f"Specificity:           {spec:.4f}")
        self._log_status("PASS" if f1 >= 0.70 else ("WARN" if f1 >= 0.50 else "FAIL"), f"F1:                    {f1:.4f}")
        self._log_status("PASS" if bal_acc >= 0.70 else "WARN", f"Balanced Accuracy:     {bal_acc:.4f}")
        self._log_status("PASS" if roc >= 0.70 else ("WARN" if roc >= 0.60 else "FAIL"), f"ROC-AUC:               {roc:.4f}")
        self._log_status("INFO", f"PR-AUC:                {pr_auc:.4f}")
        self._log_status("INFO", f"MCC:                   {mcc:.4f}")
        self._log_status("PASS" if fnr < 0.30 else "FAIL", f"False Negative Rate:   {fnr:.4f}")
        self._log_status("PASS" if fpr < 0.30 else "WARN", f"False Positive Rate:   {fpr:.4f}")
        
        # Regla estricta
        if rec < 0.50:
            self.blockers.append("Recall menor a 0.50.")

    def log_baselines(self, X_train, X_test, y_train, y_test, model_roc: float):
        self._print("\nBASELINE COMPARISON")
        majority = DummyClassifier(strategy="most_frequent")
        majority.fit(X_train, y_train)
        maj_acc = accuracy_score(y_test, majority.predict(X_test))
        
        from sklearn.linear_model import LogisticRegression
        logistic = LogisticRegression(max_iter=2000, class_weight="balanced", random_state=42)
        try:
            logistic.fit(X_train, y_train)
            log_auc = roc_auc_score(y_test, logistic.predict_proba(X_test)[:, 1])
        except Exception:
            log_auc = 0.0
        
        self._log_status("INFO", f"Accuracy clase mayoritaria: {maj_acc:.4f}")
        self._log_status("INFO", f"AUC regresión logística: {log_auc:.4f}")
        self._log_status("INFO", f"AUC modelo evaluado: {model_roc:.4f}")
        
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
        self._log_status(status, f"Casos ruido: {n_noise}")
        self._log_status(status, f"Porcentaje ruido: {noise_pct*100:.2f}%")
        
        if noise_pct > 0.30:
            self.blockers.append("Más de 30% de ruido DBSCAN sin explicación.")

    def log_scientific_summary(self):
        self._print("\n" + "="*60)
        self._print("SCIENTIFIC EXECUTION SUMMARY")
        self._print("="*60)
        
        if len(self.blockers) > 0:
            self._print("OVERALL STATUS: PARTIAL / REQUIRES VALIDATION")
            self._print("BLOCKERS:")
            for b in set(self.blockers):
                self._print(f" - {b}")
        else:
            self._print("OVERALL STATUS: CONSOLIDATED")
        
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
        from sklearn.metrics import roc_curve
        thresholds = np.linspace(0.05, 0.95, 181)
        
        rows = []
        for th in thresholds:
            y_pred = (y_proba >= th).astype(int)
            rows.append({
                "threshold": float(th),
                "f1": f1_score(y_true, y_pred, zero_division=0),
                "recall": recall_score(y_true, y_pred, zero_division=0)
            })
            
        best_f1 = max(rows, key=lambda r: r["f1"])
        fpr, tpr, roc_thresholds = roc_curve(y_true, y_proba)
        youden = tpr - fpr
        best_youden_idx = int(np.argmax(youden))
        best_youden = roc_thresholds[best_youden_idx]
        
        self._log_status("INFO", f"Threshold por defecto: 0.50")
        self._log_status("INFO", f"Threshold mejor F1: {best_f1['threshold']:.4f}")
        self._log_status("INFO", f"Threshold mejor Youden J: {best_youden:.4f}")
        self._log_status("WARN", f"Threshold seleccionado: {selected_threshold:.4f}")

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

