import hashlib
import pandas as pd
import os

def calculate_data_hash(file_path: str) -> str:
    """Calcula el hash SHA-256 de un archivo para asegurar la integridad de los datos."""
    if not os.path.exists(file_path):
        return "FILE_NOT_FOUND"
    
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        # Leer en bloques para eficiencia
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def verify_reproducibility_env():
    """Verifica variables de entorno críticas para la replicación del estudio."""
    import sys
    import platform
    import sklearn
    import statsmodels
    
    env_info = {
        "Python_Version": sys.version.split()[0],
        "OS": platform.system() + " " + platform.release(),
        "Scikit-Learn": sklearn.__version__,
        "Statsmodels": statsmodels.__version__
    }
    return env_info
