"""
Módulo de configuración externa.
Carga las tarifas desde un archivo JSON sin necesidad de tocar el código.
"""

import json
import os


ARCHIVO_CONFIG = "config.json"


def cargar_configuracion():
    """
    Carga la configuración desde el archivo config.json.
    Si no existe, usa valores por defecto.
    """
    config_por_defecto = {
        "tarifa_parado": 0.02,
        "tarifa_movimiento": 0.05,
        "moneda": "€",
        "decimales": 2
    }

    if os.path.exists(ARCHIVO_CONFIG):
        try:
            with open(ARCHIVO_CONFIG, "r", encoding="utf-8") as f:
                config = json.load(f)
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Error leyendo config.json: {e}")
            print("   Usando valores por defecto.\n")
            return config_por_defecto
    else:
        print(f"⚠️  No se encontró {ARCHIVO_CONFIG}")
        print("   Usando valores por defecto.\n")
        return config_por_defecto
