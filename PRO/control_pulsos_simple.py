import serial
import time
import sys

def main():
    try:
        arduino = serial.Serial('COM5', 9600, timeout=1)
        time.sleep(2)

        print("Control de pulsos Arduino")
        print("Escribe 1, 2, 3 o 4 y presiona Enter para enviar pulsos:")
        print("1 -> Pin 3")
        print("2 -> Pin 5")
        print("3 -> Pin 6")
        print("4 -> Pin 9")
        print("q -> Salir")
        print("-" * 50)

        while True:
            command = input("Comando: ").strip()

            if command in ['1', '2', '3', '4']:
                arduino.write(command.encode())
                pin_map = {'1': 3, '2': 5, '3': 6, '4': 9}
                print(f"Pulso enviado - Comando {command} (Pin {pin_map[command]})")

            elif command.lower() == 'q':
                print("Saliendo...")
                break

            else:
                print("Comando no válido. Usa 1, 2, 3, 4 o q")

            if arduino.in_waiting:
                response = arduino.readline().decode().strip()
                if response:
                    print(f"Arduino: {response}")

    except serial.SerialException as e:
        print(f"Error de conexión serial: {e}")
        print("Asegúrate de que el Arduino esté conectado y el puerto COM sea correcto")

    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario")

    except Exception as e:
        print(f"Error inesperado: {e}")

    finally:
        if 'arduino' in locals():
            arduino.close()
            print("Conexión serial cerrada")

if __name__ == "__main__":
    main()