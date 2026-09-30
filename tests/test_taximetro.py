"""
Pruebas automatizadas del Taxímetro Digital.
Verifica que las tarifas, el cálculo del total y la persistencia funcionen correctamente.
"""

import sys
import os
import json
import tempfile

# Añadir la carpeta src al path para poder importar
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from config import cargar_configuracion
from persistencia import cargar_historial, guardar_carrera


def test_cargar_configuracion():
    """Verifica que la configuración se carga correctamente desde config.json."""
    config = cargar_configuracion()

    # Verificar que tiene las claves necesarias
    assert "tarifa_parado" in config, "Falta tarifa_parado en config"
    assert "tarifa_movimiento" in config, "Falta tarifa_movimiento en config"
    assert "moneda" in config, "Falta moneda en config"

    # Verificar que los valores son correctos
    assert config["tarifa_parado"] == 0.02, "tarifa_parado debe ser 0.02"
    assert config["tarifa_movimiento"] == 0.05, "tarifa_movimiento debe ser 0.05"

    print("✅ Test de configuración: OK")


def test_calculo_tarifa_parado():
    """Verifica el cálculo de tarifa cuando el taxi está parado."""
    config = cargar_configuracion()
    segundos = 10
    total = segundos * config["tarifa_parado"]
    assert total == 0.20, f"10 segundos parado deben costar 0.20€, no {total}"
    print("✅ Test de cálculo parado: OK")


def test_calculo_tarifa_movimiento():
    """Verifica el cálculo de tarifa cuando el taxi se mueve."""
    config = cargar_configuracion()
    segundos = 10
    total = segundos * config["tarifa_movimiento"]
    assert total == 0.50, f"10 segundos en movimiento deben costar 0.50€, no {total}"
    print("✅ Test de cálculo movimiento: OK")


def test_calculo_mixto():
    """Verifica el cálculo con diferentes estados."""
    config = cargar_configuracion()
    # 5 segundos parado + 5 segundos en movimiento
    total = (5 * config["tarifa_parado"]) + (5 * config["tarifa_movimiento"])
    assert total == 0.35, f"El total debe ser 0.35€, no {total}"
    print("✅ Test de cálculo mixto: OK")


def test_guardar_carrera():
    """Verifica que las carreras se guardan correctamente."""
    # Usar un archivo temporal para no ensuciar el historial real
    import persistencia
    archivo_original = persistencia.ARCHIVO_HISTORIAL

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        archivo_temp = f.name

    try:
        persistencia.ARCHIVO_HISTORIAL = archivo_temp

        # Guardar una carrera de prueba
        guardar_carrera(120.5, 3.50, "movimiento")

        # Verificar que se guardó
        historial = cargar_historial()
        assert len(historial) == 1, "Debe haber 1 carrera en el historial"
        assert historial[0]["duracion_segundos"] == 120.5
        assert historial[0]["importe"] == 3.50
        assert historial[0]["estado_final"] == "movimiento"
        assert "fecha" in historial[0], "Debe tener fecha"

        print("✅ Test de guardar carrera: OK")

    finally:
        persistencia.ARCHIVO_HISTORIAL = archivo_original
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)


def test_historial_vacio():
    """Verifica que un historial vacío se maneja correctamente."""
    import persistencia
    archivo_original = persistencia.ARCHIVO_HISTORIAL

    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        archivo_temp = f.name

    try:
        persistencia.ARCHIVO_HISTORIAL = archivo_temp

        # Archivo vacío
        with open(archivo_temp, 'w') as f:
            json.dump([], f)

        historial = cargar_historial()
        assert historial == [], "El historial debe estar vacío"

        print("✅ Test de historial vacío: OK")

    finally:
        persistencia.ARCHIVO_HISTORIAL = archivo_original
        if os.path.exists(archivo_temp):
            os.remove(archivo_temp)


if __name__ == "__main__":
    print("=" * 50)
    print("   EJECUTANDO PRUEBAS DEL TAXÍMETRO v2.0")
    print("=" * 50)

    test_cargar_configuracion()
    test_calculo_tarifa_parado()
    test_calculo_tarifa_movimiento()
    test_calculo_mixto()
    test_guardar_carrera()
    test_historial_vacio()

    print("=" * 50)
    print("   TODAS LAS PRUEBAS PASARON ✅")
    print("=" * 50)
