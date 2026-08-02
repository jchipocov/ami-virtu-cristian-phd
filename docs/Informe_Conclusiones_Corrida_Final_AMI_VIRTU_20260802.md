# Informe de conclusiones de la corrida analítica ampliada
## Modelamiento predictivo, validación psicométrica, XAI y segmentación

**Proyecto:** Proyecto Doctoral AMI-VIRTU & ARD-VIRTU  
**Para:** Asesoría doctoral / Capítulo de resultados  
**Autor:** [Nombre del autor]  
**Fecha:** 2 de agosto de 2026  
**Pipeline:** `main.py` — modelo principal `RandomForestClassifier`  
**Muestra:** 823 registros brutos; 702 casos en la muestra analítica final

---

## 1. Resumen ejecutivo

La corrida ampliada consolidó una muestra analítica final de **702 estudiantes**, obtenida a partir de 823 registros brutos. Se excluyeron 94 casos por target inválido y 27 casos sospechosos identificados mediante controles de ocultamiento y aquiescencia. La variable objetivo fue **Riesgo_Binario**, construida a partir de `Score_Riesgo_Total >= 3.0`; por tanto, los resultados se refieren a **riesgo estimado** y no a deserción observada.

Los resultados muestran tres hallazgos principales. Primero, el instrumento presenta una base psicométrica sólida: KMO de **0.9209**, prueba de Bartlett significativa, consistencia interna adecuada o alta y una replicabilidad factorial global elevada mediante split-half EFA y Tucker’s Φ (**Φ media = 0.9430**). Segundo, la AMI se relaciona de forma inversa y consistente con las distintas dimensiones de riesgo, con asociaciones especialmente relevantes frente al riesgo académico y al riesgo LMS. Tercero, existe una señal predictiva real, aunque de magnitud moderada. Entre los modelos comparados, **Random Forest obtuvo el mejor equilibrio general** entre discriminación, sensibilidad, precisión y estabilidad clasificatoria.

La conclusión central no es que la AMI explique por sí sola todo el riesgo estudiantil, sino que constituye un conjunto de competencias con valor empírico para identificar vulnerabilidad educativa. El modelo puede emplearse como herramienta de **tamizaje o priorización**, pero no como diagnóstico definitivo ni como sustituto de la evaluación académica y tutorial.

### Cifras clave

| Área | Indicador | Resultado |
|---|---|---:|
| Muestra | Casos analíticos finales | **702** |
| Target | Prevalencia de riesgo | **32.34%** |
| Psicometría | KMO | **0.9209** |
| Replicabilidad | Tucker’s Φ media | **0.9430** |
| Asociación | AMI global vs. riesgo académico | **r = -0.464** |
| Asociación | AMI global vs. riesgo LMS | **r = -0.472** |
| Modelo principal CV | AUC-ROC | **0.6692** |
| Modelo principal CV | PR-AUC | **0.5363** |
| Modelo principal CV | Recall | **0.7181** |
| Modelo principal holdout | AUC-ROC | **0.7406** |
| Modelo principal holdout | Balanced Accuracy | **0.6870** |

---

## 2. Integridad y trazabilidad de la muestra

El flujo de datos quedó documentado de la siguiente manera:

| Etapa | Registros |
|---|---:|
| Registros brutos | 823 |
| Excluidos por target inválido | 94 |
| Registros estructuralmente válidos | 729 |
| Casos sospechosos excluidos | 27 |
| **Muestra analítica final** | **702** |

La muestra final contiene **227 casos positivos de riesgo** y **475 casos negativos**, equivalentes a una prevalencia positiva de **32.34%**. La definición explícita del target fortalece la reproducibilidad del análisis y evita confundir el riesgo estimado con la deserción real.

---

## 3. Resultados psicométricos y estructurales

### 3.1 Consistencia interna

| Dimensión | Alpha de Cronbach | Omega de McDonald | Interpretación |
|---|---:|---:|---|
| AMI crítica | 0.7937 | 0.8095 | Adecuada |
| AMI técnica | 0.7882 | 0.8040 | Adecuada |
| AMI participativa | 0.7402 | 0.7550 | Aceptable |
| Riesgo académico | 0.7956 | 0.8115 | Adecuada |
| Riesgo LMS | 0.9115 | 0.9297 | Excelente |

Los coeficientes evidencian que las escalas mantienen niveles satisfactorios de consistencia interna. La dimensión participativa presenta los valores más bajos, pero permanece dentro de un rango aceptable para investigación social aplicada.

### 3.2 Adecuación factorial

- **KMO:** 0.9209.
- **Bartlett:** p < 0.0001.
- **Varianza total explicada:** 41.89%.
- **Interpretación del EFA:** estructura válida.

Estos resultados indican que la matriz de correlaciones es adecuada para el análisis factorial y que los ítems comparten suficiente varianza común.

### 3.3 Replicabilidad mediante split-half EFA

| Factor | Tucker’s Φ | Interpretación |
|---|---:|---|
| Crítico | 0.9660 | Excelente replicabilidad |
| Técnico | 0.9567 | Excelente replicabilidad |
| Participativo | 0.9062 | Replicabilidad adecuada |
| **Media global** | **0.9430** | **Replicabilidad alta** |

La estructura de tres dimensiones muestra una elevada estabilidad al dividir la muestra en dos mitades. Este resultado constituye evidencia de **replicabilidad factorial**, no una CFA convencional. En consecuencia, debe evitarse presentar Tucker’s Φ como sustituto de índices CFA tales como CFI, TLI, RMSEA o SRMR.

---

## 4. Asociaciones entre AMI y riesgo multidimensional

Las 16 pruebas de asociación fueron corregidas mediante Benjamini-Hochberg con FDR de 0.05. Todas conservaron significación estadística.

### 4.1 Resultados principales para AMI global

| Dimensión de riesgo | Pearson r | Tamaño del efecto | Lectura |
|---|---:|---|---|
| Riesgo total | -0.203 | Pequeño | A mayor AMI, menor riesgo global |
| Riesgo académico | -0.464 | Moderado | Asociación inversa sustantiva |
| Riesgo LMS | -0.472 | Moderado | Asociación inversa sustantiva |
| Riesgo de continuidad | -0.290 | Pequeño | Asociación inversa consistente |

El patrón es claro: los estudiantes con mayores competencias de alfabetización mediática e informacional tienden a presentar menores niveles de riesgo, especialmente en las dimensiones académica y de interacción con el LMS. Entre las asociaciones específicas, destaca la relación entre **AMI crítica y riesgo LMS** (Pearson r = -0.485; Spearman ρ = -0.512).

Estos resultados respaldan con mayor fuerza una interpretación **asociativa** que causal. La evidencia permite afirmar que AMI y riesgo covarían de forma consistente, pero no que una dimensión cause por sí sola la reducción del riesgo.

---

## 5. Comparación de modelos predictivos

Se compararon tres modelos mediante el mismo esquema de validación cruzada repetida y predicciones out-of-fold.

| Modelo | AUC | PR-AUC | Recall | Precision | Balanced Accuracy | MCC |
|---|---:|---:|---:|---:|---:|---:|
| Regresión logística | 0.6197 | 0.4797 | 0.7621 | 0.3673 | 0.5674 | 0.1341 |
| **Random Forest** | **0.6692** | 0.5363 | 0.7181 | **0.3947** | **0.5959** | **0.1822** |
| Gradient Boosting | 0.6579 | **0.5368** | **0.7753** | 0.3761 | 0.5803 | 0.1594 |

### 5.1 Selección del modelo principal

**Random Forest fue seleccionado como modelo principal** porque presentó el mejor equilibrio global:

- mayor AUC;
- mayor precisión;
- mayor Balanced Accuracy;
- mayor MCC;
- recall superior a 0.70;
- PR-AUC prácticamente equivalente al de Gradient Boosting.

Gradient Boosting alcanzó el recall más alto, pero lo hizo con menor precisión y menor equilibrio global. La regresión logística mostró una sensibilidad alta, aunque con menor discriminación y menor capacidad de clasificación balanceada.

### 5.2 Interpretación de la validación cruzada

El Random Forest obtuvo:

- **AUC-ROC:** 0.6692 ± 0.0528;
- **PR-AUC:** 0.5363 ± 0.0578;
- **Recall OOF:** 0.7181;
- **Precision OOF:** 0.3947;
- **Balanced Accuracy OOF:** 0.5959;
- **MCC OOF:** 0.1822.

El modelo detecta aproximadamente siete de cada diez casos positivos, pero genera una proporción relevante de falsas alarmas. Para una herramienta de alerta temprana, este comportamiento puede ser útil cuando el costo de omitir a un estudiante vulnerable es mayor que el costo de revisar una alerta adicional. Sin embargo, la precisión limitada obliga a que las alertas sean verificadas por personal académico o tutorial.

### 5.3 Evaluación holdout

La evaluación final en holdout produjo:

| Métrica | Resultado |
|---|---:|
| Accuracy | 0.7299 |
| AUC-ROC | 0.7406 |
| Precision | 0.6250 |
| Recall | 0.5479 |
| Specificity | 0.8261 |
| Balanced Accuracy | 0.6870 |
| PR-AUC | 0.6018 |
| MCC | 0.3870 |

Matriz de confusión:

|  | Predicho sin riesgo | Predicho en riesgo |
|---|---:|---:|
| Real sin riesgo | 114 | 24 |
| Real en riesgo | 33 | 40 |

El holdout muestra mejor discriminación y precisión que la validación cruzada. Para la redacción doctoral, las métricas de validación cruzada deben considerarse la estimación principal de generalización, mientras que el holdout funciona como evidencia complementaria.

---

## 6. Interpretabilidad mediante SHAP

En el modelo Random Forest, la importancia global por dimensión fue:

| Dimensión | mean(|SHAP|) |
|---|---:|
| AMI crítica | **0.3529** |
| AMI participativa | **0.3321** |
| AMI técnica | **0.3150** |

La dimensión crítica presentó la mayor magnitud predictiva promedio, seguida de la participativa y la técnica. Esta jerarquía indica cuánto utiliza el modelo cada dimensión para producir sus predicciones, pero no establece por sí sola:

- la dirección del efecto;
- una relación causal;
- la estabilidad del ranking entre folds;
- que una puntuación alta o baja incremente necesariamente el riesgo.

Por ello, los resultados SHAP deben presentarse como evidencia explicativa **exploratoria y de magnitud predictiva**, no como prueba causal. La estabilidad inter-folds y el bootstrap de rankings no fueron calculados en esta corrida.

---

## 7. Segmentación y perfiles estudiantiles

Los métodos de clustering identificaron una estructura interpretable de tres perfiles:

1. **Perfil de AMI alta y riesgo bajo:** competencias elevadas en las tres dimensiones y menor prevalencia de riesgo.
2. **Perfil de AMI baja y riesgo alto:** menores competencias y mayor prevalencia de riesgo.
3. **Perfil intermedio:** niveles medios de AMI y riesgo.

El consenso entre algoritmos fue moderado (**ARI = 0.4681**). Los criterios empíricos no identificaron un único K óptimo:

- Silhouette de K-Means favoreció **K=2**;
- BIC de GMM favoreció **K=4**;
- **K=3** fue retenido por su alineación con el diseño teórico y por su utilidad descriptiva.

En consecuencia, los tres perfiles son defendibles como una solución teórica e interpretativa, pero no deben presentarse como la única estructura posible de los datos.

---

## 8. Estado de las hipótesis doctorales

| Hipótesis | Estado | Evidencia principal | Formulación recomendada |
|---|---|---|---|
| **H1: AMI se relaciona con el riesgo estudiantil** | **Respaldada** | Asociaciones inversas significativas; r global de -0.203 a -0.472 | La AMI se asocia inversamente con el riesgo, especialmente académico y LMS |
| **H1 predictiva** | **Respaldada parcialmente** | RF CV AUC=0.6692 y PR-AUC=0.5363 | Existe señal predictiva moderada, no determinista |
| **H2: estructura tridimensional de AMI** | **Fuertemente respaldada en replicabilidad** | Φ media=0.9430; KMO=0.9209; confiabilidad adecuada | La estructura es estable en split-half EFA; CFA convencional pendiente si fue comprometida |
| **H4: perfiles estudiantiles diferenciados** | **Respaldada exploratoriamente** | Perfiles coherentes; ARI=0.4681 | K=3 es una solución teórica útil, no el único óptimo empírico |

---

## 9. Conclusiones generales

1. **El instrumento posee una base psicométrica sólida.** La consistencia interna, el KMO y la replicabilidad de las cargas factoriales permiten sostener que las dimensiones crítica, técnica y participativa representan componentes diferenciables y suficientemente estables de la AMI.

2. **La AMI mantiene una relación inversa consistente con el riesgo.** Las asociaciones son más intensas frente al riesgo académico y al riesgo LMS, lo que sugiere que estas competencias son especialmente relevantes para la adaptación y permanencia en entornos virtuales.

3. **La capacidad predictiva es real, pero moderada.** El Random Forest supera a la regresión logística en AUC, PR-AUC, Balanced Accuracy y MCC, demostrando que las variables AMI contienen información útil para clasificar niveles de riesgo.

4. **Random Forest ofrece el mejor equilibrio operativo.** Gradient Boosting detecta más casos positivos, pero Random Forest produce un balance superior entre sensibilidad, precisión y discriminación. Por ello, debe mantenerse como modelo principal y Gradient Boosting como modelo comparativo.

5. **El sistema es más apropiado para tamizaje que para diagnóstico.** El recall OOF de 0.7181 favorece la detección de estudiantes potencialmente vulnerables, pero la precisión de 0.3947 implica que las alertas necesitan revisión humana antes de activar intervenciones.

6. **Los resultados no demuestran no linealidad por sí solos.** El mejor desempeño de los ensambles frente a la regresión logística es compatible con la presencia de interacciones o umbrales, pero la corrida no incluyó una comparación formal que permita concluir que la relación sea necesariamente no lineal.

7. **SHAP aporta interpretabilidad, no causalidad.** La dimensión crítica presentó la mayor magnitud predictiva global, pero la dirección y estabilidad de los efectos permanecen pendientes de evaluación específica.

8. **La segmentación aporta una tipología útil, aunque exploratoria.** Los perfiles alto, medio y bajo facilitan la interpretación educativa, pero K=3 debe justificarse desde el marco teórico y no como único óptimo empírico.

9. **La tesis cuenta con resultados defendibles.** Su fortaleza principal está en la convergencia entre evidencia psicométrica, asociaciones estadísticas, comparación predictiva y segmentación. La contribución debe formularse como un modelo integrador de identificación de riesgo, no como una herramienta definitiva de predicción de deserción.

---

## 10. Recomendaciones para la redacción y defensa

### 10.1 Mensaje central para el tribunal

> La investigación demuestra que la Alfabetización Mediática e Informacional constituye una señal relevante y multidimensional del riesgo estudiantil. Su valor no radica en determinar de forma absoluta quién abandonará los estudios, sino en aportar evidencia reproducible para priorizar acompañamiento académico y tutorial.

### 10.2 Cómo presentar el modelo

- Presentar **Random Forest** como modelo principal.
- Presentar **Gradient Boosting** como contraste con mayor sensibilidad.
- Usar la validación cruzada como estimación principal.
- Usar el holdout como confirmación complementaria.
- Evitar llamar “deserción” al target cuando se trata de riesgo estimado.
- Evitar afirmar causalidad o no linealidad demostrada.
- Presentar SHAP como magnitud predictiva exploratoria.
- Describir K=3 como solución teórica e interpretable.

### 10.3 Próximos pasos de cierre

- [x] Consolidar la muestra final de 702 casos.
- [x] Comparar regresión logística, Random Forest y Gradient Boosting.
- [x] Seleccionar Random Forest como modelo principal.
- [x] Optimizar el threshold sin utilizar el holdout.
- [ ] Ejecutar, solo si el cronograma lo permite, una optimización pequeña de Random Forest y conservar el modelo actual si no existe una mejora clara.
- [ ] Congelar las métricas definitivas y trasladarlas al Capítulo IV.
- [ ] Redactar discusión, limitaciones y conclusiones con el lenguaje metodológico señalado en este informe.

---

## 11. Dictamen final

La corrida ampliada puede considerarse **científicamente útil y defendible para una tesis doctoral**. La evidencia psicométrica y asociativa es sólida; la evidencia predictiva es moderada pero superior a los baselines; y la segmentación aporta una lectura interpretativa coherente. El modelo no debe venderse como un predictor perfecto ni como sustituto del juicio académico, sino como un sistema de apoyo para detectar patrones de vulnerabilidad y orientar intervenciones tempranas.

**Modelo principal recomendado:** Random Forest.  
**Modelo comparativo:** Gradient Boosting.  
**Estado global:** resultados consolidados con mejoras predictivas opcionales antes del cierre definitivo.
