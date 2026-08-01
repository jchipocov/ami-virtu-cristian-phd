# Reporte de Segmentación y Perfiles de Estudiantes (Clustering K=3)

## 1. Introducción y Métricas de Validación
El motor de agrupamiento no supervisado ha segmentado a la población estudiantil en **K=3 clústeres** o perfiles en función de sus destrezas de Alfabetización Mediática e Informacional (AMI) y sus scores de riesgo:
- **Silhouette Score:** **0.3872** (indicador de cohesión y separación de los clústeres).
- **BIC Score (GMM):** **1954.4400**.

## 2. Caracterización de los Perfiles (K-Means)

| Perfil / Conglomerado | Tamaño (N) | % Muestra | AMI Crítico | AMI Técnico | AMI Participativo | Prevalencia Riesgo |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Grupo 0** | 198 | 28.2% | 4.181 | 3.976 | 4.151 | 24.7% |
| **Grupo 1** | 186 | 26.5% | 3.129 | 2.906 | 2.849 | 47.8% |
| **Grupo 2** | 318 | 45.3% | 3.668 | 3.475 | 3.469 | 28.0% |


### Descripción Metodológica de los Grupos:
- **Grupo 0:** Estudiantes con alta competencia AMI global y niveles bajos o moderados de riesgo. Representan el perfil **Competente / Resiliente**.
- **Grupo 1:** Estudiantes en un rango intermedio o adaptativo de literacidad digital. Representan el perfil **Adaptativo**.
- **Grupo 2:** Estudiantes con puntuaciones AMI críticamente bajas en todas las dimensiones y una prevalencia de riesgo sustancialmente elevada. Representan el perfil **Vulnerable**.

---
*Metodología: Ensamble multialgoritmo (K-Means, Ward, GMM, DBSCAN) sobre dataset activo.*
