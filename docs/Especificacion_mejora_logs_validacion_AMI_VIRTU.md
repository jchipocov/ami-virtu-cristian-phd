# Especificación de mejora de logs y validación científica
## Proyecto AMI-VIRTU / ARD-VIRTU

**Objetivo:** mejorar la trazabilidad, interpretación y robustez del pipeline, evitando que resultados exploratorios sean presentados como confirmaciones concluyentes.

**Fuentes revisadas**
- `real_bitacora_ejecuciones_20260629.log`
- `ConclusionesCorrida_20260629.md`

---

# 1. Problemas que debe corregir el pipeline

La ejecución actual contiene métricas útiles, pero no permite verificar con suficiente claridad:

1. Qué modelo se ejecutó realmente.
2. Cuántos registros entraron y salieron de cada etapa.
3. Qué variable exacta se predijo.
4. Cuánto mejora el modelo frente a un baseline.
5. Cuánta incertidumbre tienen Accuracy, AUC, F1 y Recall.
6. Si los clústeres son estables.
7. Si SHAP representa importancia, dirección o interacción.
8. Si una hipótesis está confirmada o solo tiene evidencia exploratoria.

---

# 2. Convención visual del log

Cada resultado debe llevar una etiqueta automática:

```text
[PASS] Resultado sólido.
[WARN] Resultado interpretable con cautela.
[FAIL] Resultado insuficiente para una conclusión fuerte.
[INFO] Información descriptiva.
[SKIP] Etapa no ejecutada.
[ERROR] Error técnico o científico.
```

Ejemplo:

```text
[PASS] KMO = 0.9259 | Adecuación muestral excelente
[WARN] ROC-AUC = 0.6375 | Discriminación modesta
[FAIL] ARI = 0.1584 | Bajo consenso entre algoritmos
```

---

# 3. Nuevos bloques que debe imprimir el log

## 3.1 Identificación inequívoca de la ejecución

```text
RUN IDENTIFICATION
[INFO] Run ID: 2026-06-29_15-04-02_rf
[INFO] Pipeline: main.py
[INFO] Modelo solicitado: rf
[INFO] Modelo instanciado: RandomForestClassifier
[INFO] Random state: 42
[INFO] Git commit: <hash>
[INFO] Git branch: <branch>
[INFO] Python: 3.11.3
[INFO] Scikit-learn: 1.8.0
```

### Código sugerido

```python
import os
import platform
import subprocess
import sklearn

def safe_git_value(*args: str) -> str:
    try:
        return subprocess.check_output(
            ["git", *args],
            stderr=subprocess.DEVNULL,
            text=True,
        ).strip()
    except Exception:
        return "NOT_AVAILABLE"

def execution_metadata(model) -> dict:
    return {
        "requested_model": os.getenv(
            "PREDICTIVE_RISK_MODEL_TYPE",
            "NOT_SET",
        ),
        "actual_model": model.__class__.__name__,
        "random_state": getattr(
            model,
            "random_state",
            "NOT_EXPOSED",
        ),
        "python": platform.python_version(),
        "sklearn": sklearn.__version__,
        "git_commit": safe_git_value("rev-parse", "HEAD"),
        "git_branch": safe_git_value(
            "rev-parse",
            "--abbrev-ref",
            "HEAD",
        ),
    }
```

## 3.2 Flujo de registros

```text
DATA FLOW
[INFO] Registros originales:          279
[INFO] Registros con target válido:   279
[WARN] Casos sospechosos:              19
[INFO] Casos excluidos:                19
[PASS] Muestra analítica final:       260
[INFO] Train:                         208
[INFO] Test:                           52
[PASS] Integridad de conteos: VERIFICADA
```

### Código sugerido

```python
def validate_data_flow(
    n_raw: int,
    n_target_valid: int,
    n_excluded: int,
    n_final: int,
    n_train: int,
    n_test: int,
) -> None:
    errors = []

    if n_target_valid > n_raw:
        errors.append(
            "n_target_valid no puede superar n_raw"
        )

    if n_final != n_target_valid - n_excluded:
        errors.append(
            "n_final debe ser n_target_valid - n_excluded"
        )

    if n_train + n_test != n_final:
        errors.append(
            "n_train + n_test debe ser igual a n_final"
        )

    if errors:
        raise ValueError(" | ".join(errors))
```

## 3.3 Definición exacta del target

```text
TARGET DEFINITION
[INFO] Variable objetivo: Riesgo_Binario
[INFO] Variable fuente: Score_Riesgo_Total
[INFO] Regla: Score_Riesgo_Total >= 3.0
[INFO] Positivo: 1 = estudiante en riesgo
[INFO] Negativo: 0 = estudiante sin riesgo
[WARN] El target es un proxy de riesgo, no deserción observada
```

### Código sugerido

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class TargetDefinition:
    name: str
    source_variable: str
    rule: str
    positive_label: int = 1
    negative_label: int = 0
    observed_event: bool = False

def target_status(target: TargetDefinition) -> str:
    if target.observed_event:
        return (
            "[PASS] Target corresponde a un evento observado"
        )

    return (
        "[WARN] Target basado en proxy; "
        "no debe denominarse deserción observada"
    )
```

## 3.4 Distribución de clases

```text
CLASS DISTRIBUTION
[INFO] Positivos: 95 (36.54%)
[INFO] Negativos: 165 (63.46%)
[WARN] Ratio de desbalance: 1.74 : 1
[INFO] Split estratificado: Sí
[INFO] Técnica de balanceo: Ninguna
```

### Código sugerido

```python
import numpy as np

def class_distribution(y) -> dict:
    labels, counts = np.unique(
        y,
        return_counts=True,
    )
    data = dict(
        zip(labels.tolist(), counts.tolist())
    )

    positive = data.get(1, 0)
    negative = data.get(0, 0)
    n = len(y)

    minority = min(positive, negative)
    majority = max(positive, negative)

    return {
        "positive": positive,
        "negative": negative,
        "positive_pct": positive / n,
        "negative_pct": negative / n,
        "imbalance_ratio": (
            majority / minority
            if minority
            else float("inf")
        ),
    }
```

## 3.5 Configuración del modelo

```text
MODEL CONFIGURATION
[INFO] Estimador: RandomForestClassifier
[INFO] Train/test: 80/20
[INFO] Split estratificado: Sí
[INFO] Threshold: 0.50
[INFO] n_estimators: 500
[INFO] class_weight: balanced
[INFO] max_depth: None
```

```python
def model_configuration(
    model,
    threshold: float,
) -> dict:
    return {
        "estimator": model.__class__.__name__,
        "threshold": threshold,
        "parameters": model.get_params(
            deep=False
        ),
    }
```

---

# 4. Métricas predictivas que deben agregarse

Debe registrarse:

- Accuracy
- Precision
- Recall o sensibilidad
- Specificity
- F1
- Balanced Accuracy
- ROC-AUC
- PR-AUC
- Matthews Correlation Coefficient
- Negative Predictive Value
- False Positive Rate
- False Negative Rate

```text
CONFUSION MATRIX
                 Predicho 0    Predicho 1
Real 0                30             3
Real 1                11             8

CLASSIFICATION METRICS
[PASS] Accuracy:              0.7308
[PASS] Precision:             0.7273
[FAIL] Recall:                0.4211
[PASS] Specificity:           0.9091
[WARN] F1:                    0.5333
[WARN] Balanced Accuracy:     0.6651
[WARN] ROC-AUC:               0.6375
[INFO] PR-AUC:                <valor>
[INFO] MCC:                   <valor>
[FAIL] False Negative Rate:   0.5789
[PASS] False Positive Rate:   0.0909
```

### Código sugerido

```python
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    confusion_matrix,
    f1_score,
    matthews_corrcoef,
    precision_score,
    recall_score,
    roc_auc_score,
)

def binary_metrics(
    y_true,
    y_pred,
    y_proba,
) -> dict:
    tn, fp, fn, tp = confusion_matrix(
        y_true,
        y_pred,
        labels=[0, 1],
    ).ravel()

    specificity = (
        tn / (tn + fp)
        if (tn + fp)
        else 0.0
    )
    npv = (
        tn / (tn + fn)
        if (tn + fn)
        else 0.0
    )
    fpr = (
        fp / (fp + tn)
        if (fp + tn)
        else 0.0
    )
    fnr = (
        fn / (fn + tp)
        if (fn + tp)
        else 0.0
    )

    return {
        "tn": int(tn),
        "fp": int(fp),
        "fn": int(fn),
        "tp": int(tp),
        "accuracy": accuracy_score(
            y_true,
            y_pred,
        ),
        "precision": precision_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "recall": recall_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "specificity": specificity,
        "npv": npv,
        "f1": f1_score(
            y_true,
            y_pred,
            zero_division=0,
        ),
        "balanced_accuracy": (
            balanced_accuracy_score(
                y_true,
                y_pred,
            )
        ),
        "roc_auc": roc_auc_score(
            y_true,
            y_proba,
        ),
        "pr_auc": average_precision_score(
            y_true,
            y_proba,
        ),
        "mcc": matthews_corrcoef(
            y_true,
            y_pred,
        ),
        "false_positive_rate": fpr,
        "false_negative_rate": fnr,
    }
```

---

# 5. Comparación obligatoria contra baselines

```text
BASELINE COMPARISON
[INFO] Accuracy clase mayoritaria: 0.6346
[INFO] Accuracy dummy estratificado: <valor>
[INFO] AUC regresión logística: <valor>
[INFO] AUC modelo no lineal: 0.6375
[PASS] Mejora absoluta vs mayoría: +0.0962
```

### Código sugerido

```python
from sklearn.dummy import DummyClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    roc_auc_score,
)

def evaluate_baselines(
    X_train,
    X_test,
    y_train,
    y_test,
) -> dict:
    majority = DummyClassifier(
        strategy="most_frequent"
    )
    majority.fit(X_train, y_train)

    stratified = DummyClassifier(
        strategy="stratified",
        random_state=42,
    )
    stratified.fit(X_train, y_train)

    logistic = LogisticRegression(
        max_iter=2000,
        class_weight="balanced",
        random_state=42,
    )
    logistic.fit(X_train, y_train)

    return {
        "majority_accuracy": accuracy_score(
            y_test,
            majority.predict(X_test),
        ),
        "stratified_accuracy": accuracy_score(
            y_test,
            stratified.predict(X_test),
        ),
        "logistic_auc": roc_auc_score(
            y_test,
            logistic.predict_proba(
                X_test
            )[:, 1],
        ),
    }
```

---

# 6. Intervalos de confianza

```text
UNCERTAINTY
[INFO] Método: bootstrap, 2000 iteraciones
[WARN] Accuracy 95% CI: [<low>, <high>]
[WARN] ROC-AUC 95% CI:  [<low>, <high>]
[WARN] Recall 95% CI:   [<low>, <high>]
```

### Código sugerido

```python
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    recall_score,
    roc_auc_score,
)

def bootstrap_metric_ci(
    y_true,
    y_pred,
    y_proba,
    metric_name: str,
    n_bootstrap: int = 2000,
    random_state: int = 42,
) -> tuple[float, float]:
    rng = np.random.default_rng(
        random_state
    )

    y_true = np.asarray(y_true)
    y_pred = np.asarray(y_pred)
    y_proba = np.asarray(y_proba)

    values = []
    n = len(y_true)

    for _ in range(n_bootstrap):
        idx = rng.integers(
            0,
            n,
            size=n,
        )

        y_b = y_true[idx]
        pred_b = y_pred[idx]
        proba_b = y_proba[idx]

        if len(np.unique(y_b)) < 2:
            continue

        if metric_name == "accuracy":
            value = accuracy_score(
                y_b,
                pred_b,
            )
        elif metric_name == "recall":
            value = recall_score(
                y_b,
                pred_b,
                zero_division=0,
            )
        elif metric_name == "roc_auc":
            value = roc_auc_score(
                y_b,
                proba_b,
            )
        else:
            raise ValueError(
                f"Métrica no soportada: {metric_name}"
            )

        values.append(value)

    if not values:
        raise RuntimeError(
            "No fue posible calcular el intervalo"
        )

    low, high = np.percentile(
        values,
        [2.5, 97.5],
    )

    return float(low), float(high)
```

---

# 7. Validación cruzada repetida

Una única partición train/test no debe usarse como evidencia definitiva.

```text
CROSS-VALIDATION
[INFO] Método: RepeatedStratifiedKFold
[INFO] Splits: 5
[INFO] Repeticiones: 10
[INFO] Evaluaciones: 50
[WARN] ROC-AUC media: <valor>
[INFO] ROC-AUC std: <valor>
[WARN] Recall medio: <valor>
[WARN] F1 medio: <valor>
```

### Código sugerido

```python
import numpy as np
from sklearn.model_selection import (
    RepeatedStratifiedKFold,
    cross_validate,
)

def repeated_cv_summary(
    model,
    X,
    y,
) -> dict:
    cv = RepeatedStratifiedKFold(
        n_splits=5,
        n_repeats=10,
        random_state=42,
    )

    scoring = {
        "accuracy": "accuracy",
        "balanced_accuracy": (
            "balanced_accuracy"
        ),
        "roc_auc": "roc_auc",
        "f1": "f1",
        "recall": "recall",
        "precision": "precision",
    }

    result = cross_validate(
        model,
        X,
        y,
        cv=cv,
        scoring=scoring,
        n_jobs=-1,
        error_score="raise",
    )

    summary = {}

    for metric in scoring:
        values = result[f"test_{metric}"]
        summary[metric] = {
            "mean": float(
                np.mean(values)
            ),
            "std": float(
                np.std(values, ddof=1)
            ),
            "min": float(
                np.min(values)
            ),
            "max": float(
                np.max(values)
            ),
        }

    return summary
```

---

# 8. Análisis de threshold

Debe registrarse el umbral de decisión utilizado.

```text
THRESHOLD ANALYSIS
[INFO] Threshold por defecto: 0.50
[INFO] Threshold mejor F1: <valor>
[INFO] Threshold mejor Youden J: <valor>
[INFO] Threshold para Recall >= 0.70: <valor>
[WARN] Threshold seleccionado: <valor>
[INFO] Criterio: <criterio>
```

### Código sugerido

```python
import numpy as np
from sklearn.metrics import (
    f1_score,
    recall_score,
    roc_curve,
)

def threshold_analysis(
    y_true,
    y_proba,
) -> dict:
    thresholds = np.linspace(
        0.05,
        0.95,
        181,
    )

    rows = []

    for threshold in thresholds:
        y_pred = (
            y_proba >= threshold
        ).astype(int)

        rows.append({
            "threshold": float(threshold),
            "f1": f1_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
            "recall": recall_score(
                y_true,
                y_pred,
                zero_division=0,
            ),
        })

    best_f1 = max(
        rows,
        key=lambda row: row["f1"],
    )

    fpr, tpr, roc_thresholds = roc_curve(
        y_true,
        y_proba,
    )
    youden = tpr - fpr
    best_youden_idx = int(
        np.argmax(youden)
    )

    return {
        "best_f1": best_f1,
        "best_youden_threshold": float(
            roc_thresholds[
                best_youden_idx
            ]
        ),
    }
```

> El threshold debe seleccionarse dentro de validación cruzada o con un conjunto de validación. No debe optimizarse directamente sobre el test final.

---

# 9. Ajustes de psicometría

## 9.1 No llamar CFA a split-half EFA

```text
FACTORIAL VALIDATION
[INFO] Procedimiento: Split-half EFA
[INFO] Métrica: Tucker's Phi
[PASS] Factor crítico: 0.9717
[PASS] Factor técnico: 0.9280
[WARN] Factor participativo: 0.8458
[WARN] Promedio global: 0.9152
[INFO] CFA convencional ejecutada: NO
```

## 9.2 Clasificación automática de Tucker Phi

```python
def classify_tucker_phi(
    value: float,
) -> tuple[str, str]:
    if value >= 0.95:
        return (
            "PASS",
            "Congruencia excelente",
        )

    if value >= 0.90:
        return (
            "PASS",
            "Congruencia adecuada",
        )

    if value >= 0.85:
        return (
            "WARN",
            "Congruencia marginal",
        )

    return (
        "FAIL",
        "Congruencia insuficiente",
    )
```

## 9.3 Estado factorial global

```python
def factorial_global_status(
    phi_by_factor: dict[str, float],
) -> tuple[str, str]:
    statuses = [
        classify_tucker_phi(value)[0]
        for value in phi_by_factor.values()
    ]

    if "FAIL" in statuses:
        return (
            "FAIL",
            "Existe al menos un factor insuficiente",
        )

    if "WARN" in statuses:
        return (
            "WARN",
            "Existe al menos un factor marginal",
        )

    return (
        "PASS",
        "Todos los factores son adecuados",
    )
```

---

# 10. Ajustes de correlaciones

## 10.1 Corrección por pruebas múltiples

```python
from statsmodels.stats.multitest import (
    multipletests,
)

def adjust_pvalues_bh(
    pvalues: list[float],
) -> list[float]:
    _, adjusted, _, _ = multipletests(
        pvalues,
        alpha=0.05,
        method="fdr_bh",
    )

    return adjusted.tolist()
```

El log debe imprimir:

```text
Score_AMI_Global vs Score_Riesgo_LMS
[INFO] Pearson r: -0.280
[INFO] p bruto: 0.0000
[PASS] p ajustado BH: <valor>
[WARN] Tamaño de efecto: pequeño
```

## 10.2 Tamaño de efecto

```python
def correlation_effect(
    r: float,
) -> str:
    value = abs(r)

    if value < 0.10:
        return "Trivial"

    if value < 0.30:
        return "Pequeño"

    if value < 0.50:
        return "Moderado"

    return "Grande"
```

## 10.3 No inferir no linealidad automáticamente

Debe imprimirse:

```text
[INFO] Prueba explícita de no linealidad: NO
[WARN] Una correlación baja no demuestra no linealidad
```

---

# 11. Ajustes de SHAP

## 11.1 Terminología correcta

Reemplazar:

```text
Impacto Gini
```

por:

```text
Importancia global SHAP
```

o:

```text
mean(|SHAP|)
```

## 11.2 Log recomendado

```text
SHAP GLOBAL
[INFO] Participativo: mean(|SHAP|)=0.3546
[INFO] Técnico: mean(|SHAP|)=0.3478
[INFO] Crítico: mean(|SHAP|)=0.2975
[WARN] Dirección no inferible desde mean(|SHAP|)
[WARN] Interacciones SHAP no calculadas
```

## 11.3 Artefactos que deben generarse

```text
XAI ARTIFACTS
[PASS] shap_summary_bar.png
[PASS] shap_summary_beeswarm.png
[PASS] shap_dependence_C10.png
[PASS] shap_dependence_P10.png
[PASS] shap_dependence_P3.png
[SKIP] shap_interaction_summary.png
```

---

# 12. Ajustes de clustering

## 12.1 DBSCAN

```text
DBSCAN VALIDATION
[INFO] Casos analizados: 260
[INFO] Casos asignados: 126
[FAIL] Casos ruido: 134
[FAIL] Porcentaje ruido: 51.54%
```

```python
import numpy as np

def dbscan_summary(labels) -> dict:
    labels = np.asarray(labels)

    n_total = len(labels)
    n_noise = int(
        np.sum(labels == -1)
    )
    n_assigned = n_total - n_noise

    return {
        "n_total": n_total,
        "n_assigned": n_assigned,
        "n_noise": n_noise,
        "noise_pct": (
            n_noise / n_total
            if n_total
            else 0.0
        ),
    }
```

## 12.2 Silhouette

```python
def classify_silhouette(
    value: float,
) -> tuple[str, str]:
    if value >= 0.50:
        return (
            "PASS",
            "Separación razonable",
        )

    if value >= 0.25:
        return (
            "WARN",
            "Separación débil o moderada",
        )

    return (
        "FAIL",
        "Estructura insuficiente",
    )
```

## 12.3 ARI

```python
def classify_ari(
    value: float,
) -> tuple[str, str]:
    if value >= 0.75:
        return (
            "PASS",
            "Consenso fuerte",
        )

    if value >= 0.50:
        return (
            "WARN",
            "Consenso moderado",
        )

    if value >= 0.25:
        return (
            "WARN",
            "Consenso débil",
        )

    return (
        "FAIL",
        "Consenso muy bajo",
    )
```

## 12.4 BIC comparativo

No imprimir un único BIC aislado.

```text
GMM MODEL SELECTION
K=2 | BIC=<valor>
K=3 | BIC=1954.4437
K=4 | BIC=<valor>
K=5 | BIC=<valor>
[PASS] K seleccionado: 3
```

```python
from sklearn.mixture import (
    GaussianMixture,
)

def select_gmm_by_bic(
    X,
    k_values=range(2, 7),
    random_state: int = 42,
) -> dict:
    results = []

    for k in k_values:
        model = GaussianMixture(
            n_components=k,
            covariance_type="full",
            random_state=random_state,
        )
        model.fit(X)

        results.append({
            "k": k,
            "bic": float(
                model.bic(X)
            ),
            "aic": float(
                model.aic(X)
            ),
            "model": model,
        })

    best = min(
        results,
        key=lambda row: row["bic"],
    )

    return {
        "results": results,
        "best_k": best["k"],
        "best_model": best["model"],
    }
```

---

# 13. Validación por universidad

El efecto de universidad debe obligar a evaluar generalización institucional.

```text
UNIVERSITY GENERALIZATION
Universidad A | AUC=<valor> | Recall=<valor>
Universidad B | AUC=<valor> | Recall=<valor>
Universidad C | AUC=<valor> | Recall=<valor>
[WARN] Variabilidad institucional: <nivel>
```

### Código sugerido

```python
import numpy as np
from sklearn.base import clone
from sklearn.metrics import (
    roc_auc_score,
)

def leave_one_group_out_auc(
    model,
    X,
    y,
    groups,
) -> list[dict]:
    groups = np.asarray(groups)
    y = np.asarray(y)

    results = []

    for group in np.unique(groups):
        train_mask = groups != group
        test_mask = groups == group
        y_test = y[test_mask]

        if len(np.unique(y_test)) < 2:
            results.append({
                "group": str(group),
                "auc": None,
                "status": "SKIP",
            })
            continue

        estimator = clone(model)
        estimator.fit(
            X[train_mask],
            y[train_mask],
        )

        y_proba = estimator.predict_proba(
            X[test_mask]
        )[:, 1]

        results.append({
            "group": str(group),
            "auc": float(
                roc_auc_score(
                    y_test,
                    y_proba,
                )
            ),
            "status": "OK",
        })

    return results
```

---

# 14. Umbrales configurables

```python
VALIDATION_THRESHOLDS = {
    "kmo": {
        "pass": 0.90,
        "warn": 0.70,
    },
    "cronbach_alpha": {
        "pass": 0.80,
        "warn": 0.70,
    },
    "tucker_phi": {
        "pass": 0.90,
        "warn": 0.85,
    },
    "roc_auc": {
        "pass": 0.70,
        "warn": 0.60,
    },
    "f1": {
        "pass": 0.70,
        "warn": 0.50,
    },
    "recall": {
        "pass": 0.70,
        "warn": 0.50,
    },
    "silhouette": {
        "pass": 0.50,
        "warn": 0.25,
    },
    "ari": {
        "pass": 0.75,
        "warn": 0.25,
    },
}
```

```python
def classify_high_is_good(
    value: float,
    pass_threshold: float,
    warn_threshold: float,
) -> str:
    if value >= pass_threshold:
        return "PASS"

    if value >= warn_threshold:
        return "WARN"

    return "FAIL"
```

---

# 15. Resumen científico automático

```text
============================================================
SCIENTIFIC EXECUTION SUMMARY
============================================================
[PASS] Reproducibilidad: VERIFICADA

[PASS] Consistencia interna: ALTA

[WARN] Estructura factorial: PARCIALMENTE ESTABLE
       Factor participativo con Tucker Phi marginal.

[WARN] Capacidad predictiva: MODESTA
       AUC=0.6375
       F1=0.5333
       Recall=0.4211

[FAIL] Detección de riesgo: INSUFICIENTE
       Se omite 57.89% de los positivos.

[FAIL] Estabilidad de clustering: BAJA
       ARI=0.1584
       Silhouette=0.3872

[WARN] XAI: IMPORTANCIA CALCULADA
       Dirección e interacción no validadas.

OVERALL STATUS: PARTIAL / REQUIRES VALIDATION
============================================================
```

---

# 16. Evaluación automática de hipótesis

## H1 — capacidad predictiva

```python
def evaluate_h1(
    auc: float,
    auc_ci_low: float | None,
    recall: float,
    cv_auc_mean: float | None,
) -> tuple[str, str]:
    if (
        auc_ci_low is None
        or cv_auc_mean is None
    ):
        return (
            "WARN",
            "Evidencia predictiva preliminar; "
            "faltan intervalos o validación cruzada",
        )

    if (
        auc_ci_low > 0.50
        and cv_auc_mean >= 0.70
        and recall >= 0.60
    ):
        return (
            "PASS",
            "Evidencia predictiva consistente",
        )

    if auc >= 0.60:
        return (
            "WARN",
            "Señal predictiva modesta; "
            "requiere validación adicional",
        )

    return (
        "FAIL",
        "Capacidad discriminante insuficiente",
    )
```

## H2 — estructura factorial

```python
def evaluate_h2(
    phi_by_factor: dict[str, float],
    cfa_executed: bool,
) -> tuple[str, str]:
    minimum_phi = min(
        phi_by_factor.values()
    )

    if (
        cfa_executed
        and minimum_phi >= 0.90
    ):
        return (
            "PASS",
            "Estructura consistentemente apoyada",
        )

    if minimum_phi >= 0.85:
        return (
            "WARN",
            "Apoyo parcial-favorable",
        )

    return (
        "FAIL",
        "Estructura factorial inestable",
    )
```

## H4 — perfiles

```python
def evaluate_h4(
    ari: float,
    silhouette: float,
    bootstrap_ari: float | None,
) -> tuple[str, str]:
    if (
        ari >= 0.50
        and silhouette >= 0.50
        and bootstrap_ari is not None
        and bootstrap_ari >= 0.50
    ):
        return (
            "PASS",
            "Perfiles diferenciados y estables",
        )

    if silhouette >= 0.25:
        return (
            "WARN",
            "Evidencia exploratoria; "
            "estabilidad insuficiente",
        )

    return (
        "FAIL",
        "No hay estructura confiable",
    )
```

---

# 17. Orden recomendado del log

```text
01. Identificación de ejecución
02. Reproducibilidad
03. Flujo de registros
04. Definición del target
05. Calidad y exclusiones
06. Psicometría
07. EFA y congruencia factorial
08. Asociaciones bivariadas
09. Ajuste por pruebas múltiples
10. Configuración del modelo
11. Distribución de clases
12. Baselines
13. Matriz de confusión
14. Métricas predictivas
15. Intervalos de confianza
16. Validación cruzada
17. Threshold
18. Validación por universidad
19. SHAP
20. Clustering
21. Estabilidad de clústeres
22. Evidencia cualitativa
23. Evaluación de hipótesis
24. Resumen científico
25. Artefactos generados
26. Errores y etapas omitidas
```

---

# 18. Prioridades de implementación

## Prioridad 1 — obligatoria

1. Identidad real del estimador.
2. Flujo completo de registros.
3. Definición exacta del target.
4. Matriz de confusión.
5. Recall, specificity y balanced accuracy.
6. Baseline mayoritario.
7. Estados `PASS/WARN/FAIL`.
8. Terminología SHAP correcta.
9. Conteo de ruido de DBSCAN.
10. Resumen científico automático prudente.

## Prioridad 2 — alta

1. Validación cruzada repetida.
2. Intervalos de confianza.
3. PR-AUC y MCC.
4. Comparación con regresión logística.
5. Corrección por pruebas múltiples.
6. Comparación de BIC para varios K.
7. Validación leave-one-university-out.

## Prioridad 3 — avanzada

1. Bootstrap de estabilidad de clústeres.
2. SHAP dependence.
3. SHAP interaction.
4. Calibración de probabilidades.
5. Brier Score.
6. Decision Curve Analysis.
7. CFA convencional.
8. Invarianza factorial por universidad.
9. Validación externa con la muestra ampliada.

---

# 19. Criterios que impiden declarar una corrida consolidada

La ejecución debe quedar como `PARTIAL / REQUIRES VALIDATION` cuando ocurra cualquiera de estas condiciones:

```text
- AUC sin intervalo de confianza.
- Ausencia de validación cruzada.
- Recall menor a 0.50.
- Target proxy presentado como deserción observada.
- mean(|SHAP|) interpretado como dirección causal.
- ARI menor a 0.25.
- Más de 30% de ruido DBSCAN sin explicación.
- Tucker Phi menor a 0.85 en algún factor.
- Diferencias no explicadas entre N original y N final.
- Modelo solicitado distinto del modelo instanciado.
```

---

# 20. Resultado esperado

Con estos cambios, la bitácora permitirá verificar:

- qué datos fueron utilizados;
- qué casos fueron excluidos;
- qué modelo se ejecutó;
- qué variable se predijo;
- cuánto mejora frente a un baseline;
- cuántos positivos detecta y omite;
- qué resultados son inferenciales;
- qué resultados son predictivos;
- qué factores son estables;
- qué clústeres son reproducibles;
- qué afirma SHAP y qué no;
- qué hipótesis tienen apoyo fuerte, parcial o insuficiente.

La salida final debe favorecer una interpretación científica reproducible y prudente, no una narrativa automática orientada a confirmar hipótesis.
