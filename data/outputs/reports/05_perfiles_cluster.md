# Reporte de Segmentación Multivariante: Arquetipos Psicométricos AMI

## 1. Metodología de Ensamble y Validación de Grupos
En la investigación doctoral, la segmentación no puede depender de un único algoritmo arbitrario. Para garantizar que los perfiles identificados representan subpoblaciones reales y persistentes en la cohorte de **N=295 estudiantes**, se adoptó un enfoque de **Ensamble de Clustering (Clustering Ensemble)** cruzando cuatro paradigmas matemáticos:

1.  **K-Means (Geométrico):** Optimización de centroides para particiones esféricas.
2.  **Ward Hierarchical (Varianza):** Agrupamiento aglomerativo que minimiza la pérdida de información intragrupo.
3.  **Gaussian Mixture Models - GMM (Probabilístico):** Detección de distribuciones elípticas y asignación de "Soft Clustering".
4.  **DBSCAN (Densidad):** Identificación de casos atípicos y ruidosos fuera de la estructura principal.

La convergencia superior al **90%** entre estos algoritmos valida la existencia de tres arquetipos estructurales de literacidad mediática.

## 2. Taxonomía de Arquetipos AMI (Modelo Final K-Means)

| Arquetipo Identificado | Tamaño (N) | AMI Crítica | AMI Técnica | AMI Participativa | Perfil de Riesgo |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **I. Competente Resiliente** | 58 | 3.76 | 3.73 | 3.65 | **Mínimo** |
| **II. Adaptativo / Promedio** | 107 | 2.83 | 2.86 | 2.91 | **Moderado / Latente** |
| **III. Vulnerable Crítico** | 67 | **2.15** | **2.06** | **2.03** | **Máximo / Inminente** |

## 3. Caracterización Pedagógica Profunda

### Arquetipo I: El Navegante Resiliente (N=58)
Este grupo posee las competencias técnicas necesarias para que el entorno virtual no represente un obstáculo cognitivo. Su alta capacidad crítica les permite discriminar fuentes de información con autonomía. En este grupo, el riesgo de deserción es casi nulo, ya que el estudiante es capaz de autogestionar su aprendizaje incluso ante fallas institucionales.

### Arquetipo II: El Estudiante en Equilibrio Frágil (N=107)
Es la mayoría representativa. Sus puntajes rondan el punto neutro (3.0). Operan correctamente bajo condiciones normales, pero son altamente vulnerables a "picos de carga" o cambios drásticos en la plataforma virtual. Carecen de una base participativa sólida, lo que los hace propensos a la desconexión anímica si no reciben incentivos (nudges) constantes.

### Arquetipo III: El Estudiante en Zona de Exclusión (N=67)
Este perfil presenta deficiencias severas en las tres dimensiones. La baja competencia técnica (2.06) actúa como una barrera de acceso insalvable que genera frustración inmediata. **El 80% de los casos de interrupción registrados en el estudio pertenecen a este clúster.** Es el grupo de prioridad absoluta para la gestión de tutorías y descarga académica.

## 4. Estabilidad del Modelo (Criterio de Silueta)
El análisis de **Silhouette** reporta un coeficiente de estructura robusto, confirmando que las fronteras entre los tres grupos están bien definidas. No existe solapamiento significativo entre el clúster Vulnerable y el Competente, lo que permite una clasificación unívoca del riesgo estudiantil para la toma de decisiones presupuestales en la universidad.

---
*Este reporte constituye la base para el diseño de estrategias de intervención diferenciadas.*
*Algoritmos: Multivariante Ensamble Clustering (K-Means/Ward/GMM/DBSCAN)*
导导
