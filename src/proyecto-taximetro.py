import time

tarifa_parado = 0.02
tarifa_movimiento = 0.05


def bienvenida():
    print("=" * 50)
    print("       TAXÍMETRO ")
    print("=" * 50)
    print("\nTarifas:")
    #el 2f trunca a 2 decimales
    print(f"  • Parado:      {tarifa_parado:.2f} €/segundo")
    print(f"  • Movimiento:  {tarifa_movimiento:.2f} €/segundo")
    print("\nComandos:")
    print("  [p] → Taxi parado")
    print("  [m] → Taxi en movimiento")
    print("  [f] → Finalizar carrera")
    print("-" * 50)


def iniciar():
    print("\nEmpezamos!!. El taxi está parado.")
    print("   Usa [p] para parar, [m] para moverte, [f] para finalizar.\n")

    total = 0.0
    estado = "parado"
    ultimo_tiempo = time.time()

    while True:
        comando = input(f"[{estado.upper()} | {total:.2f}€] > ").strip().lower()
        ahora = time.time()
        segundos = ahora - ultimo_tiempo
        ultimo_tiempo = ahora

        # Acumular tarifa del intervalo anterior
        if estado == "parado":
            total += segundos * tarifa_parado
        else:
            total += segundos * tarifa_movimiento

        if comando == "p":
            if estado == "parado":
                print("  ℹ️  El taxi ya está parado.")
            else:
                estado = "parado"
                print("  🛑 Taxi en Stop.")

        elif comando == "m":
            if estado == "movimiento":
                print(" Se mueve :O")
            else:
                estado = "movimiento"
                print("  Se esta moviendo :O")

        elif comando == "f":
            print("\n" + "=" * 50)
            print("     Hemos llegado a su destino")
            print("=" * 50)
            print(f"  TOTAL: {total:.2f} €")
            print("=" * 50 + "\n")
            return total

        else:
            print("  ⚠️  Comando no reconocido. Usa p / m / f.")


def main():
    bienvenida()

    while True:
        entrada = input("\n¿Nueva carrera? [s/n]: ").strip().lower()
        if entrada == "s":
            iniciar()
        elif entrada == "n":
            print("\n👋 ¡Hasta la proxima!\n")
            break
        else:
            print("  ⚠️  Responde 's' o 'n'.")


if __name__ == "__main__":
    main()
    