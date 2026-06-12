# Auditoría Doctoral Integral: Proyecto AMI-VIRTU & ARD-VIRTU

**Auditor:** Revisión Metodológica Experta (Nivel Doctoral)  
**Fecha de Auditoría:** 09 de Junio de 2026  
**Corpus revisado:** README.md, todos los docs/, reports generados, main.py, requirements.txt  
**Estándar de referencia:** APA 7ª edición · Normas de rigor doctoral en ciencias sociales computacionales

---

## 🔬 Veredicto General

> [!IMPORTANT]
> El proyecto AMI-VIRTU posee una **arquitectura analítica sólida y bien concebida**. El pipeline estadístico (psicometría → inferencia → XAI → clustering → triangulación mixta) está correctamente secuenciado y responde a las exigencias de una tesis doctoral en ciencias sociales computacionales. Sin embargo, se han identificado **11 áreas de mejora** —algunas menores y otras críticas— que deben atenderse antes de la defensa.

---

## ✅ Fortalezas Confirmadas

| Área | Evaluación |
| :--- | :--- |
| Secuencia metodológica global | **Excelente** — Psicometría → Inferencia → XAI → Clustering → Triangulación |
| Uso de Omega de McDonald junto a Cronbach | **Correcto y actual** (McNeish, 2018) |
| Inclusión de KMO, Bartlett, VIF y Hosmer-Lemeshow | **Impecable** — Blindaje estadístico completo |
| Ensamble de 4 algoritmos de clustering + ARI | **Innovador** — Supera la práctica estándar |
| Inclusión de SHAP como capa XAI post-hoc | **Pertinente y bien fundamentado** |
| Hash SHA-256 para auditoría forense | **Buena práctica científica** reproducible |
| Triangulación mixta cuanti-cuali | **Contribución doctoral genuina** |
| Detección del "Riesgo Invisible" (4.7%) | **Hallazgo original y de alto valor** |
| Detector de inconsistencias / flatliners | **Ético y metodológicamente riguroso** |
| Inversión de ítems (C6, T6, P5) documentada | **Correcto** |

---

## 🚨 HALLAZGOS CRÍTICOS (Prioridad Alta)

### HC-01 · Inconsistencia entre N=295 y N=263 en documentación

**Archivos afectados:** `DataStatistics.md` (pie de página), `Informe_Metodologico_Doctoral.md`

El pie de página de `DataStatistics.md` reporta:
> *"Fecha: 28 de Abril de 2026 | Dataset N=263 (Filtrado por Coherencia)"*

...mientras que **todos los reportes de análisis y el README** usan consistentemente N=295. Esta discrepancia es crítica porque un jurado de tesis examinará esta contradicción inmediatamente.

**Acción requerida:**
- Definir y documentar **un único N oficial** con su flujo de exclusiones: N_original → N_filtrado (por coherencia) → N_final para análisis.
- Ejemplo correcto: *"N=295 casos recolectados; N=263 casos válidos tras aplicar el Filtro de Coherencia (IC ≥ 0.6); N=295 reportado en análisis psicométricos, N=263 en modelos inferenciales."*
- Si los reportes de análisis (regresión, clustering) usan 295 o 263, debe ser declarado explícitamente y con coherencia.

---

### HC-02 · Ausencia de Validez de Constructo Confirmatoria (AFC/CFA)

**Archivos afectados:** `Informe_Metodologico_Doctoral.md`, `DataStatistics.md`, `VADEMECUM_ESTADISTICO.md`

El proyecto documenta y ejecuta un **Análisis Factorial Exploratorio (EFA)** pero **no menciona ni implementa un Análisis Factorial Confirmatorio (AFC/CFA)**. Para una tesis doctoral que defiende la estructura trimodal de la AMI (Crítica, Técnica, Participativa), el estándar metodológico exige:

1. **EFA** sobre una submuestra (p.ej., n≈150) para explorar la estructura factorial.
2. **CFA** sobre la muestra restante para *confirmar* dicha estructura.

Sin CFA, el argumento de "estructura validada" es incompleto ante un jurado especializado. La librería `factor_analyzer` (ya presente en requirements.txt) no implementa CFA; se requiere `semopy` o similar.

**Acción requerida:** Documentar si este paso será añadido al pipeline o justificar explícitamente (con referencia) por qué el EFA es suficiente para el alcance del estudio (e.g., muestra < 300, carácter exploratorio-confirmatorio mixto).

---

### HC-03 · Falta de reporte de tamaño de efecto en contrastes sociodemográficos

**Archivos afectados:** `DataStatistics.md` (Fase 2), `Informe_Metodologico_Doctoral.md` (Sección 4)

Los contrastes de género (T-test) y universidad (ANOVA) reportan estadísticos y p-valores, pero **no incluyen tamaños de efecto**. Las directrices APA 7 y la práctica doctoral moderna exigen:

| Prueba | Tamaño de efecto requerido |
| :--- | :--- |
| T-test independiente | **d de Cohen** |
| ANOVA de una vía | **η² (eta cuadrado) o ω²** |
| Correlaciones | **r de Pearson** (ya presente) |

Un p-valor significativo con un tamaño de efecto pequeño (d < 0.20) no tiene relevancia práctica. Reportar ambos es la norma doctoral actual.

---

### HC-04 · El Pseudo R² de McFadden reportado es inconsistente entre documentos

**Archivos afectados:** `RESUMEN_EJECUTIVO.md` (Sección 5), `03_modelo_inferencial.md`

- `RESUMEN_EJECUTIVO.md` reporta: **McFadden R² = 0.42**
- `03_modelo_inferencial.md` reporta: **McFadden R² = 0.2442**

Ambos valores no pueden ser correctos simultáneamente para el mismo modelo. Un valor de 0.42 en ciencias sociales es extraordinariamente alto (casi perfecto) y generaría sospecha de sobreajuste. El valor de 0.24 es más creíble y se alinea con la interpretación del propio documento ("superior a 0.20 indica ajuste robusto").

**Acción requerida:** Verificar en el código fuente (`stats_analyzer.py`) cuál es el valor calculado y unificar en todos los documentos.

---

### HC-05 · Ausencia de validación cruzada (Cross-Validation) para el modelo logístico

**Archivos afectados:** `DataStatistics.md`, `Implementation_plan.md`, `Informe_Metodologico_Doctoral.md`

El modelo de regresión logística se evalúa con un único split train/test. Con N=295 (o N=263 filtrado), este tamaño muestral es insuficiente para garantizar la estabilidad de los coeficientes con un simple holdout. La práctica estándar doctoral exige:

- **k-Fold Cross-Validation (k=5 o k=10)** para estimar el error de generalización.
- O al mínimo, **Leave-One-Out (LOO)** para muestras pequeñas.

Sin esto, el ROC-AUC reportado (0.88) puede ser optimistamente inflado (data leakage parcial o varianza de partición).

---

## ⚠️ HALLAZGOS IMPORTANTES (Prioridad Media)

### HI-01 · La bibliografía es insuficiente para defensa doctoral

**Archivo afectado:** `Bibliografia.md`

El documento lista **12 referencias**. Para una tesis doctoral en este dominio (learning analytics + estadística + XAI + métodos mixtos), el estándar mínimo académico es **40-80 referencias** con distribución equilibrada entre:

- Marco teórico AMI y deserción (≥ 10 refs).
- Metodología estadística y psicométrica (≥ 10 refs).
- Learning analytics y sistemas de alerta temprana (≥ 10 refs).
- XAI y machine learning educativo (≥ 8 refs).
- Métodos mixtos y NLP (≥ 5 refs).

Adicionalmente, **"Google DeepMind / Gemini (2024): Large Language Models in Qualitative Research"** no es una referencia académica citable en APA 7. Debe reemplazarse por artículos peer-reviewed sobre LLMs en investigación cualitativa.

---

### HI-02 · Ausencia de la curva ROC y su gráfico como output

**Archivos afectados:** `DataStatistics.md`, `03_modelo_inferencial.md`, `data/outputs/`

El AUC-ROC (0.88) es mencionado en el resumen ejecutivo y en la bitácora, pero **no existe un gráfico ROC dedicado** en `data/outputs/`. Los reportes existentes incluyen:
- `07_matriz_confusion.png` ✅
- Curva ROC: **❌ AUSENTE**

Para la defensa doctoral, la curva ROC es un artefacto visual indispensable que los jurados esperan ver. Debe generarse y referenciarse en `03_modelo_inferencial.md`.

---

### HI-03 · Reporte 01 atribuye fiabilidad al ARD-VIRTU pero debería ser AMI-VIRTU

**Archivo afectado:** `data/outputs/reports/01_fiabilidad.md`

El título del reporte dice:
> *"Reporte de Consistencia Interna y Fiabilidad Psicométrica (ARD-VIRTU)"*

Sin embargo, la tabla de resultados muestra los coeficientes para las **Dimensiones Crítica, Técnica y Participativa**, que son dimensiones del instrumento **AMI-VIRTU**. El ARD-VIRTU tiene sus propios ítems (A1-A8, L1-L8) que deberían tener su propio reporte de fiabilidad por separado. La confusión entre ambos instrumentos en el título del reporte es un error que un evaluador detectará.

---

### HI-04 · Falta de declaración de supuestos del modelo logístico

**Archivos afectados:** `DataStatistics.md` (Fase 2), `Informe_Metodologico_Doctoral.md` (Sección 3)

La regresión logística requiere la verificación explícita de sus supuestos. El documento menciona VIF y Hosmer-Lemeshow, pero omite:

1. **Linealidad de los logit** (Box-Tidwell test para predictores continuos).
2. **Ausencia de outliers influyentes** (Distancia de Cook, leverage).
3. **Tamaño muestral por evento** (EPV - Events Per Variable). Con 3 predictores, se requieren mínimo 30 eventos (casos en riesgo=1) para estabilidad del modelo.

---

### HI-05 · Los reportes `_FINAL` duplicados crean ambigüedad de versión

**Archivos afectados:** `data/outputs/reports/`

Existen archivos duplicados con sufijo `_FINAL`:
- `04_triangulacion_mixta_FINAL.md` (82 bytes — casi vacío)
- `06_sintesis_ejecutiva_FINAL.md` (1316 bytes — incompleto)

Junto a sus versiones "principales" completas. Esta duplicación crea ambigüedad sobre cuál es la versión canónica, y el archivo `04_triangulacion_mixta_FINAL.md` de 82 bytes sugiere un error de ejecución o escritura incompleta.

---

### HI-06 · Justificación del uso de datos sintéticos no está suficientemente enmarcada

**Archivos afectados:** `DataStatistics.md` (Sección 1.2), `RESUMEN_EJECUTIVO.md`

El pipeline usa datos generados por Cópulas Gaussianas como etapa de validación. Aunque el documento menciona la "transición a datos reales", **no existe una declaración formal** de qué análisis se ejecutaron sobre datos sintéticos vs. reales, ni cómo los resultados del simulador influyeron en el diseño del instrumento real. Los jurados doctorales son especialmente sensibles al uso de datos sintéticos y exigen una frontera metodológica clara.

---

## 📋 HALLAZGOS MENORES (Prioridad Baja)

### Hm-01 · Caracteres extraños en múltiples documentos

**Archivos afectados:** `README.md` (L132), `RESUMEN_EJECUTIVO.md` (L46), `Validacion_Metodologica_XAI.md` (L35), `Hitos_Metodologicos_Logrados.md` (L44), `Plan_Capacitacion.md` (L57), `Bibliografia.md` (L35)

Todos estos archivos terminan con el carácter chino `导导` que es un artefacto de codificación. Debe eliminarse de todos los archivos antes de la entrega formal.

---

### Hm-02 · El `README.md` tiene un emoji mal codificado

**Archivo afectado:** `README.md` (L9)

La línea contiene `## 导` (carácter chino) antes del número de sección, probablemente un emoji de mapa/brújula que no se codificó correctamente. El documento de guía maestra debe presentarse limpio.

---

### Hm-03 · El error tipográfico en `main.py` debe corregirse

**Archivo afectado:** `main.py` (L313)

```python
print("      PROYECTO AMI-VIRTU FINALIADO CON ÉXITO      ")
#                              ↑ "FINALIADO" debería ser "FINALIZADO"
```

Aunque es código fuente, este texto aparece en la consola durante las ejecuciones de auditoría y puede registrarse en bitácoras que sean revisadas por el comité doctoral.

---

### Hm-04 · `Pendientes_analisis.md` ya no tiene utilidad como documento activo

**Archivo afectado:** `docs/Pendientes_analisis.md`

El documento declara "100% COMPLETADO" con todos los ítems marcados. Su presencia en la carpeta `docs/` puede confundir a revisores. Debería archivarse como registro histórico o renombrarse como `HISTORIAL_AVANCE.md`.

---

### Hm-05 · Ausencia de `google-generativeai` en `requirements.txt`

**Archivo afectado:** `requirements.txt`

El `README.md` documenta el uso de la API Gemini Pro/Flash para síntesis narrativa, y el código lo referencia (`qualitative_engine.py`), pero la librería `google-generativeai` no aparece en `requirements.txt`. Un tercero que clone el repositorio no podrá instalar el entorno completo correctamente.

---

### Hm-06 · Falta de sección de Limitaciones en los reportes de salida

**Archivos afectados:** `06_sintesis_ejecutiva.md`, `Informe_Metodologico_Doctoral.md`

Todo estudio doctoral debe incluir una sección de **Limitaciones del estudio**. Los reportes generados automáticamente no la incluyen. Al menos el informe de síntesis ejecutiva debería documentar:
- Alcance geográfico/institucional de la muestra.
- Limitaciones del análisis de datos sintéticos.
- Restricciones del modelo (solo variables AMI como predictores; factores socioeconómicos excluidos).
- Generalización limitada a contextos de educación virtual similar.

---

## 📐 MATRIZ DE PRIORIDADES

```
┌─────────────────────────────────────────────────────────────┐
│                     MATRIZ DE ACCIÓN                        │
├──────────┬──────────────────────────────────┬───────────────┤
│ Código   │ Descripción                      │ Prioridad     │
├──────────┼──────────────────────────────────┼───────────────┤
│ HC-01    │ Inconsistencia N=295 vs N=263     │ 🔴 CRÍTICA    │
│ HC-02    │ Ausencia de CFA                  │ 🔴 CRÍTICA    │
│ HC-03    │ Sin tamaño de efecto (d, η²)     │ 🔴 CRÍTICA    │
│ HC-04    │ McFadden R² inconsistente         │ 🔴 CRÍTICA    │
│ HC-05    │ Sin Cross-Validation              │ 🔴 CRÍTICA    │
├──────────┼──────────────────────────────────┼───────────────┤
│ HI-01    │ Bibliografía insuficiente (12 r.) │ 🟡 IMPORTANTE │
│ HI-02    │ Curva ROC ausente (gráfico)       │ 🟡 IMPORTANTE │
│ HI-03    │ Error instrumento en 01_fiab.     │ 🟡 IMPORTANTE │
│ HI-04    │ Supuestos logit incompletos       │ 🟡 IMPORTANTE │
│ HI-05    │ Archivos _FINAL duplicados        │ 🟡 IMPORTANTE │
│ HI-06    │ Datos sintéticos sin demarcar     │ 🟡 IMPORTANTE │
├──────────┼──────────────────────────────────┼───────────────┤
│ Hm-01    │ Caracteres 导导 en todos los docs │ 🟢 MENOR      │
│ Hm-02    │ Emoji roto en README              │ 🟢 MENOR      │
│ Hm-03    │ Typo "FINALIADO" en main.py       │ 🟢 MENOR      │
│ Hm-04    │ Pendientes.md obsoleto            │ 🟢 MENOR      │
│ Hm-05    │ google-generativeai no en req.txt │ 🟢 MENOR      │
│ Hm-06    │ Falta sección de Limitaciones     │ 🟢 MENOR      │
└──────────┴──────────────────────────────────┴───────────────┘
```

---

## 🛠️ PLAN DE ACCIÓN RECOMENDADO

### Semana 1 — Correcciones Críticas de Documentación (sin cambiar código)
1. **HC-01:** Definir el N canónico del estudio y unificar en todos los documentos.
2. **HC-04:** Verificar el valor real de McFadden R² en logs de ejecución y unificar.
3. **Hm-01/02/03:** Limpiar artefactos (caracteres chinos, typos, emojis rotos).
4. **HI-03:** Corregir título del reporte `01_fiabilidad.md`.
5. **HI-05:** Eliminar o archivar los archivos `_FINAL` vacíos/incompletos.

### Semana 2 — Mejoras Metodológicas (implican cambios de código)
6. **HC-03:** Implementar `pingouin.compute_effsize()` (ya está en requirements) para d de Cohen y η² en `stats_analyzer.py`.
7. **HC-05:** Implementar k-Fold CV (k=10) para validar el AUC-ROC reportado.
8. **HI-02:** Agregar generación de gráfico ROC en `reporter.py`.
9. **Hm-05:** Añadir `google-generativeai` a `requirements.txt`.

### Semana 3 — Enriquecimiento Doctoral
10. **HC-02:** Documentar decisión sobre CFA con justificación bibliográfica, o implementarlo.
11. **HI-01:** Expandir `Bibliografia.md` a ≥ 40 referencias en formato APA 7.
12. **HI-04:** Documentar verificación de supuestos del modelo logit.
13. **HI-06:** Agregar subsección clara de demarcación entre fase sintética y fase real.
14. **Hm-06:** Crear sección de Limitaciones en `06_sintesis_ejecutiva.md`.

---

## 📚 Referencias para las Correcciones

- **Tamaño de efecto:** Cohen, J. (1988). *Statistical power analysis for the behavioral sciences* (2nd ed.). Erlbaum.
- **CFA en escalas educativas:** Brown, T. A. (2015). *Confirmatory Factor Analysis for Applied Research* (2nd ed.). Guilford Press.
- **Cross-Validation en modelos educativos:** Steyerberg, E. W. (2019). *Clinical Prediction Models* (2nd ed.). Springer.
- **Supuestos regresión logística:** Hosmer, D. W., Lemeshow, S., & Sturdivant, R. X. (2013). *Applied Logistic Regression* (3rd ed.). Wiley.
- **EPV en modelos logísticos:** Peduzzi, P., et al. (1996). A simulation study of the number of events per variable in logistic regression analysis. *Journal of Clinical Epidemiology, 49*(12), 1373–1379.

---

*Auditoría realizada sobre el estado del repositorio a fecha 09 de Junio de 2026.*  
*Este documento es orientativo y no modifica ningún archivo de código fuente.*

---

## 📒 REGISTRO DE RESOLUCIONES (Changelog de Correcciones)

Este registro es un documento vivo. Cada vez que se resuelva un hallazgo, se anota aquí con fecha, acción y archivo afectado.

### ✅ Resuelto

| Fecha | Código | Acción realizada | Archivos modificados |
| :--- | :---: | :--- | :--- |
| 2026-06-09 | **HC-01** | Aclaración oficial N=295 (campo) vs N=263 (filtrado por coherencia). Se documenta qué N usa cada fase analítica. | `docs/DataStatistics.md` |
| 2026-06-09 | **HC-04** | McFadden R² corregido de 0.42 (erróneo) a **0.2442** (valor real del modelo). | `docs/RESUMEN_EJECUTIVO.md` |
| 2026-06-09 | **HI-03** | Título del reporte `01_fiabilidad.md` corregido: ARD-VIRTU → **AMI-VIRTU**. Agregada nota aclarando que ARD-VIRTU requiere reporte propio. | `data/outputs/reports/01_fiabilidad.md` |
| 2026-06-09 | **Hm-01** | Caracteres chinos `导导` eliminados por completo de todos los documentos de `docs/` y reportes (`03`, `04`, `05`, `06`, `07`). | `README.md`, `docs/Validacion_Metodologica_XAI.md`, `docs/Hitos_Metodologicos_Logrados.md`, `docs/Plan_Capacitacion.md`, `docs/RESUMEN_EJECUTIVO.md`, `data/outputs/reports/` |
| 2026-06-09 | **Hm-02** | Emoji de mapa roto corregido en sección 1 del `README.md`. | `README.md` |
| 2026-06-09 | **Hm-06** | Sección **6. Limitaciones del Estudio** agregada a `06_sintesis_ejecutiva.md` con 5 limitaciones formalmente declaradas. | `data/outputs/reports/06_sintesis_ejecutiva.md` |
| 2026-06-09 | **HI-01** (parcial) | Referencia no académica de Google DeepMind reemplazada por dos papers peer-reviewed (Touvron et al., 2023; Gilardi et al., 2023). Nota de expansión a ≥40 refs agregada. | `docs/Bibliografia.md` |
| 2026-06-09 | **HI-02** (nota) | Nota de pendiente agregada en `03_modelo_inferencial.md` señalando la ausencia de la curva ROC como gráfico. Pendiente de implementación en código. | `data/outputs/reports/03_modelo_inferencial.md` |
| 2026-06-09 | **HC-02** (nota) | Notas de pendiente agregadas en `Informe_Metodologico_Doctoral.md` sobre ausencia de CFA y opciones de implementación. | `docs/Informe_Metodologico_Doctoral.md` |
| 2026-06-09 | **HC-03** (nota) | Nota de pendiente agregada en `Informe_Metodologico_Doctoral.md` sobre ausencia de tamaños de efecto en contrastes. | `docs/Informe_Metodologico_Doctoral.md` |
| 2026-06-09 | **HC-05** (nota) | Nota de pendiente agregada en `03_modelo_inferencial.md` sobre ausencia de Cross-Validation. | `data/outputs/reports/03_modelo_inferencial.md` |
| 2026-06-09 | **HC-02** | `run_confirmatory_factor_analysis()` implementado en `stats_analyzer.py` usando Tucker's Congruence Coefficient (Φ) con split-half EFA. Ref: Lorenzo-Seva & ten Berge (2006). Resultados integrados en bitácora. | `src/analysis/stats_analyzer.py`, `main.py` |
| 2026-06-09 | **HC-03** | `run_demographic_contrasts()` extendido: T-test de Welch con **d de Cohen** + potencia observada; ANOVA con **η²** y **η² parcial**. Bitácora actualizada. | `src/analysis/stats_analyzer.py`, `main.py` |
| 2026-06-09 | **HC-05** | `run_logistic_cv()` implementado con Stratified k-Fold (k=10) usando Pipeline para evitar data-leakage. Reporta AUC media ± std + IC 95% + F1. Bitácora actualizada. | `src/analysis/stats_analyzer.py`, `main.py` |
| 2026-06-09 | **HI-02** | `plot_roc_curve()` implementado en `reporter.py`. Genera `08_roc_curve.png` con AUC anotado y umbral de Youden. Integrado en `generate_all_reports()`. | `src/utils/reporter.py`, `main.py` |
| 2026-06-09 | **Hm-03** | Typo `"FINALIADO"` corregido a `"FINALIZADO"` en `main.py` (L313). | `main.py` |
| 2026-06-09 | **Hm-05** | `google-generativeai>=0.5.0` agregado a `requirements.txt`. | `requirements.txt` |
| 2026-06-09 | **HI-03** | Ya resuelto en primera sesión: título `01_fiabilidad.md` corregido de ARD-VIRTU → AMI-VIRTU. Registrado formalmente. | `data/outputs/reports/01_fiabilidad.md` |
| 2026-06-09 | **HI-04** | `run_logit_assumption_checks()` implementado con: (1) EPV, (2) Box-Tidwell (linealidad del logit), (3) Distancia de Cook + leverage. Resultados en bitácora. Reporte `02_contrastes.md` actualizado. | `src/analysis/stats_analyzer.py`, `main.py`, `data/outputs/reports/02_contrastes.md` |
| 2026-06-09 | **HI-05** | 3 archivos duplicados/incompletos eliminados: `04_triangulacion_mixta_FINAL.md` (82 bytes), `06_sintesis_ejecutiva_FINAL.md` (incompleto), `01_fiabilidad_v2.md`. `reports/` queda con 7 archivos canónicos. | `data/outputs/reports/` |
| 2026-06-09 | **HI-02** | ✅ Ya registrado en sprint anterior: `plot_roc_curve()` en `reporter.py`. | — |
| 2026-06-09 | **HI-06** | Flujo analítico real y sintético completamente desacoplados (configuración `.env` y salidas separadas en `outputs/real/` y `outputs/synthetic/`). Documentación actualizada formalmente para demarcar y contrastar ambas fases. | `main.py`, `docs/DataStatistics.md`, `docs/RESUMEN_EJECUTIVO.md` |
| 2026-06-09 | **Hm-04** | Archivo obsoleto `Pendientes_analisis.md` renombrado a `HISTORIAL_AVANCE.md` (con título actualizado y estado formalizado) y el archivo original eliminado de `docs/`. | `docs/Pendientes_analisis.md`, `docs/HISTORIAL_AVANCE.md` |

---

### 🔄 En Progreso (Requieren cambios de código fuente)

*No hay ítems en progreso en este momento. Todos los cambios de código planeados han sido implementados.*

---

### 📌 Pendiente (Sin fecha asignada)

| Código | Descripción | Bloqueante |
| :--- | :--- | :--- |
| **HI-01** | Expandir bibliografía a ≥ 40 referencias APA 7 | Requiere revisión manual del investigador |
| **Hm-04** | Revisar y actualizar `Pendientes.md` (posiblemente obsoleto) | Revisión manual del investigador |

