# ============================================================
# TAXÍMETRO DIGITAL - Proyecto P1 (Fase 2)
# Con logging, persistencia y configuración externa
# ============================================================

import time
import logging

# Importar módulos del proyecto
from config import cargar_configuracion
from logger_config import configurar_log
from persistencia import guardar_carrera, mostrar_historial


# ============================================================
# CARGAR CONFIGURACIÓN EXTERNA
# ============================================================
config = cargar_configuracion()
tarifa_parado = config["tarifa_parado"]
tarifa_movimiento = config["tarifa_movimiento"]
MONEDA = config["moneda"]
DECIMALES = config["decimales"]

# Configurar el logger
logger = configurar_log()


# ============================================================
# FUNCIÓN BIENVENIDA: Muestra las instrucciones al conductor
# ============================================================
def bienvenida():
    print("=" * 50)
    print("       TAXÍMETRO DIGITAL v2.0")
    print("=" * 50)
    print("\nTarifas (cargadas desde config.json):")
    print(f"  • Parado:      {tarifa_parado:.{DECIMALES}f} {MONEDA}/segundo")
    print(f"  • Movimiento:  {tarifa_movimiento:.{DECIMALES}f} {MONEDA}/segundo")
    print("\nComandos:")
    print("  [p] → Taxi parado")
    print("  [m] → Taxi en movimiento")
    print("  [f] → Finalizar carrera")
    print("-" * 50)


# ============================================================
# FUNCIÓN INICIAR: Gestiona una carrera completa
# ============================================================
def iniciar():
    logger.info("Nueva carrera iniciada")
    print("\n✅ Carrera iniciada. El taxi está parado.")
    print("   Usa [p] para parar, [m] para moverte, [f] para finalizar.\n")

    # Iniciamos las variables para guardar el estado de la carrera
    total = 0.0
    estado = "parado"
    ultimo_tiempo = time.time()
    inicio_carrera = ultimo_tiempo

    # Bucle infinito: el taxi sigue funcionando hasta que el usuario pulsa "f"
    while True:
        try:
            # Pedimos un comando al usuario
            comando = input(f"[{estado.upper()} | {total:.{DECIMALES}f}{MONEDA}] > ").strip().lower()

            # Calculamos cuánto tiempo pasó desde el último comando
            ahora = time.time()
            segundos = ahora - ultimo_tiempo
            ultimo_tiempo = ahora

            # COBRAMOS el tiempo que pasó según el estado en el que ESTABA el taxi
            if estado == "parado":
                total += segundos * tarifa_parado
            else:
                total += segundos * tarifa_movimiento

            # Procesamos el comando que escribió el usuario
            if comando == "p":
                if estado == "parado":
                    print("  ℹ️  El taxi ya está parado.")
                    logger.info("Intento de parar cuando ya estaba parado")
                else:
                    estado = "parado"
                    print("  🛑 Taxi parado.")
                    logger.info("Estado cambiado a: PARADO")

            elif comando == "m":
                if estado == "movimiento":
                    print("  ℹ️  El taxi ya está en movimiento.")
                    logger.info("Intento de mover cuando ya estaba en movimiento")
                else:
                    estado = "movimiento"
                    print("  🚗 Taxi en movimiento.")
                    logger.info("Estado cambiado a: MOVIMIENTO")

            elif comando == "f":
                # Calcular duración total de la carrera
                duracion = ahora - inicio_carrera

                # Mostramos el total
                print("\n" + "=" * 50)
                print("      🏁  CARRERA FINALIZADA")
                print("=" * 50)
                print(f"  Duración: {duracion:.1f} segundos")
                print(f"  TOTAL: {total:.{DECIMALES}f} {MONEDA}")
                print("=" * 50 + "\n")

                # Guardar en el historial
                guardar_carrera(duracion, total, estado)
                logger.info(f"Carrera finalizada - Duración: {duracion:.1f}s, Total: {total:.2f}€")

                return total

            else:
                print("  ⚠️  Comando no reconocido. Usa p / m / f.")
                logger.warning(f"Comando no reconocido: {comando}")

        except KeyboardInterrupt:
            logger.warning("Programa interrumpido por el usuario (Ctrl+C)")
            print("\n\n⚠️  Programa interrumpido. Cerrando...")
            break
        except Exception as e:
            logger.error(f"Error inesperado: {e}")
            print(f"  ❌ Error: {e}")


# ============================================================
# FUNCIÓN MAIN: El menú principal del programa
# ============================================================
def main():
    logger.info("Sistema iniciado correctamente")
    bienvenida()

    # Bucle infinito para poder hacer varias carreras sin cerrar el programa
    while True:
        try:
            # Menú principal
            print("\n" + "-" * 50)
            print("  ¿Qué quieres hacer?")
            print("  [s] → Iniciar nueva carrera")
            print("  [h] → Ver historial de carreras")
            print("  [n] → Salir del programa")
            print("-" * 50)

            entrada = input("  Opción: ").strip().lower()

            if entrada == "s":
                iniciar()
            elif entrada == "h":
                mostrar_historial()
            elif entrada == "n":
                logger.info("Sistema cerrado por el usuario")
                print("\n👋 ¡Hasta la próxima!\n")
                break
            else:
                print("  ⚠️  Opción no válida. Usa s / h / n.")
                logger.warning(f"Entrada no válida en menú: {entrada}")
        except KeyboardInterrupt:
            logger.warning("Programa interrumpido por el usuario (Ctrl+C)")
            print("\n\n👋 ¡Hasta la próxima!\n")
            break


# ============================================================
# PUNTO DE ENTRADA: Esto ejecuta el programa cuando lo inicias
# ============================================================
if __name__ == "__main__":
    main()
