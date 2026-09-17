# Capítulo 4: Resultados de la Investigación (Secciones de Depuración y OE1)

> **Documento Técnico de Integración Tesis Doctoral**  
> **Proyecto:** AMI-VIRTU & ARD-VIRTU  
> **Fecha de Certificación:** 2026-09-17 14:44:47  
> **Muestra Cuantitativa Principal Certificada:** $N = 753$ estudiantes universitarios  
> **Submuestra de Integración Cualitativa:** $N = 729$ estudiantes universitarios  
> **Hash de Integridad Base Analítica Final ($N = 753$):** `259724F4BF0F9B8EDC7C6579750B0258709F720DE2CC4A8C6739EB29C5C19BF0`  

---

## 4.1 Depuración, Validación Psicométrica y Arquitectura Muestral Dual

El proceso de recolección de información primaria en las universidades públicas seleccionadas (UNMSM, UNI, UNTELS) arrojó un total bruto inicial de **$N = 823$ cuestionarios registrados**. Con la finalidad de salvaguardar los estándares éticos internacionales y garantizar una rigurosa calidad psicométrica de los datos sin sesgar la representatividad muestral, se ejecutó un protocolo de depuración articulado en dos niveles: una delimitación inicial de la población elegible y, a partir de ella, una **arquitectura metodológica dual** que separa el análisis puramente psicométrico-cuantitativo de la integración cualitativa intra-instrumento (Tabla 4.1).

### Tabla 4.1
*Flujo metodológico de depuración y conformación de la arquitectura muestral dual*

| Etapa del Flujo | Fuente / Criterio Operativo | $N$ Previo | Casos Excluidos | % respecto $N$ previo | % Muestra Bruta | $N$ Resultante | Justificación Metodológica y Ética |
|:---|:---|---:|---:|---:|---:|---:|:---|
| **1. Muestra Bruta de Campo** | Formulario de encuesta administrado | — | — | — | — | **823** | Captura censal inicial en plataforma digital. |
| **2. Filtro Ético (Consentimiento)** | Reactivo formal de consentimiento informado | 823 | 5 | 0.61% | 0.61% | **818** | Exclusión imperativa de participantes sin consentimiento voluntario expreso (Declaración de Helsinki / Concytec). |
| **3. Filtro Metodológico (Actividad Virtual)** | Cursado de asignaturas virtuales (2022-2025) | 818 | 44 | 5.38% | 5.35% | **774** | Delimitación de la población objetivo: estudiantes con experiencia directa en entornos virtuales universitarios. |
| **4. Control de Calidad Cuantitativo Objetivo** | Detector de aquiescencia absoluta (*DataCleaner*) | 774 | 21 | 2.71% | 2.55% | **753** | Exclusión objetiva de respuestas uniformes (varianza = 0 pre-inversión en los 30 ítems AMI). |
| **MUESTRA CUANTITATIVA PRINCIPAL** | **Base analítica oficial consolidada y congelada** | — | — | — | **91.49%** | **753** | **Muestra oficial para la caracterización OE1, fiabilidad, contrastes inferenciales y modelos predictivos.** |
| *Submuestra de Integración Cualitativa (Paralela)* | Filtro de suficiencia textual en respuestas abiertas | 774 | 45 | 5.81% | 5.47% | **729** | Participantes con densidad textual suficiente para el procesamiento semántico con NLP y el *joint display* intra-instrumento. |

*Nota Metodológica sobre la Separación de Pipelines:*  
A diferencia de aproximaciones previas que utilizaban el filtro de Inteligencia Artificial para descartar sujetos de toda la investigación, el diseño metodológico adoptado establece que la ausencia o brevedad de respuesta en preguntas abiertas cualitativas opcionales no constituye causal de anulación de los 30 reactivos cerrados cuantitativos. Por consiguiente, la **Muestra Cuantitativa Principal ($N = 753$)** preserva la totalidad de participantes elegibles con respuestas Likert válidas, mientras que la **Submuestra de Integración ($N = 729$)** se reserva para los análisis mixtos concurrentes intra-instrumento.

---

### 4.1.1 Criterios de Exclusión Psicométrica Cuantitativa ($n = 21$)

La depuración psicométrica de la muestra cuantitativa se restringió estrictamente a criterios observables de invalidez de respuesta (Tabla 4.2). Se identificaron **21 participantes con varianza cero (flatliners)** en la totalidad de la escala AMI (30 reactivos en datos brutos pre-inversión). Estos sujetos marcaron idéntica opción escalar a lo largo de todo el cuestionario, ignorando los controles de polaridad semántica invertida (ítem C6). 

Asimismo, durante la auditoría metodológica se descartó la aplicación de reglas inferenciales subjetivas basadas en discordancias de autoinforme (como la regla exploratoria A2/A4, que pretendía calificar como contradictorio el percibir un rendimiento académico "Alto" habiendo desaprobado asignaturas previamente). Dado que ambas variables proceden del autoinforme del estudiante y no de un registro institucional administrativo, tal discrepancia no constituye necesariamente falsedad o error de medida, por lo que dichos registros se mantuvieron plenamente integrados en la muestra analítica.

### Tabla 4.2
*Desglose de exclusiones por patrones de respuesta anómala objetiva en la población elegible ($N = 774$)*

| Patrón Observable Detectado | Criterio Técnico Operativo | Registros ($n$) | % ($N=774$) | Acción Metodológica Realizada |
|:---|:---|---:|---:|:---|
| **Respuestas uniformes (Varianza = 0)** | Mismo valor escalar en los 30 reactivos AMI (datos brutos pre-inversión) | **21** | **2.71%** | Exclusión analítica cuantitativa |
| *— Patrón uniforme "5"* | Marcó 5 ("Totalmente de acuerdo") en los 30 ítems | 9 | 1.16% | Exclusión analítica cuantitativa |
| *— Patrón uniforme "4"* | Marcó 4 ("De acuerdo") en los 30 ítems | 6 | 0.78% | Exclusión analítica cuantitativa |
| *— Patrón uniforme "3"* | Marcó 3 ("Neutral / Ni de acuerdo ni en desacuerdo") | 5 | 0.65% | Exclusión analítica cuantitativa |
| *— Patrón uniforme "2"* | Marcó 2 ("En desacuerdo") en los 30 ítems | 1 | 0.13% | Exclusión analítica cuantitativa |
| **Escalas completamente vacías** | Omisión total de la escala AMI (30 ítems NaN) | **0** | **0.00%** | Sin casos en la cohorte elegible |
| **TOTAL EXCLUSIONES CUANTITATIVAS** | Criterio objetivo de varianza nula | **21** | **2.71%** | **Muestra cuantitativa oficial = 753** |

---

## 4.2 Caracterización del Nivel de Alfabetización Mediática e Informacional (OE1)

El primer objetivo específico de la investigación consistió en caracterizar el nivel de Alfabetización Mediática e Informacional (AMI) en los estudiantes universitarios bajo modalidad virtual, evaluado mediante una escala multidimensional de 30 reactivos distribuidos equitativamente en tres dimensiones: **Crítica** (ítems C1 a C10), **Técnica** (ítems T1 a T10) y **Participativa** (ítems P1 a P10).

### 4.2.1 Patrón de Datos Faltantes y Tratamiento mediante Imputación Iterativa Multivariada
En la muestra analítica ($N = 753$), sobre un universo de $22,590$ celdas de respuesta posibles ($753 	imes 30$), se registraron **$2,161$ valores ausentes ($9.57\%$)**. La distribución de las omisiones presentó un comportamiento marcadamente heterogéneo entre dimensiones:
* **Dimensión Crítica (C1-C10):** $1,051$ celdas faltantes (**$13.96\%$** de la dimensión), fluctuando a nivel de reactivo individual entre el $6.77\%$ (C6) y el $18.46\%$ (C10).
* **Dimensión Técnica (T1-T10):** $1,110$ celdas faltantes (**$14.74\%$** de la dimensión), oscilando entre el $4.91\%$ (T10) y el $20.98\%$ (T7).
* **Dimensión Participativa (P1-P10):** **$0$ celdas faltantes ($0.00\%$)**, registrando respuesta íntegra del $100\%$ en todos los participantes.

A nivel de participantes, el **$50.46\%$ de la muestra ($n = 382$)** completó de manera íntegra los 30 reactivos, mientras que el $49.54\%$ ($n = 371$) presentó omisiones parciales concentradas en reactivos específicos de los bloques Crítico y Técnico. Solo 2 estudiantes omitieron el bloque Crítico completo y 7 el bloque Técnico completo.

El patrón observado de datos faltantes fue estructurado y diferencial entre bloques del instrumento, lo que hace cuestionable asumir MCAR (*Missing Completely At Random*). Dada su asociación con la posición y estructura secuencial del cuestionario electrónico, el tratamiento analítico se realizó bajo un **supuesto MAR (*Missing At Random*) plausible**, sin asumir que dicho mecanismo pueda establecerse de manera definitiva a partir de los datos observados. La concentración de omisiones en determinados bloques es compatible, entre otras explicaciones posibles, con efectos de posición o fatiga de respuesta del encuestado.

Si se hubiera aplicado una eliminación por lista (*listwise deletion*), se habría descartado innecesariamente a casi la mitad de la cohorte útil ($n = 373$), reduciendo drásticamente la potencia estadística. En consecuencia, el tratamiento de valores ausentes se ejecutó mediante **imputación iterativa multivariada mediante ecuaciones encadenadas (`IterativeImputer`, semilla fija 42, 10 iteraciones)**, implementada en esta fase como imputación única con redondeo y acotamiento al rango de enteros Likert $[1, 5]$. Este procedimiento se adoptó para aprovechar la información multivariada disponible y preservar, en mayor medida que una imputación univariada simple, la estructura de asociación entre variables, reconociendo que no incorpora la modelación de variabilidad entre imputaciones propia de un marco de imputación múltiple con reglas de Rubin.

### Tabla 4.3
*Estadísticos descriptivos de las dimensiones y puntaje global AMI en la muestra cuantitativa oficial ($N = 753$)*

| Variable / Dimensión AMI | $N$ Válido | $N$ Faltante | Media ($M$) | Error Est. | Desv. Est. ($DE$) | Mediana ($Md$) | Mínimo | Máximo | P25 | P75 | IQR | Asimetría | Curtosis |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| **Dimensión Crítica** | 753 | 0 | **3.6345** | 0.0195 | 0.5359 | 3.7000 | 1.9000 | 5.0000 | 3.3000 | 4.0000 | 0.7000 | -0.2190 | 0.4384 |
| **Dimensión Técnica** | 753 | 0 | **3.4404** | 0.0186 | 0.5116 | 3.5000 | 1.0000 | 5.0000 | 3.1000 | 3.7000 | 0.6000 | -0.1359 | 0.7725 |
| **Dimensión Participativa** | 753 | 0 | **3.4683** | 0.0218 | 0.5995 | 3.4000 | 1.5000 | 5.0000 | 3.1000 | 3.9000 | 0.8000 | -0.0706 | -0.3607 |
| **Score AMI Global** | 753 | 0 | **3.5144** | 0.0177 | 0.4868 | 3.5000 | 1.9000 | 5.0000 | 3.2000 | 3.8333 | 0.6333 | -0.0839 | 0.1868 |

---

### 4.2.2 Clasificación por Niveles Relativos a la Muestra (Terciles Empíricos)

De conformidad con el marco del estudio, la categorización en niveles de alfabetización (**Bajo**, **Medio**, **Alto**) se realizó aplicando el criterio de **terciles empíricos calculados directamente sobre la distribución observada ($N = 753$)**, estableciendo formalmente:
* **Nivel Bajo:** $Score \le P_{33}$
* **Nivel Medio:** $Score > P_{33} \land Score \le P_{66}$
* **Nivel Alto:** $Score > P_{66}$

> **Declaración Epistemológica de Relatividad Muestral:**  
> Esta clasificación es estrictamente **relativa a la muestra analizada**. Describe la posición ordinal de un estudiante en comparación con sus pares de la presente cohorte y no debe confundirse con una evaluación de suficiencia basada en normas poblacionales externas o estándares universales de competencia digital.

### Tabla 4.4
*Distribución muestral por niveles de Alfabetización Mediática e Informacional ($N = 753$)*

| Dimensión AMI | Corte $P_{33}$ | Corte $P_{66}$ | Nivel Bajo ($Score \le P_{33}$) | Nivel Medio ($P_{33} < Score \le P_{66}$) | Nivel Alto ($Score > P_{66}$) | Empates en $P_{33}$ | Empates en $P_{66}$ |
|:---|---:|---:|---:|---:|---:|---:|---:|
| **Dimensión Crítica** | 3.4000 | 3.8000 | **253 (33.60%)** | **258 (34.26%)** | **242 (32.14%)** | 60 | 87 |
| **Dimensión Técnica** | 3.2667 | 3.6000 | **251 (33.33%)** | **268 (35.59%)** | **234 (31.08%)** | 0 | 103 |
| **Dimensión Participativa** | 3.2000 | 3.8000 | **291 (38.65%)** | **240 (31.87%)** | **222 (29.48%)** | 55 | 33 |
| **Score AMI Global** | 3.3333 | 3.7333 | **265 (35.19%)** | **247 (32.80%)** | **241 (32.01%)** | 22 | 16 |

*Interpretación Psicométrica:*  
El promedio global de Alfabetización Mediática e Informacional se situó en **$3.5144$** en la escala Likert continua de 1 a 5, ubicándose por encima del punto neutral teórico (3.0000). La dimensión con mayor puntaje promedio fue la **Crítica** ($M = 3.6345$), seguida de la dimensión **Participativa** ($M = 3.4683$) y la **Técnica** ($M = 3.4404$). Los coeficientes de asimetría y curtosis cercanos a cero evidencian una distribución simétrica adecuada y sin efecto techo o piso restrictivo.

---

## 4.3 Análisis Descriptivo de Sensibilidad y Robustez Metodológica

Para contrastar el impacto de las decisiones de depuración y documentar con rigor la transición entre versiones del pipeline analítico, se ejecutó un **análisis descriptivo de sensibilidad** comparando la muestra cuantitativa oficial consolidada (**$N = 753$**) frente a la versión preliminar histórica restringida (**$N = 702$**) (Tabla 4.5).

Dado que los 702 sujetos históricos se encuentran contenidos dentro de los 753 casos de la muestra oficial ($702 \subset 753$), ambas muestras están anidadas y no son independientes, por lo que la aplicación de pruebas inferenciales de hipótesis para muestras independientes (como el estadístico $t$ de Welch) resulta metodológicamente inapropiada. Por tanto, el análisis de robustez se formaliza mediante la magnitud absoluta de las diferencias de medias ($\Delta M = M_{753} - M_{702}$), el cambio porcentual ($\%\Delta$) y la diferencia estandarizada expresada en unidades de desviación estándar de la muestra oficial ($\Delta / DE_{753}$).

### Tabla 4.5
*Comparación de robustez descriptiva entre la muestra oficial ($N=753$) y la muestra restringida histórica ($N=702$)*

| Dimensión AMI | Media Oficial ($N=753$) | Media Histórica ($N=702$) | Diferencia Absoluta ($\Delta M$) | % Cambio Relativo | Diferencia Estandarizada ($\Delta / DE_{753}$) | Diagnóstico Metodológico |
|:---|---:|---:|---:|---:|---:|:---|
| **Dimensión Crítica** | 3.6345 | 3.6698 | -0.0353 | -0.97% | **-0.0658** | **Robusto / Diferencia trivial (|Delta/DE| < 0.10)** |
| **Dimensión Técnica** | 3.4404 | 3.4655 | -0.0252 | -0.73% | **-0.0492** | **Robusto / Diferencia trivial (|Delta/DE| < 0.10)** |
| **Dimensión Participativa** | 3.4683 | 3.4973 | -0.0290 | -0.84% | **-0.0484** | **Robusto / Diferencia trivial (|Delta/DE| < 0.10)** |
| **Score AMI Global** | 3.5144 | 3.5442 | -0.0298 | -0.85% | **-0.0613** | **Robusto / Diferencia trivial (|Delta/DE| < 0.10)** |

*Conclusión de Robustez:*  
Los resultados indican que la caracterización descriptiva del OE1 es **robusta ante la reincorporación de los casos que habían sido excluidos en iteraciones preliminares**. La diferencia observada en las medias no supera en ningún caso los **0.036 puntos** en la escala de 1 a 5 (cambio porcentual inferior al $0.97\%$), representando menos de **0.07 desviaciones estándar**. Por consiguiente, las inferencias y conclusiones del estudio no se ven afectadas por la exclusión previa de casos cualitativos o por la eliminación de la regla exploratoria A2/A4.

---

## 4.4 Auditoría del Componente Cualitativo y Marco Ético

### 4.4.1 Integración Concurrente Intra-Instrumento Asistida por IA
El componente cualitativo de la investigación está conformado por las respuestas narrativas abiertas recopiladas dentro del mismo formulario de campo (campos BC1-BC4, BT1-BT4, BP1-BP4). Este esquema responde a un **diseño mixto concurrente intra-instrumento**, donde la recolección cuantitativa y cualitativa ocurre de manera simultánea en el mismo cuestionario autoadministrado.

En etapas tempranas del proyecto, el indicador generado por el modelo de lenguaje se denominó bajo la etiqueta de "disonancia cognitiva". La auditoría metodológica determinó que dicha formulación era conceptualmente impropia: los modelos algorítmicos no realizan diagnósticos psicológicos. En la versión definitiva de la tesis, dicho componente se define formalmente como un **índice de coherencia textual de integración concurrente**, diseñado para evaluar la consistencia semántica entre el discurso del participante y sus autopercepciones Likert.

### 4.4.2 Harness de Validación Computacional de la Submuestra Cualitativa
El análisis retrospectivo de los 45 casos con puntaje cualitativo $< 0.60$ reveló que su calificación obedeció primordialmente a un fenómeno de **baja densidad o ausencia de discurso textual**, y no a contradicciones conceptuales profundas:
* La longitud promedio del texto en los participantes con suficiencia textual ($N = 729$) fue de **698.2 caracteres**, mientras que en los 45 casos excluidos de la submuestra fue de apenas **224.9 caracteres**.
* El promedio de preguntas abiertas omitidas o con respuestas monosilábicas (*"ninguna"*, *"no opina"*) en los 45 casos fue de **4.91 respuestas vacías**, frente a un promedio de apenas **0.25** en los participantes retenidos.
* Este hallazgo justifica plenamente la decisión de separar los pipelines: **un estudiante no debe ser excluido del análisis cuantitativo de AMI por el hecho de haber respondido con brevedad preguntas abiertas opcionales**, preservando su información en la muestra cuantitativa oficial ($N = 753$).

### 4.4.3 Salvaguardas Éticas y Anonimización por Diseño
1. **Anonimización Irrevocable:** Previo a cualquier interacción con la API de procesamiento del lenguaje, todos los campos de información personal identificatoria (nombres, apellidos, DNI, correos electrónicos, códigos de matrícula) fueron purgados mediante el módulo `pii_filter`, garantizando que ninguna información sensible fuese transmitida externamente.
2. **Rol Auxiliar de la IA:** La Inteligencia Artificial actúa exclusivamente como instrumento de procesamiento textual estructurado. Las decisiones metodológicas de inclusión y exclusión muestral descansan en criterios epistemológicos humanos y comprobación estadística transparente.

---

## 4.5 Notas de Corrección Psicométrica y Auditoría Forense

1. **Corrección de Consistencia Interna en la Dimensión Crítica:**  
   En versiones iniciales de los reportes automatizados, la dimensión Crítica figuraba con un coeficiente Alfa de Cronbach de $0.7937$. La auditoría demostró que este valor se debió a una segunda inversión redundante aplicada al reactivo C6 dentro de la función `calculate_reliability` de `stats_analyzer.py` (revirtiéndolo accidentalmente a su escala no invertida). Con la escala correctamente unificada, la dimensión Crítica alcanza en la muestra oficial ($N = 753$) un Alfa de Cronbach de **$0.8673$**, que certifica una **alta consistencia interna**, mientras que la escala AMI Global de 30 ítems alcanza un Alfa de **$0.9112$**, acreditando una **excelente consistencia psicométrica**.

2. **Alcance de la Imputación Iterativa:**  
   La imputación de valores ausentes se ejecutó mediante ecuaciones encadenadas (`IterativeImputer`), preservando la estructura de covarianzas multivariadas entre reactivos. Dado que no se aplicaron reglas de combinación de Rubin para modelar la varianza entre múltiples imputaciones, el procedimiento se reporta formalmente como una imputación única iterativa multivariada, adecuada para los análisis univariados y multivariados del OE1.

3. **Prevalencia de la Variable Riesgo Total:**  
   En la muestra analítica oficial ($N = 753$), la variable multidimensional `Riesgo_Total` identifica a **261 estudiantes (34.66%)** en situación de vulnerabilidad académica o digital, frente a **492 estudiantes (65.34%)** sin indicadores de riesgo, constituyendo la base empírica para la contrastación de los objetivos específicos subsiguientes (OE2 y OE3).
