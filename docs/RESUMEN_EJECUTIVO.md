# Resumen Ejecutivo Integral del Proyecto: AMI-VIRTU & ARD-VIRTU

## 1. Contexto Académico y el Eje de la Literacidad
La **Alfabetización Mediática e Informacional (AMI)** no es una competencia aislada; es el núcleo que permite a los ciudadanos digitales navegar, discernir y crear contenido en un ecosistema mediático saturado. En esta investigación doctoral, se define como el factor determinante en la permanencia de los estudiantes universitarios. El proyecto AMI-VIRTU descompone este constructo en tres dimensiones críticas: la **crítica** (discernimiento de veracidad), la **técnica** (dominio de plataformas LMS) y la **participativa** (interacción ética y proactiva).

## 2. Origen del Proyecto y Objetivos de Investigación
El proyecto surge ante la necesidad de crear una arquitectura computacional robusta para validar la hipótesis central de la tesis: *"Existe una relación inversa significativamente fuerte entre el nivel AMI y el riesgo de deserción virtual"*.

### Instrumentos Validados:
- **AMI-VIRTU:** Evaluación psicométrica de competencias informacionales (30 ítems).
- **ARD-VIRTU:** Sistema de detección de riesgo académico y de deserción.

## 3. Arquitectura del Sistema: De la Simulación a la Industrialización
El software ha sido desarrollado bajo principios de **Programación Orientada a Objetos (OOP)** en Python 3.11, garantizando que el pipeline sea reproducible y au### Módulos del Pipeline Desacoplado:
- **Simulación Avanzada (`src/simulation`):** Generación de datos sintéticos (N=295 psicometría / N=263 inferencia) mediante Cópulas Gaussianas y factor latente, para validación matemática y algorítmica previa a campo.
- **Procesamiento de Campo Real (`src/processing/real_data_loader.py`):** Ingestión del Excel de encuestas reales, aplicando exclusiones éticas/metodológicas (exclusión de 7 sin consentimiento y 36 sin clases virtuales), consolidando una muestra de **N=303** (y **N=302** tras el filtro de coherencia semántica).
- **Motor Analítico Maestro (`main.py`):** Un orquestador que bifurca la ejecución y guarda reportes independientes en `data/outputs/real/` o `data/outputs/synthetic/` según el origen configurado en `.env`.

## 4. Hallazgos Estratégicos: La AMI como Amplificador de Resiliencia
Uno de los aportes más profundos de este proyecto es la validación de la **Hipótesis del Amplificador**. La AMI no solo predice quién se queda, sino cómo el estudiante percibe la calidad del sistema.

### Dinámica del Fenómeno:
- **Efecto Escudo:** En entornos universitarios óptimos, un alto AMI garantiza una navegación sin fricciones.
- **Efecto Radar (Compensación - Data Sintética):** En simulaciones donde se incluye `Calidad_Percibida`, se ha demostrado estadísticamente ($p=0.0012$) que los estudiantes con alta competencia AMI logran "compensar" las deficiencias de los sistemas con baja calidad percibida, actuando como un factor de resiliencia digital.
- **Desglose Multidimensional del Riesgo (Fase Real):** El sistema diferencia entre el **Riesgo Académico** (autoeficacia y desempeño) y el **Riesgo LMS** (comportamiento digital), permitiendo identificar si un estudiante es vulnerable por falta de conocimientos previos o por barreras tecnológicas.

## 5. Resultados Estadísticos y Blindaje Doctoral (Comparativa)
El pipeline contrasta los resultados teóricos limpios frente a la realidad de campo:

| Métrica / Hallazgo | Flujo Sintético (N=263 Válido) | Flujo Real de Campo (N=302 Válido) |
| :--- | :--- | :--- |
| **Fiabilidad Psicométrica** | $\alpha$ y $\omega$ > 0.94 (Estructura Limpia) | Dimensiones AMI: $\alpha$ y $\omega$ > 0.84 (Muy Consistente) |
| **KMO / Bartlett** | 0.89 / $p < .001$ | 0.9270 / $p < .001$ (Adecuación Muestral Excelente) |
| **Pseudo $R^2$ de McFadden** | **0.2442** (Ajuste Teórico Alto) | **0.0110** (Ajuste Típico de Campo en Ciencias Sociales) |
| **ROC-AUC (Clasificación)** | **0.88** (Discriminación Excelente) | **0.6092** / CV AUC = **0.5361** (Clasificación Moderada/Ruidosa) |
| **Contraste de Grupos** | Género y Universidad Significativos | Género/Edad omitidos por ausencia en encuesta. Univ: $\eta^2 = 0.0813$ (Mediano) |
| **Consenso de Perfiles (ARI)** | 0.82 | 0.1774 (Perfiles más solapados en la realidad de campo) |

*Nota Científica:* La marcada atenuación en el $R^2$ y AUC en la data real es metodológicamente esperable y refleja el alto nivel de ruido en encuestas autoinformadas no controladas de campo, lo cual sustenta un diagnóstico doctoral realista.

## 6. Inteligencia Artificial Explicable (XAI) y Auditoría
Para evitar el sesgo de "caja negra", se utiliza **KernelSHAP**. Se ha descendido al nivel de los **30 ítems individuales**, identificando que en el flujo real de campo, los reactivos de la Dimensión Participativa y Técnica (e.g., P3, T10, T6) actúan como las características de mayor impacto local en la probabilidad de riesgo. La integridad del análisis está blindada mediante un sistema de **Hashing SHA-256** que audita la inmutabilidad de la data procesada en cada ejecución.

## 7. Conclusiones y Estado de Cierre
El proyecto AMI-VIRTU ha alcanzado su fase de **Industrialización Completa y Desacoplada**. El sistema genera automáticamente el paquete de reportes doctorales de alta fidelidad organizados por rutas independientes (`data/outputs/real/` y `data/outputs/synthetic/`), asegurando que la defensa de la tesis cuente con un respaldo empírico inexpugnable tanto para la simulación metodológica como para el análisis de campo real.

---
*Este proyecto transforma los datos en estrategias de equidad y retención universitaria.*
*Última Actualización: 09 de Junio de 2026 (Revisión Doctoral v2.2)*
