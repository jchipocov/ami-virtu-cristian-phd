# Informe de Arquitectura Analítica: Ecosistema AMI-VIRTU & ARD-VIRTU
**Destinatario:** Comité Doctoral / Asesor de PhD
**Propósito:** Presentar el pipeline analítico, su lógica metodológica y su contribución al análisis del riesgo de deserción en entornos virtuales.

## Enfoque General del Estudio
Este sistema analítico ha sido diseñado para examinar cómo los niveles de alfabetización mediática e informacional (AMI) se relacionan estadísticamente con distintos patrones de permanencia, riesgo académico o deserción en estudiantes de entornos virtuales. La arquitectura no busca establecer relaciones causales simplistas, sino generar evidencia robusta sobre asociaciones, patrones predictivos y perfiles estudiantiles, integrando métodos psicométricos, inferenciales, de aprendizaje automático y análisis cualitativo avanzado.

## 1. Preparación y Consistencia del Dato
La primera fase del pipeline tiene como propósito garantizar que los datos sean coherentes, comparables y analíticamente válidos. En esta etapa se realiza la anonimización de información personal bajo un enfoque de *privacy by design*, se revisan valores faltantes y se estandariza la codificación de respuestas tipo Likert. Aunque estas escalas son de naturaleza ordinal, se tratan como aproximaciones continuas bajo el supuesto de equidistancia entre categorías (*Assumption of Equidistant Categories*). Como se establece en la literatura psicométrica: *"Although Likert-type items are ordinal by nature, they are treated as approximately continuous under the assumption of equidistant categories, which is common in psychometric modeling when scale reliability is high and item aggregation is performed"*. Un aspecto clave es la corrección de ítems redactados en sentido inverso mediante la transformación $f(x)=6-x$, asegurando la coherencia interpretativa del constructo.

## 2. Validación Psicométrica del Instrumento
Antes de analizar la relación con la deserción, se demuestra que el instrumento **AMI-VIRTU** mide de forma consistente el constructo teórico. La consistencia interna se evalúa mediante el Alfa de Cronbach y el coeficiente **Omega de McDonald**, el cual ofrece una estimación más robusta al no depender del supuesto de tau-equivalencia. Adicionalmente, se valida la adecuación muestral mediante las pruebas de **KMO (Kaiser-Meyer-Olkin)** y **Esfericidad de Bartlett**, procediendo con un **Análisis Factorial Exploratorio (EFA)**. Se utiliza el método de extracción de Máxima Verosimilitud (o Ejes Principales) con rotación oblicua (**Oblimin** o Promax), permitiendo la intercorrelación teórica entre las dimensiones crítica, técnica y participativa, validando así la estructura latente del constructo.

## 3. Análisis Inferencial y Modelamiento Estadístico
Una vez validado el instrumento, el análisis se orienta a examinar la relación entre AMI y deserción mediante **Regresión Logística Binaria**. El objetivo es estimar la asociación entre los niveles de AMI y la probabilidad de riesgo, calculando *Odds Ratios*, intervalos de confianza y niveles de significancia estadística ($p < .05$). El rigor del modelo se garantiza mediante diagnósticos de **Multicolinealidad (VIF < 5)**, pruebas de bondad de ajuste de **Hosmer-Lemeshow ($p > 0.05$)**, el **Pseudo R² de McFadden** y el análisis de discriminación mediante la curva **ROC/AUC**. Para la clasificación final, se utiliza el **Índice de Youden** para determinar el umbral óptimo que maximiza la sensibilidad en la detección de riesgo.

## 4. Análisis de Moderación y Multidimensionalidad del Riesgo
El modelo se amplía incorporando términos de interacción para evaluar si la relación entre AMI y deserción varía según condiciones moderadoras. Un aporte clave de esta arquitectura es el **Desglose Multidimensional del Riesgo (ARD-VIRTU)**, el cual separa la vulnerabilidad en tres dimensiones: **Académica** (desempeño y autoeficacia), **Comportamiento LMS** (interacción digital) y **Continuidad**. Esto permite una inferencia más precisa sobre el tipo de apoyo que requiere cada estudiante.

## 5. Interpretabilidad mediante IA Explicable (XAI)
Se incorpora **SHAP (SHapley Additive exPlanations)** como herramienta de interpretabilidad post-hoc. Mientras la regresión logística identifica asociaciones a nivel de variables agregadas bajo un marco inferencial, SHAP permite observar la contribución de los **30 ítems individuales** en la probabilidad estimada de riesgo. Es fundamental precisar que *"SHAP was used as a complementary interpretability layer, not as a substitute for inferential statistics"*, proporcionando una capa de transparencia analítica sobre el peso relativo de cada reactivo.

## 6. Segmentación Multivariada y Consenso (Clustering)
Se aplican técnicas de clustering (ensamble de **K-Means, Ward, DBSCAN y GMM**) para identificar perfiles diferenciados. La estabilidad de estos grupos se valida mediante el **Coeficiente de Silueta**, el **Criterio de Información Bayesiano (BIC)** y el **Adjusted Rand Index (ARI)**, el cual cuantifica el consenso entre algoritmos. La taxonomía resultante se basa en esta convergencia, permitiendo reconocer patrones como estudiantes vulnerables, adaptativos o competentes con alta robustez estadística.

## 7. Componente Cualitativo y NLP
Se integran técnicas de **NLP** sobre respuestas abiertas mediante modelos basados en **Transformers (Gemini Flash)**. Esta arquitectura permite realizar un análisis semántico para extraer sentimientos y perfiles narrativos. El rigor se garantiza mediante un proceso de **validación de coherencia**, donde el modelo calcula un índice de alineación entre el discurso cualitativo y las respuestas cuantitativas, asegurando la triangulación validada.

## 8. Triangulación Analítica y Reproducibilidad Forense
Finalmente, se integran los resultados cuantitativos y cualitativos para validar la coherencia de los hallazgos. Para garantizar la integridad científica, el pipeline implementa un sistema de **Hashing SHA-256** que verifica la inmutabilidad del dataset antes de cada análisis. La ejecución bajo condiciones de estricta **reproducibilidad** incluye el uso de semillas fijas (`random_state`) y auditoría de entorno (`VerifyEnv`), asegurando que los resultados puedan ser auditados por evaluadores externos con total transparencia académica.

---
*Este documento constituye el sustento metodológico oficial para el reporte de resultados del ecosistema AMI-VIRTU & ARD-VIRTU.*
