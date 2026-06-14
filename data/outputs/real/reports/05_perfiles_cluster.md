# Reporte de Segmentación y Perfiles de Estudiantes (Clustering K=3)

## 1. Introducción y Métricas de Validación
El motor de agrupamiento no supervisado ha segmentado a la población estudiantil en **K=3 clústeres** o perfiles en función de sus destrezas de Alfabetización Mediática e Informacional (AMI) y sus scores de riesgo:
- **Silhouette Score:** **0.3872** (indicador de cohesión y separación de los clústeres).
- **BIC Score (GMM):** **1954.4400**.

## 2. Caracterización de los Perfiles (K-Means)

| Perfil / Conglomerado | Tamaño (N) | % Muestra | AMI Crítico | AMI Técnico | AMI Participativo | Prevalencia Riesgo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Grupo 0** | 79 | 30.4% | 4.010 | 4.086 | 4.194 | 38.0% |
| **Grupo 1** | 130 | 50.0% | 3.558 | 3.435 | 3.456 | 33.1% |
| **Grupo 2** | 51 | 19.6% | 2.939 | 2.808 | 2.802 | 43.1% |


### Descripción Metodológica de los Grupos:
- **Grupo 0:** Estudiantes con alta competencia AMI global y niveles bajos o moderados de riesgo. Representan el perfil **Competente / Resiliente**.
- **Grupo 1:** Estudiantes en un rango intermedio o adaptativo de literacidad digital. Representan el perfil **Adaptativo**.
- **Grupo 2:** Estudiantes con puntuaciones AMI críticamente bajas en todas las dimensiones y una prevalencia de riesgo sustancialmente elevada. Representan el perfil **Vulnerable**.

---
*Metodología: Ensamble multialgoritmo (K-Means, Ward, GMM, DBSCAN) sobre dataset activo.*
