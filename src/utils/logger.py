import os
import json
from datetime import datetime

class ExecutionLogger:
    """
    Clase para gestionar la bitácora de ejecuciones del pipeline.
    Asegura la trazabilidad de cada análisis realizado en formatos MD y JSONL.
    """
    def __init__(self, log_path: str):
        self.log_path = log_path
        self.jsonl_path = log_path.replace(".log", ".jsonl")
        
    def log_run(self, env: str, num_records: int, accuracy: float, details: str = ""):
        """Registra una entrada en el archivo de bitácora markdown."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        if not os.path.exists(self.log_path):
            with open(self.log_path, "w", encoding="utf-8") as f:
                f.write("# Bitácora de Ejecución Científica - AMI-VIRTU\n\n")

        with open(self.log_path, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"EJECUCIÓN: {timestamp}\n")
            f.write(f"Entorno: {env} | Registros: {num_records} | Accuracy: {accuracy:.2f}\n")
            f.write(f"{'-'*60}\n")
            if details:
                f.write("RESULTADOS DETALLADOS:\n")
                f.write(details)
                f.write("\n")
            f.write(f"{'='*60}\n")
        
        print(f"-> Detalles registrados en bitácora: {self.log_path}")

    def log_run_jsonl(self, payload: dict):
        """Registra la ejecución en formato JSONL para análisis programático."""
        payload['timestamp'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        with open(self.jsonl_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(payload, ensure_ascii=False) + "\n")
            
        print(f"-> Registro estructurado guardado en: {self.jsonl_path}")
