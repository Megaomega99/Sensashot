import serial
import time
import sys
import os
import random
import threading
import csv
import atexit
from datetime import datetime
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import messagebox

images_shown = []

def save_images_log():
    if images_shown:
        try:
            with open('imagenes_mostradas.csv', 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'Nombre_Imagen', 'Pin_Activado'])
                for entry in images_shown:
                    writer.writerow(entry)
            print(f"\nRegistro guardado: {len(images_shown)} imágenes en 'imagenes_mostradas.csv'")
        except Exception as e:
            print(f"Error al guardar el registro: {e}")

atexit.register(save_images_log)

def show_random_image(pin_number):
    imagenes_dir = "imagenes"

    if not os.path.exists(imagenes_dir):
        print("Carpeta 'imagenes' no encontrada")
        return

    image_files = [f for f in os.listdir(imagenes_dir)
                  if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

    if not image_files:
        print("No se encontraron imágenes en la carpeta 'imagenes'")
        return

    random_image = random.choice(image_files)
    image_path = os.path.join(imagenes_dir, random_image)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    images_shown.append([timestamp, random_image, pin_number])

    def display_image():
        root = tk.Tk()
        root.attributes('-fullscreen', True)
        root.configure(bg='black')
        root.attributes('-topmost', True)

        try:
            image = Image.open(image_path)
            screen_width = root.winfo_screenwidth()
            screen_height = root.winfo_screenheight()

            image_ratio = image.width / image.height
            screen_ratio = screen_width / screen_height

            if image_ratio > screen_ratio:
                new_width = screen_width
                new_height = int(screen_width / image_ratio)
            else:
                new_height = screen_height
                new_width = int(screen_height * image_ratio)

            image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)

            label = tk.Label(root, image=photo, bg='black')
            label.pack(expand=True)

            def close_window():
                root.destroy()

            root.after(10000, close_window)
            root.bind('<Escape>', lambda e: root.destroy())

            root.mainloop()

        except Exception as e:
            print(f"Error al mostrar imagen: {e}")
            root.destroy()

    threading.Thread(target=display_image, daemon=True).start()
    print(f"Mostrando imagen: {random_image}")

def main():
    try:
        arduino = serial.Serial('COM5', 9600, timeout=1)
        time.sleep(2)

        print("Control de pulsos Arduino con visualización de imágenes")
        print("Escribe 1, 2, 3 o 4 y presiona Enter para enviar pulsos:")
        print("1 -> Pin 3")
        print("2 -> Pin 5")
        print("3 -> Pin 6")
        print("4 -> Pin 9")
        print("q -> Salir")
        print("-" * 50)
        print("NOTA: Coloca imágenes en la carpeta 'imagenes' para visualización")
        print("-" * 50)

        while True:
            command = input("Comando: ").strip()

            if command in ['1', '2', '3', '4']:
                arduino.write(command.encode())
                pin_map = {'1': 3, '2': 5, '3': 6, '4': 9}
                print(f"Pulso enviado - Comando {command} (Pin {pin_map[command]})")

                show_random_image(pin_map[command])

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