# AMI-VIRTU: Ecosistema Analitico para la Retencion Universitaria 🎓🚀

Bienvenido al repositorio oficial del proyecto **AMI-VIRTU** (Analítica de Literacidad Mediática e Informacional para la Retención Virtual). Este sistema ha sido desarrollado como el motor analítico de una investigación doctoral enfocada en predecir y prevenir la deserción en la educación superior virtual mediante métodos mixtos.

Este documento sirve como **Guía Maestra para el Destinatario**. Si has recibido este proyecto zipeado, aquí encontrarás todo lo necesario para hacerlo funcionar, entender sus tripas y visualizar sus resultados.

---

## � 1. Estructura del Proyecto (Mapa de Archivos)

Para que sepas dónde estás parado, aquí tienes la anatomía del sistema:

```text
learning_analytics_ami/
├── data/
│   ├── raw/                # Datos brutos (CSV) recolectados de campo.
│   ├── processed/          # Dataset consolidado e híbrido (Cuali + Cuanti).
│   └── outputs/            # ¡AQUÍ ESTÁN LOS RESULTADOS!
│       ├── academic_tables/# Tablas con scores listos para la tesis (N=295).
│       ├── reports/        # Los 7 Reportes Doctorales en formato Markdown (.md).
│       └── [Gráficos PNG]  # Heatmaps, SHAP, Clusters y Radar Charts.
├── docs/                   # Artículos de fundamentación metodológica (Vademécum, XAI).
├── src/                    # Código fuente en Python (Lógica del negocio).
│   ├── analysis/           # Regresión, Clustering, XAI y Triangulación.
│   ├── processing/         # Limpieza, Inversión de ítems y Scorer.
│   ├── simulation/         # Motor de generación de datos sintéticos.
│   └── utils/              # Motor de reportes y utilidades.
├── scripts/
│   └── run_simulation.py   # Script independiente para generar/regenerar datos.
├── main.py                 # ORQUESTRADOR PRINCIPAL (Ejecutar este archivo).
├── requirements.txt        # Librerías necesarias.
└── README.md               # Este manual.
```

---

## 🛠️ 2. Configuración del Entorno (Paso a Paso)

Este proyecto requiere **Python 3.11** o superior. Sigue estos pasos para prepararlo:

### 2.1. Crear el Entorno Virtual (Venv)
Es vital para no ensuciar tu instalación global de Python:
```bash
# En Windows (PowerShell):
python -m venv venv
.\venv\Scripts\activate

# En Linux o MacOS:
python3 -m venv venv
source venv/bin/activate
```

### 2.2. Instalar el Ecosistema Científico
Instala todas las dependencias necesarias (`pandas`, `scipy`, `statsmodels`, `shap`, `google-generativeai`, etc.):
```bash
pip install -r requirements.txt
```

### 2.3. Configuración de API (Opcional - Síntesis Narrativa)
El sistema utiliza **Gemini Pro/Flash** para la síntesis narrativa final. Si deseas que los reportes incluyan conclusiones agénticas redactadas por la IA:
1. Crea un archivo `.env` en la raíz (o usa variables de entorno).
2. Añade tu API Key: `GOOGLE_API_KEY=tu_clave_aqui`.
*Si no tienes una clave, el sistema entrará en **"Modo Resiliente"**: realizará todo el análisis estadístico y extraerá las evidencias textuales crudas de los alumnos sin fallar.*

---

## 🚀 3. Manual de Operación

### Escenario A: Generar Nuevos Datos
Si quieres ver cómo el simulador crea a los 295 estudiantes ficticios con sus respuestas de "Section B":
```bash
python scripts/run_simulation.py
```

### Escenario B: Ejecutar el Análisis Doctoral (Recomendado)
Este comando procesa el dataset híbrido existente, calcula la fiabilidad, lanza la regresión, identifica los clústeres y genera los 7 reportes finales:
```bash
python main.py
```

---

## 📊 4. ¿Qué obtendrás tras la ejecución?

Al terminar, debes dirigirte a `data/outputs/reports/`. Allí encontrarás los 7 pilares de la investigación:

1.  **01_fiabilidad.md:** Validación de la consistencia interna (Alfa y Omega).
2.  **02_contrastes.md:** Evidencia de que el AMI es independiente del género/universidad.
3.  **03_modelo_inferencial.md:** El núcleo predictivo. ¿Cuánto margen de deserción reduce el AMI?
4.  **04_explicabilidad_xai.md:** ¿Qué preguntas exactas del test son las más importantes? (vía SHAP).
5.  **05_perfiles_cluster.md:** Taxonomía de los 3 tipos de alumnos (Vulnerable, Adaptativo, Competente).
6.  **06_sintesis_ejecutiva.md:** Resumen de conclusiones listo para copiar a la tesis.
7.  **07_triangulacion_mixta.md:** El cruce entre el dato numérico y "la voz del estudiante".

---

## 🧠 5. Consideraciones Técnicas para el Tercero

- **Hardening de Datos:** El sistema anonimiza automáticamente cualquier dato personal (PII Filter).
- **Inversión de Ítems:** No te preocupes por las preguntas negativas (C6, T6, P5), el código las invierte automáticamente (`6 - valor`) antes de cualquier cálculo.
- **Riesgo:** El riesgo total se calcula mediante una combinación de rendimiento, interrupción previa e inactividad en el aula virtual.

---
*Este proyecto es parte de la Tesis Doctoral AMI-VIRTU 2026. Ha sido diseñado para ser auditable, escalable y metodológicamente inexpugnable.*
导导
