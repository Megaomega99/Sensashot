import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import serial
import time
import os
import random
import threading
import csv
import atexit
from datetime import datetime
from PIL import Image, ImageTk

class ArduinoPulsosGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Control de Pulsos Arduino - Interfaz Cliente")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Variables
        self.arduino = None
        self.connected = False
        self.images_shown = []
        self.com_port = tk.StringVar(value="COM5")
        self.show_images = tk.BooleanVar(value=True)
        self.available_images = []
        self.used_images = []

        # Configurar cierre del programa
        atexit.register(self.save_images_log)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_ui()

    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="Control de Pulsos Arduino",
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)

        # Frame de configuración
        config_frame = tk.LabelFrame(self.root, text="Configuración",
                                   font=('Arial', 12, 'bold'), padx=20, pady=10)
        config_frame.pack(fill='x', padx=20, pady=10)

        # Puerto COM
        com_frame = tk.Frame(config_frame)
        com_frame.pack(fill='x', pady=5)

        tk.Label(com_frame, text="Puerto COM:", font=('Arial', 10)).pack(side='left')
        com_entry = tk.Entry(com_frame, textvariable=self.com_port, font=('Arial', 10), width=10)
        com_entry.pack(side='left', padx=(10, 20))

        # Botón de conexión
        self.connect_btn = tk.Button(com_frame, text="Conectar", command=self.toggle_connection,
                                   font=('Arial', 10, 'bold'), bg='#27ae60', fg='white',
                                   padx=20, cursor='hand2')
        self.connect_btn.pack(side='left')

        # Estado de conexión
        self.status_label = tk.Label(com_frame, text="Desconectado",
                                   font=('Arial', 10, 'bold'), fg='red')
        self.status_label.pack(side='left', padx=(20, 0))

        # Checkbox para mostrar imágenes
        img_check = tk.Checkbutton(config_frame, text="Mostrar imágenes aleatorias",
                                 variable=self.show_images, font=('Arial', 10))
        img_check.pack(anchor='w', pady=5)

        # Frame de controles principales
        control_frame = tk.LabelFrame(self.root, text="Controles de Pulsos",
                                    font=('Arial', 14, 'bold'), padx=20, pady=20)
        control_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Grid de botones
        buttons_frame = tk.Frame(control_frame)
        buttons_frame.pack(expand=True)

        # Configuración de botones
        button_configs = [
            {"text": "PIN 3", "command": lambda: self.send_pulse('1', 3), "color": "#e74c3c"},
            {"text": "PIN 5", "command": lambda: self.send_pulse('2', 5), "color": "#3498db"},
            {"text": "PIN 6", "command": lambda: self.send_pulse('3', 6), "color": "#f39c12"},
            {"text": "PIN 9", "command": lambda: self.send_pulse('4', 9), "color": "#9b59b6"}
        ]

        # Crear botones en grid 2x2
        for i, config in enumerate(button_configs):
            row = i // 2
            col = i % 2

            btn = tk.Button(buttons_frame, text=config["text"],
                          command=config["command"],
                          font=('Arial', 16, 'bold'),
                          bg=config["color"], fg='white',
                          width=15, height=3,
                          cursor='hand2',
                          relief='raised',
                          borderwidth=3)
            btn.grid(row=row, column=col, padx=20, pady=20)

        # Frame de información
        info_frame = tk.LabelFrame(self.root, text="Información",
                                 font=('Arial', 12, 'bold'), padx=20, pady=10)
        info_frame.pack(fill='x', padx=20, pady=10)

        # Log de actividad
        log_frame = tk.Frame(info_frame)
        log_frame.pack(fill='both', expand=True)

        tk.Label(log_frame, text="Registro de actividad:", font=('Arial', 10, 'bold')).pack(anchor='w')

        # Text widget con scrollbar
        text_frame = tk.Frame(log_frame)
        text_frame.pack(fill='both', expand=True, pady=5)

        self.log_text = tk.Text(text_frame, height=6, font=('Courier', 9))
        scrollbar = tk.Scrollbar(text_frame, orient='vertical', command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side='left', fill='both', expand=True)
        scrollbar.pack(side='right', fill='y')

        # Botones de utilidad
        utils_frame = tk.Frame(info_frame)
        utils_frame.pack(fill='x', pady=(10, 0))

        tk.Button(utils_frame, text="Limpiar Log", command=self.clear_log,
                font=('Arial', 9), bg='#95a5a6', fg='white').pack(side='left')

        tk.Button(utils_frame, text="Abrir Carpeta Imágenes", command=self.open_images_folder,
                font=('Arial', 9), bg='#16a085', fg='white').pack(side='left', padx=(10, 0))

        tk.Button(utils_frame, text="Ver Registro CSV", command=self.view_csv,
                font=('Arial', 9), bg='#8e44ad', fg='white').pack(side='left', padx=(10, 0))

        # Log inicial
        self.log_message("Aplicación iniciada. Configure el puerto COM y presione Conectar.")

    def toggle_connection(self):
        if not self.connected:
            self.connect_arduino()
        else:
            self.disconnect_arduino()

    def connect_arduino(self):
        try:
            self.arduino = serial.Serial(self.com_port.get(), 9600, timeout=1)
            time.sleep(2)
            self.connected = True

            self.connect_btn.config(text="Desconectar", bg='#e74c3c')
            self.status_label.config(text="Conectado", fg='green')
            self.log_message(f"Conectado al puerto {self.com_port.get()}")

        except Exception as e:
            messagebox.showerror("Error de Conexión",
                               f"No se pudo conectar al puerto {self.com_port.get()}\n\n{str(e)}")
            self.log_message(f"Error de conexión: {str(e)}")

    def disconnect_arduino(self):
        if self.arduino:
            self.arduino.close()
            self.arduino = None

        self.connected = False
        self.connect_btn.config(text="Conectar", bg='#27ae60')
        self.status_label.config(text="Desconectado", fg='red')
        self.log_message("Desconectado del Arduino")

        # Guardar registro de imágenes al desconectar
        self.save_images_log()

    def send_pulse(self, command, pin):
        if not self.connected or not self.arduino:
            messagebox.showwarning("Advertencia", "Primero debe conectarse al Arduino")
            return

        try:
            self.arduino.write(command.encode())
            self.log_message(f"Pulso enviado al PIN {pin}")

            if self.show_images.get():
                self.show_random_image(pin)

        except Exception as e:
            messagebox.showerror("Error", f"Error al enviar pulso: {str(e)}")
            self.log_message(f"Error al enviar pulso: {str(e)}")

    def show_random_image(self, pin_number):
        imagenes_dir = "imagenes"

        if not os.path.exists(imagenes_dir):
            self.log_message("Carpeta 'imagenes' no encontrada")
            return

        image_files = [f for f in os.listdir(imagenes_dir)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not image_files:
            self.log_message("No se encontraron imágenes en la carpeta")
            return

        # Si no hay imágenes disponibles, reiniciar la lista
        if not self.available_images:
            self.available_images = image_files.copy()
            self.used_images = []
            self.log_message(f"Reiniciando ciclo de imágenes. Total: {len(image_files)} imágenes")

        # Seleccionar imagen aleatoria de las disponibles
        random_image = random.choice(self.available_images)

        # Mover imagen de disponibles a usadas
        self.available_images.remove(random_image)
        self.used_images.append(random_image)

        image_path = os.path.join(imagenes_dir, random_image)

        remaining = len(self.available_images)
        self.log_message(f"Imagen seleccionada: {random_image} (Quedan {remaining} por mostrar)")

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.images_shown.append([timestamp, random_image, pin_number])

        def display_image():
            img_window = tk.Toplevel()
            img_window.attributes('-fullscreen', True)
            img_window.configure(bg='black')
            img_window.attributes('-topmost', True)

            try:
                image = Image.open(image_path)
                screen_width = img_window.winfo_screenwidth()
                screen_height = img_window.winfo_screenheight()

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

                label = tk.Label(img_window, image=photo, bg='black')
                label.pack(expand=True)
                label.image = photo  # Mantener referencia

                def close_window():
                    img_window.destroy()

                img_window.after(10000, close_window)
                img_window.bind('<Escape>', lambda e: img_window.destroy())
                img_window.bind('<Button-1>', lambda e: img_window.destroy())

            except Exception as e:
                self.log_message(f"Error al mostrar imagen: {e}")
                img_window.destroy()

        threading.Thread(target=display_image, daemon=True).start()
        self.log_message(f"Mostrando imagen: {random_image}")

    def log_message(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def clear_log(self):
        self.log_text.delete(1.0, tk.END)

    def open_images_folder(self):
        if not os.path.exists("imagenes"):
            os.makedirs("imagenes")
        os.startfile("imagenes")

    def view_csv(self):
        if os.path.exists("imagenes_mostradas.csv"):
            os.startfile("imagenes_mostradas.csv")
        else:
            messagebox.showinfo("Información", "Aún no se ha generado el archivo CSV")

    def save_images_log(self):
        if self.images_shown:
            try:
                with open('imagenes_mostradas.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Timestamp', 'Nombre_Imagen', 'Pin_Activado'])
                    for entry in self.images_shown:
                        writer.writerow(entry)
                print(f"Registro CSV guardado: {len(self.images_shown)} imágenes en 'imagenes_mostradas.csv'")
                self.log_message(f"Registro CSV guardado: {len(self.images_shown)} imágenes")
            except Exception as e:
                print(f"Error al guardar registro CSV: {e}")
                self.log_message(f"Error al guardar registro CSV: {e}")
        else:
            self.log_message("No hay imágenes para guardar en el registro")

    def on_closing(self):
        if self.connected:
            self.disconnect_arduino()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ArduinoPulsosGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()