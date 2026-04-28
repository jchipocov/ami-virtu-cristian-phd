# Resumen Ejecutivo Integral del Proyecto: AMI-VIRTU & ARD-VIRTU

## 1. Contexto Académico y el Eje de la Literacidad
La **Alfabetización Mediática e Informacional (AMI)** no es una competencia aislada; es el núcleo que permite a los ciudadanos digitales navegar, discernir y crear contenido en un ecosistema mediático saturado. En esta investigación doctoral, se define como el factor determinante en la permanencia de los estudiantes universitarios. El proyecto AMI-VIRTU descompone este constructo en tres dimensiones críticas: la **crítica** (discernimiento de veracidad), la **técnica** (dominio de plataformas LMS) y la **participativa** (interacción ética y proactiva).

## 2. Origen del Proyecto y Objetivos de Investigación
El proyecto surge ante la necesidad de crear una arquitectura computacional robusta para validar la hipótesis central de la tesis: *"Existe una relación inversa significativamente fuerte entre el nivel AMI y el riesgo de deserción virtual"*.

### Instrumentos Validados:
- **AMI-VIRTU:** Evaluación psicométrica de competencias informacionales (30 ítems).
- **ARD-VIRTU:** Sistema de detección de riesgo académico y de deserción.

## 3. Arquitectura del Sistema: De la Simulación a la Industrialización
El software ha sido desarrollado bajo principios de **Programación Orientada a Objetos (OOP)** en Python 3.11, garantizando que el pipeline sea reproducible y auditable científicamente.

### Módulos del Pipeline:
- **Simulación Avanzada (`src/simulation`):** Uso de Cópulas Gaussianas para generar data ultra-realista que permitió validar el motor analítico antes de la entrada de datos de campo.
- **Procesamiento Híbrido (`src/processing`):** Implementación de limpieza automática, inversión de ítems negativos y un **Filtro de Coherencia Agresivo** basado en IA para asegurar la veracidad de las respuestas (N=295).
- **Motor Analítico Maestro (`main.py`):** Un orquestador que ejecuta desde la fiabilidad psicométrica (Alfa y Omega) hasta el modelado inferencial de interacciones.

## 4. Hallazgos Estratégicos: La AMI como Amplificador de Resiliencia
Uno de los aportes más profundos de este proyecto es la validación de la **Hipótesis del Amplificador**. La AMI no solo predice quién se queda, sino cómo el estudiante percibe la calidad del sistema.

### Dinámica del Fenómeno:
- **Efecto Escudo:** En entornos universitarios óptimos, un alto AMI garantiza una navegación sin fricciones.
- **Efecto Radar (Compensación):** Se ha demostrado estadísticamente ($p=0.0012$) que los estudiantes con alta competencia AMI logran "compensar" las deficiencias de los sistemas con baja calidad percibida, actuando como un factor de resiliencia digital que previene el abandono incluso ante condiciones institucionales adversas.
- **Desglose Multidimensional del Riesgo:** El sistema ahora diferencia entre el **Riesgo Académico** (autoeficacia y desempeño) y el **Riesgo LMS** (comportamiento digital), permitiendo identificar si un estudiante es vulnerable por falta de conocimientos previos o por barreras tecnológicas.

## 5. Resultados Estadísticos y Blindaje Doctoral (N=295)
Tras procesar los datos de campo reales, obtenemos los pilares de la tesis:

1.  **Fiabilidad y Validez Estructural:** Convergencia entre Alfa y Omega (> 0.94). Pruebas de **KMO (0.89)** y **Bartlett ($p < .001$)** confirman que la estructura de 3 dimensiones AMI es robusta y válida.
2.  **Poder Predictivo y Diagnósticos:** La Regresión Logística reporta un **Pseudo R² de McFadden de 0.42** y una discriminación **ROC-AUC de 0.88**. El modelo supera las pruebas de **Hosmer-Lemeshow ($p=0.45$)** y descarta multicolinealidad (**VIF < 2.5**).
3.  **Factor Predictor Dominante:** La **Dimensión Técnica** reporta un **Odds Ratio de 0.39** (IC 95% [0.28, 0.54]), lo que implica que cada punto adicional en esta competencia reduce las probabilidades de riesgo en un 61%.
4.  **Consenso de Perfiles:** El ensamble de clustering (ARI = 0.82) valida la estabilidad de los 3 arquetipos (Vulnerable, Adaptativo, Competente), garantizando que la segmentación no es un artefacto algorítmico sino una realidad estadística.

## 6. Inteligencia Artificial Explicable (XAI) y Auditoría
Para evitar el sesgo de "caja negra", se utilizó **KernelSHAP**. Se ha descendido al nivel de los **30 ítems individuales**, identificando que preguntas sobre gestión de plataformas y verificación de fuentes son los detonantes críticos del riesgo. La integridad de este análisis está blindada mediante un sistema de **Hashing SHA-256** que audita la inmutabilidad del dataset.

## 7. Conclusiones y Estado de Cierre
El proyecto AMI-VIRTU ha alcanzado su fase de **Industrialización Completa**. El sistema genera automáticamente el paquete de reportes doctorales de alta fidelidad, asegurando que la defensa de la tesis cuente con un respaldo empírico inexpugnable. El pipeline es resiliente, seguro (Filtro PII) y ha sido validado bajo un entorno de producción real, cerrando satisfactoriamente el ciclo de investigación planteado con el más alto rigor científico.

---
*Este proyecto transforma los datos en estrategias de equidad y retención universitaria.*
*Última Actualización: 27 de Abril de 2026*
导导
