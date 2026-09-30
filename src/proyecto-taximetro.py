# ============================================================
# TAXÍMETRO DIGITAL - Proyecto P1
# Calcula el costo de una carrera según el tiempo y el estado
# ============================================================

# Importamos la librería 'time' para poder medir el tiempo transcurrido
import time

# ============================================================
# TARIFAS: Precio por segundo según el estado del taxi
# ============================================================
tarifa_parado = 0.02      # Cuesta 0.02€ cada segundo si el taxi está parado
tarifa_movimiento = 0.05  # Cuesta 0.05€ cada segundo si el taxi se mueve


# ============================================================
# FUNCIÓN BIENVENIDA: Muestra las instrucciones al conductor
# ============================================================
def bienvenida():
    print("=" * 50)
    print("       TAXÍMETRO ")
    print("=" * 50)
    print("\nTarifas:")
    # El :.2f formatea el número para mostrar solo 2 decimales
    print(f"  • Parado:      {tarifa_parado:.2f} €/segundo")
    print(f"  • Movimiento:  {tarifa_movimiento:.2f} €/segundo")
    print("\nComandos:")
    print("  [p] → Taxi parado")
    print("  [m] → Taxi en movimiento")
    print("  [f] → Finalizar carrera")
    print("-" * 50)


# ============================================================
# FUNCIÓN INICIAR: Gestiona una carrera completa
# ============================================================
def iniciar():
    print("\nEmpezamos!!. El taxi está parado.")
    print("   Usa [p] para parar, [m] para moverte, [f] para finalizar.\n")

    # Iniciamos las variables para guardar el estado de la carrera
    total = 0.0              # El dinero acumulado empieza en 0
    estado = "parado"        # El taxi empieza parado
    ultimo_tiempo = time.time()  # Guardamos el momento exacto en que empieza

    # Bucle infinito: el taxi sigue funcionando hasta que el usuario pulsa "f"
    while True:
        # Pedimos un comando al usuario
        # .strip() quita espacios, .lower() convierte a minúsculas
        comando = input(f"[{estado.upper()} | {total:.2f}€] > ").strip().lower()

        # Calculamos cuánto tiempo pasó desde el último comando
        ahora = time.time()              # Hora actual
        segundos = ahora - ultimo_tiempo  # Diferencia = tiempo transcurrido
        ultimo_tiempo = ahora            # Actualizamos el reloj para la próxima vez

        # COBRAMOS el tiempo que pasó según el estado en el que ESTABA el taxi
        if estado == "parado":
            total += segundos * tarifa_parado       # Cobramos tarifa de parado
        else:
            total += segundos * tarifa_movimiento   # Cobramos tarifa de movimiento

        # Procesamos el comando que escribió el usuario
        if comando == "p":
            # Si el taxi ya estaba parado, avisamos
            if estado == "parado":
                print("  ℹ️  El taxi ya está parado.")
            else:
                # Si no, cambiamos el estado a parado
                estado = "parado"
                print("  🛑 Taxi en Stop.")

        elif comando == "m":
            # Si el taxi ya estaba en movimiento, avisamos
            if estado == "movimiento":
                print(" Se mueve :O")
            else:
                # Si no, cambiamos el estado a movimiento
                estado = "movimiento"
                print("  Se esta moviendo :O")

        elif comando == "f":
            # Mostramos el total y terminamos la carrera
            print("\n" + "=" * 50)
            print("     Hemos llegado a su destino")
            print("=" * 50)
            print(f"  TOTAL: {total:.2f} €")
            print("=" * 50 + "\n")
            return total  # Devuelve el total y sale de la función

        else:
            # Si el comando no es p, m ni f, mostramos un error
            print("  ⚠️  Comando no reconocido. Usa p / m / f.")


# ============================================================
# FUNCIÓN MAIN: El menú principal del programa
# ============================================================
def main():
    bienvenida()  # Primero mostramos las instrucciones

    # Bucle infinito para poder hacer varias carreras sin cerrar el programa
    while True:
        entrada = input("\n¿Nueva carrera? [s/n]: ").strip().lower()
        if entrada == "s":
            iniciar()  # Empezamos una nueva carrera
        elif entrada == "n":
            print("\n👋 ¡Hasta la proxima!\n")
            break  # Salimos del bucle y cerramos el programa
        else:
            print("  ⚠️  Responde 's' o 'n'.")


# ============================================================
# PUNTO DE ENTRADA: Esto ejecuta el programa cuando lo inicias
# ============================================================
if __name__ == "__main__":
    main()
