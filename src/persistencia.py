"""
Módulo de persistencia de datos.
Guarda el historial de carreras en un archivo JSON.
"""

import json
import os
from datetime import datetime


ARCHIVO_HISTORIAL = "historial_carreras.json"


def cargar_historial():
    """
    Carga el historial de carreras desde el archivo JSON.
    Si no existe, devuelve una lista vacía.
    """
    if os.path.exists(ARCHIVO_HISTORIAL):
        try:
            with open(ARCHIVO_HISTORIAL, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def guardar_carrera(duracion_segundos, importe, estado_final):
    """
    Guarda los datos de una carrera en el historial.
    Se añade al final del archivo (forma incremental).
    """
    historial = cargar_historial()

    carrera = {
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "duracion_segundos": round(duracion_segundos, 2),
        "importe": round(importe, 2),
        "estado_final": estado_final
    }

    historial.append(carrera)

    with open(ARCHIVO_HISTORIAL, "w", encoding="utf-8") as f:
        json.dump(historial, f, indent=2, ensure_ascii=False)

    return carrera


def mostrar_historial():
    """Muestra todas las carreras guardadas."""
    historial = cargar_historial()

    if not historial:
        print("\n📭 No hay carreras guardadas todavía.\n")
        return

    print("\n" + "=" * 60)
    print("         📊 HISTORIAL DE CARRERAS")
    print("=" * 60)

    for i, carrera in enumerate(historial, 1):
        print(f"\n  Carrera #{i}")
        print(f"    Fecha:     {carrera['fecha']}")
        print(f"    Duración:  {carrera['duracion_segundos']} segundos")
        print(f"    Importe:   {carrera['importe']:.2f} €")
        print(f"    Estado:    {carrera['estado_final']}")

    print("\n" + "=" * 60)
    print(f"  Total carreras: {len(historial)}")
    print("=" * 60 + "\n")
