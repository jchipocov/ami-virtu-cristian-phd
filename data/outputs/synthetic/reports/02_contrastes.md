# Reporte de Contrastes de Hipótesis y Brechas de Literacidad

## 1. Introducción y Objetivo Académico
Este componente del análisis busca identificar la existencia de diferencias estadísticamente significativas en los niveles de Literacidad Mediática e Informacional (AMI) en función de variables de control sociodemográficas. El objetivo es determinar si el riesgo de deserción virtual está sesgado por factores externos como el género o la procedencia institucional.

## 2. Resultados de las Pruebas de Contraste (con Tamaños de Efecto) [HC-03]

Se utilizó el **T-test de Welch** (sin asumir igualdad de varianzas) para comparaciones binarias y **ANOVA de una vía** para comparaciones múltiples, reportando los tamaños de efecto requeridos por APA 7ª edición.

| Variable | Estadístico | p-valor | **Efecto** | **Magnitud** | Interpretación H₀ |
| :--- | :---: | :---: | :---: | :---: | :--- |
| **Sexo** (T-Welch) | 0.59 | 0.5536 | d = ~0.07 | Trivial | **No se rechaza H₀** |
| **Institución** (ANOVA) | 0.93 | 0.3968 | η² = ~0.006 | Trivial | **No se rechaza H₀** |
| **Semestre** (ANOVA) | 1.15 | 0.3204 | η² = ~0.008 | Trivial | **No se rechaza H₀** |

> [!NOTE]
> Los tamaños de efecto exactos son calculados automáticamente en cada ejecución del pipeline por `run_demographic_contrasts()` con `d de Cohen` (T-test) y `η²` + `η² parcial` (ANOVA). Los valores de la tabla son representativos del primer análisis. Consultar la bitácora de ejecución para los valores precisos de cada corrida.

### Interpretación de Magnitud (Cohen, 1988 / Cohen, 1992)
- **d de Cohen:** Trivial < 0.20 · Pequeño 0.20–0.49 · Mediano 0.50–0.79 · Grande ≥ 0.80
- **η² (eta cuadrado):** Trivial < 0.01 · Pequeño 0.01–0.05 · Mediano 0.06–0.13 · Grande ≥ 0.14

## 3. Interpretación Doctoral: "La tesis de la Equidad Digital"
Desde una perspectiva pedagógica, la ausencia de significancia estadística ($p > .05$) en estas variables es un hallazgo de alto valor:

1. **Equidad en Competencias:** Los resultados sugieren que no existen brechas de género ni institucionales pronunciadas en el dominio técnico y crítico de los medios dentro de la muestra (N=295).
2. **Estrategia Unificada:** Este "empate técnico" valida la implementación de un modelo de intervención AMI de carácter **transversal**. No es necesario diseñar programas segregados por género o facultad, ya que los perfiles de riesgo no dependen de estas etiquetas demográficas clásicas.
3. **Efecto trivial confirmado:** Los tamaños de efecto triviales (d < 0.20, η² < 0.01) refuerzan que las diferencias observadas carecen de relevancia práctica, más allá del nivel estadístico. Esto es un argumento empírico robusto ante el jurado doctoral.

> [!TIP]
> La homogeneidad del grupo refuerza la idea de que la analítica de aprendizaje debe basarse en el **comportamiento digital y académico** más que en los datos sociodemográficos tradicionales.

---
*Fecha de Generación: 27 de Abril de 2026 | Actualizado: 09 de Junio de 2026 (Revisión HC-03)*  
*Metodología: T-test de Welch + ANOVA con d de Cohen y η² (APA 7ª ed.)*
