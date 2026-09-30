"""
Módulo de configuración del sistema de logging.
Registra todos los eventos del taxímetro en un archivo de log.
"""

import logging
import os
from datetime import datetime


def configurar_log():
    """
    Configura el sistema de logging para registrar todos los eventos.
    Crea un archivo de log con fecha y hora para cada sesión.
    """
    # Crear carpeta de logs si no existe
    if not os.path.exists("logs"):
        os.makedirs("logs")

    # Nombre del archivo de log con fecha
    fecha = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_log = f"logs/taximetro_{fecha}.log"

    # Configurar el logger
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.FileHandler(archivo_log, encoding="utf-8"),
            logging.StreamHandler()  # También mostrar en consola
        ]
    )

    logging.info("=" * 60)
    logging.info("TAXÍMETRO DIGITAL - INICIO DE SESIÓN")
    logging.info("=" * 60)

    return logging.getLogger(__name__)
