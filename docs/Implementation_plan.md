# Plan Maestro de Implementación: AMI-VIRTU & ARD-VIRTU (Detallado)

Este documento centraliza el roadmap técnico y metodológico del proyecto, integrando la arquitectura estadística actual con la nueva fase cualitativa automatizada.

---

## Estructura del Proyecto y Flujo de Datos

```text
learning_analytics_ami/
├── main.py                 # Orquestador: Fases 1 a 9 del pipeline completo.
├── .env                    # Configuración de API Keys, APP_ENV y COHERENCE_THRESHOLD.
├── data/                   
│   ├── raw/                # Ingesta de real_data.csv o data sintética.
│   ├── processed/          # Datasets limpios e invertidos.
│   └── outputs/            # Gráficos (PNG), Tablas (CSV/XLSX) y Reportes (MD).
├── docs/                   # Vademécum, Resumen Ejecutivo y Guías Metodológicas.
├── logs/                   # Bitácoras de auditoría en Markdown y JSONL.
├── src/
│   ├── simulation/         # data_simulator.py (Cópulas Gaussianas y Factores Latentes).
│   ├── processing/         # cleaner.py (Filtro PII, Detectores de Inconsistencia), scorer.py.
│   ├── analysis/           # stats_analyzer.py (ML/Logit), clustering_engine.py (Ensamble).
│   └── utils/              # logger.py, reporter.py (Dashboards Paper-Ready).
└── tests/                  # Suite de validación psicométrica (Pytest).
```

---

## Detalle de Fases Implementadas

### Fase 1: Generación Estocástica Multivariada (COMPLETADO)
- **Motor:** `DataSimulator` basado en **Cópulas Gaussianas**.
- **Lógica Psicométrica:** Simulación de variables latentes ($F_{cri}, F_{tec}, F_{par}$) con matrices de covarianza controladas.
- **Interacción Semántica:** Implementación de la AMI como **Amplificador/Radar** ($AMI \times Calidad$).
- **Ítems Inversos:** Generación controlada de ítems negativos (`C6`, `T6`, `P5`) para validar el motor de inversión.

### Fase 2: Auditoría de Calidad y Limpieza (COMPLETADO)
- **Filtro PII (Privacy by Design):** Eliminación automática de DNI, Nombres y correos.
- **Detectores de Anomalía:**
    - **Flatliners:** Detección de varianza cero (aquiescencia).
    - **Contradicción Semántica:** Validación de coherencia entre A4 (Rendimiento) y A2 (Desaprobados).
- **Inversión de Escalas:** Normalización de ítems inversos (`6 - valor`) para permitir el cálculo de fiabilidad.

### Fase 3-4: Psicometría y Análisis de Significancia (COMPLETADO)
- **Consistencia Interna:** Cálculo de **Alfa de Cronbach** y **Omega de McDonald** (más robusto para modelos no-congenéricos).
- **Inferencia Univariada:** T-test de muestras independientes (Sexo) y ANOVA de una vía (Universidad).
- **Asociaciones:** Correlación de Punto-Biserial y Spearman para relaciones no-lineales AMI-Riesgo.

### Fase 5: Inferencia Avanzada y Machine Learning (COMPLETADO)
- **Regresión Logística (statsmodels):** 
    - Cálculo de **Odds Ratios ($Exp(\beta)$)** con Intervalos de Confianza al 95%.
    - Reporte de significancia estadística ($p < 0.05$).
- **Optimización Preventiva:** Ajuste de umbrales mediante el **Índice de Youden** para maximizar el Recall (detección de riesgo).
- **Modelos de Ensamble:** Implementación de **Gradient Boosting** (sucesor de Random Forest) optimizado por GridSearch.
- **Hipótesis del Moderador:** Validación del término de interacción para confirmar si la calidad educativa modera el impacto de la AMI.

### Fase 6: Perfilamiento Sociológico (Ensemble Clustering) (COMPLETADO)
- **Triangulación Algorítmica:** Integración de **K-Means**, **Ward**, **DBSCAN** y **GMM**.
- **Validación de Estructura:** Análisis de inercia (Codo) y coeficiente de **Silueta**.
- **Caracterización:** Generación de **Radar Charts** y perfiles de riesgo por segmento.

### Fase 7-8: XAI y Auditoría de Bitácora (COMPLETADO)
- **Explainable AI (SHAP):** 
    - **Global:** Impacto de las dimensiones en la probabilidad de deserción.
    - **Granular (Microscopía):** SHAP sobre los 30 ítems individuales para identificar las preguntas con mayor poder predictivo.
- **Registro Clínico:** Bitácora automatizada que documenta cada decisión del pipeline para replicabilidad académica.

---

## [NUEVO] Fase 9: Análisis Cualitativo Híbrido (Gemini API)

Esta fase transforma el proyecto en un modelo de **Métodos Mixtos** de vanguardia.

### 9.1 Generación Cualitativa (Decoupled Generator)
- **Módulo:** `src/simulation/qualitative_generator.py`
- **Función:** Consume scores numéricos y genera respuestas de texto para la Sección B (BC1-BP4) vía Gemini.
- **Semilla de Error:** Parámetro `p_incoherence` de entorno para inyectar un % de respuestas "mentirosas" para probar el validador.

### 9.2 Motor de Coherencia Híbrida
- **Módulo:** `src/analysis/qualitative_engine.py`
- **Métricas:** 
    - `Sentimiento_Academico` (0-1): Tono emocional de la declaración.
    - `Etiquetas_Tematicas`: Codificación automática por tópicos (ej. "Brecha tecnológica").
    - `Indice_Coherencia` (0-1): Cross-validation entre lo que el alumno marcó y lo que escribió.
- **Hardening:** Filtrado automático mediante `COHERENCE_THRESHOLD` (Variable `.env`).

### 9.3 Síntesis Narrativa Executive
- Integración en `Reporter` para redactar una "Conclusión Agéntica" que explique descriptivamente los perfiles de riesgo encontrados.

---

## [POR HACER] Fase 10: Convergencia de Dataset y Limpieza Inteligente
Esta fase asegura que el motor estadístico use la nueva data cualitativa como un filtro de rigor.

- **Check-pointing:** Implementar guardado incremental en el loop de `main.py` para evitar pérdidas por límites de API.
- **Filtro de Coherencia Agresivo:** Exclusión automática de registros con `Indice_Coherencia < 0.6` de los modelos de regresión y clustering.
- **Normalización Híbrida:** Conversión de etiquetas de sentimiento en variables numéricas continuas para su uso como covariables.

## [POR HACER] Fase 11: Triangulación de Métodos Mixtos
Cruce científico entre lo que el sistema "calcula" y lo que la IA "comprende".

- **Asociaciones de Dimensión:** Correlacionar `Score_AMI_Global` vs `Sentimiento_Academico`.
- **Análisis de Discrepancia:** Identificar grupos donde hay alto puntaje AMI pero sentimiento negativo (Potenciales "Bulos" o alumnos en crisis encubierta).
- **Semántica de clústeres:** Asignar una "Etiqueta Cualitativa" a cada clúster de K-Means basada en el análisis semántico predominante.

## [POR HACER] Fase 12: Visualización y Reporte Doctoral (Final)
Producción de los artefactos finales para la defensa de tesis.

- **Dashboards Híbridos:** Gráficos que incluyan "Word Clouds" temáticos y Radar Charts numéricos en una sola vista.
- **Citas Textuales Automatizadas:** Selección automática de las declaraciones más representativas de cada clúster para ilustrar el reporte narrativo.
- **Exportación de Paper-Ready Dashboard:** Generación de un PDF/Markdown final que combine el rigor de `statsmodels` con la riqueza de la narrativa cualitativa.
