import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import time
import os
import random
import threading
import csv
import atexit
from datetime import datetime
from PIL import Image, ImageTk

class StimulusTimingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Registro de Estímulos - Sensashot")
        self.root.geometry("900x700")
        self.root.configure(bg='#f0f0f0')

        # Variables
        self.stimuli_log = []
        self.visual_exposure_time = tk.IntVar(value=5000)  # 5 segundos por defecto
        self.show_visual_images = tk.BooleanVar(value=True)
        self.available_images = []
        self.used_images = []

        # Configurar cierre del programa
        atexit.register(self.save_stimuli_log)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.setup_ui()

    def setup_ui(self):
        # Título principal
        title_frame = tk.Frame(self.root, bg='#2c3e50', height=80)
        title_frame.pack(fill='x', pady=(0, 20))
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="Sistema de Registro de Estímulos",
                              font=('Arial', 24, 'bold'), fg='white', bg='#2c3e50')
        title_label.pack(expand=True)

        # Frame de configuración
        config_frame = tk.LabelFrame(self.root, text="Configuración de Estímulos",
                                   font=('Arial', 12, 'bold'), padx=20, pady=10)
        config_frame.pack(fill='x', padx=20, pady=10)

        # Configuración de tiempo de exposición visual
        visual_config_frame = tk.Frame(config_frame)
        visual_config_frame.pack(fill='x', pady=5)

        tk.Label(visual_config_frame, text="Tiempo de exposición visual (ms):",
                font=('Arial', 10)).pack(side='left')

        time_spinbox = tk.Spinbox(visual_config_frame, from_=500, to=30000, increment=500,
                                 textvariable=self.visual_exposure_time, font=('Arial', 10),
                                 width=10)
        time_spinbox.pack(side='left', padx=(10, 20))

        tk.Label(visual_config_frame, text="ms", font=('Arial', 10)).pack(side='left')

        # Checkbox para mostrar imágenes
        img_check = tk.Checkbutton(config_frame, text="Mostrar imágenes durante estímulo visual",
                                 variable=self.show_visual_images, font=('Arial', 10))
        img_check.pack(anchor='w', pady=5)

        # Frame de controles principales
        control_frame = tk.LabelFrame(self.root, text="Registro de Estímulos",
                                    font=('Arial', 14, 'bold'), padx=20, pady=20)
        control_frame.pack(fill='both', expand=True, padx=20, pady=10)

        # Grid de botones para estímulos
        buttons_frame = tk.Frame(control_frame)
        buttons_frame.pack(expand=True)

        # Configuración de botones para cada tipo de estímulo
        button_configs = [
            {
                "text": "ESTÍMULO\nOLFATIVO",
                "command": lambda: self.log_stimulus('Olfativo'),
                "color": "#e74c3c",
                "description": "Registrar estímulo olfativo"
            },
            {
                "text": "ESTÍMULO\nHÁPTICO",
                "command": lambda: self.log_stimulus('Haptico'),
                "color": "#3498db",
                "description": "Registrar estímulo háptico"
            },
            {
                "text": "ESTÍMULO\nVISUAL",
                "command": lambda: self.log_visual_stimulus(),
                "color": "#f39c12",
                "description": "Registrar estímulo visual con imagen"
            }
        ]

        # Crear botones en grid
        for i, config in enumerate(button_configs):
            row = i // 2
            col = i % 2

            btn = tk.Button(buttons_frame, text=config["text"],
                          command=config["command"],
                          font=('Arial', 14, 'bold'),
                          bg=config["color"], fg='white',
                          width=18, height=4,
                          cursor='hand2',
                          relief='raised',
                          borderwidth=3)
            btn.grid(row=row, column=col, padx=20, pady=20)

        # Botón de reinicio de sesión
        reset_btn = tk.Button(control_frame, text="REINICIAR SESIÓN",
                            command=self.reset_session,
                            font=('Arial', 12, 'bold'),
                            bg='#95a5a6', fg='white',
                            width=20, height=2,
                            cursor='hand2')
        reset_btn.pack(pady=20)

        # Frame de información y estadísticas
        info_frame = tk.LabelFrame(self.root, text="Información de Sesión",
                                 font=('Arial', 12, 'bold'), padx=20, pady=10)
        info_frame.pack(fill='x', padx=20, pady=10)

        # Estadísticas
        stats_frame = tk.Frame(info_frame)
        stats_frame.pack(fill='x', pady=5)

        self.stats_label = tk.Label(stats_frame, text="Estímulos registrados: 0 | Olfativos: 0 | Hápticos: 0 | Visuales: 0",
                                   font=('Arial', 10, 'bold'))
        self.stats_label.pack(anchor='w')

        # Log de actividad
        log_frame = tk.Frame(info_frame)
        log_frame.pack(fill='both', expand=True)

        tk.Label(log_frame, text="Registro de actividad:", font=('Arial', 10, 'bold')).pack(anchor='w')

        # Text widget con scrollbar
        text_frame = tk.Frame(log_frame)
        text_frame.pack(fill='both', expand=True, pady=5)

        self.log_text = tk.Text(text_frame, height=8, font=('Courier', 9))
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

        tk.Button(utils_frame, text="Exportar CSV", command=self.export_csv,
                font=('Arial', 9), bg='#d35400', fg='white').pack(side='left', padx=(10, 0))

        # Log inicial
        self.log_message("Sistema de registro de estímulos iniciado.")
        self.log_message("Tiempo de exposición visual configurado a {} ms.".format(self.visual_exposure_time.get()))

    def log_stimulus(self, stimulus_type):
        """Registra un estímulo con timestamp exacto"""
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]  # Incluir milisegundos

        stimulus_entry = {
            'timestamp': timestamp_str,
            'type': stimulus_type,
            'exposure_time_ms': None,
            'image_shown': None,
            'notes': ''
        }

        self.stimuli_log.append(stimulus_entry)
        self.log_message(f"ESTÍMULO {stimulus_type.upper()} registrado a las {timestamp_str}")
        self.update_statistics()

    def log_visual_stimulus(self):
        """Registra un estímulo visual y opcionalmente muestra imagen"""
        timestamp = datetime.now()
        timestamp_str = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]

        image_shown = None
        exposure_time = self.visual_exposure_time.get()

        if self.show_visual_images.get():
            image_shown = self.show_random_image(exposure_time)

        stimulus_entry = {
            'timestamp': timestamp_str,
            'type': 'Visual',
            'exposure_time_ms': exposure_time,
            'image_shown': image_shown,
            'notes': ''
        }

        self.stimuli_log.append(stimulus_entry)

        if image_shown:
            self.log_message(f"ESTÍMULO VISUAL registrado a las {timestamp_str} - Imagen: {image_shown} ({exposure_time}ms)")
        else:
            self.log_message(f"ESTÍMULO VISUAL registrado a las {timestamp_str} ({exposure_time}ms)")

        self.update_statistics()

    def show_random_image(self, exposure_time):
        """Muestra una imagen aleatoria por el tiempo especificado"""
        imagenes_dir = "imagenes"

        if not os.path.exists(imagenes_dir):
            self.log_message("Carpeta 'imagenes' no encontrada")
            return None

        image_files = [f for f in os.listdir(imagenes_dir)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]

        if not image_files:
            self.log_message("No se encontraron imágenes en la carpeta")
            return None

        # Sistema de rotación de imágenes
        if not self.available_images:
            self.available_images = image_files.copy()
            self.used_images = []
            self.log_message(f"Reiniciando ciclo de imágenes. Total: {len(image_files)} imágenes")

        random_image = random.choice(self.available_images)
        self.available_images.remove(random_image)
        self.used_images.append(random_image)

        image_path = os.path.join(imagenes_dir, random_image)
        remaining = len(self.available_images)
        self.log_message(f"Mostrando imagen: {random_image} por {exposure_time}ms (Quedan {remaining})")

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
                label.image = photo

                def close_window():
                    img_window.destroy()

                img_window.after(exposure_time, close_window)
                img_window.bind('<Escape>', lambda e: img_window.destroy())
                img_window.bind('<Button-1>', lambda e: img_window.destroy())

            except Exception as e:
                self.log_message(f"Error al mostrar imagen: {e}")
                img_window.destroy()

        threading.Thread(target=display_image, daemon=True).start()
        return random_image

    def update_statistics(self):
        """Actualiza las estadísticas mostradas"""
        total = len(self.stimuli_log)
        olfativo = len([s for s in self.stimuli_log if s['type'] == 'Olfativo'])
        haptico = len([s for s in self.stimuli_log if s['type'] == 'Haptico'])
        visual = len([s for s in self.stimuli_log if s['type'] == 'Visual'])

        stats_text = f"Estímulos registrados: {total} | Olfativos: {olfativo} | Hápticos: {haptico} | Visuales: {visual}"
        self.stats_label.config(text=stats_text)

    def reset_session(self):
        """Reinicia la sesión actual"""
        if self.stimuli_log:
            result = messagebox.askyesno("Confirmar Reinicio",
                                       f"¿Desea reiniciar la sesión?\n\nSe perderán {len(self.stimuli_log)} registros no guardados.")
            if result:
                self.save_stimuli_log()  # Guardar antes de reiniciar
                self.stimuli_log = []
                self.available_images = []
                self.used_images = []
                self.clear_log()
                self.update_statistics()
                self.log_message("Sesión reiniciada. Datos anteriores guardados en CSV.")
        else:
            self.log_message("No hay datos para reiniciar.")

    def log_message(self, message):
        """Añade mensaje al log de actividad"""
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        log_entry = f"[{timestamp}] {message}\n"

        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)

    def clear_log(self):
        """Limpia el log de actividad"""
        self.log_text.delete(1.0, tk.END)

    def open_images_folder(self):
        """Abre la carpeta de imágenes"""
        if not os.path.exists("imagenes"):
            os.makedirs("imagenes")
        os.startfile("imagenes")

    def view_csv(self):
        """Abre el archivo CSV de registros"""
        if os.path.exists("registro_estimulos.csv"):
            os.startfile("registro_estimulos.csv")
        else:
            messagebox.showinfo("Información", "Aún no se ha generado el archivo CSV")

    def export_csv(self):
        """Exporta manualmente el CSV"""
        if self.stimuli_log:
            self.save_stimuli_log()
            messagebox.showinfo("Exportación", f"CSV exportado con {len(self.stimuli_log)} registros")
        else:
            messagebox.showinfo("Sin datos", "No hay registros para exportar")

    def save_stimuli_log(self):
        """Guarda el registro de estímulos en CSV"""
        if self.stimuli_log:
            try:
                filename = f"registro_estimulos_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"

                with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['timestamp', 'type', 'exposure_time_ms', 'image_shown', 'notes']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for entry in self.stimuli_log:
                        writer.writerow(entry)

                # También mantener el archivo general
                with open('registro_estimulos.csv', 'w', newline='', encoding='utf-8') as csvfile:
                    fieldnames = ['timestamp', 'type', 'exposure_time_ms', 'image_shown', 'notes']
                    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                    writer.writeheader()
                    for entry in self.stimuli_log:
                        writer.writerow(entry)

                print(f"Registro guardado: {len(self.stimuli_log)} estímulos en '{filename}'")
                self.log_message(f"Registro CSV guardado: {len(self.stimuli_log)} estímulos")

            except Exception as e:
                print(f"Error al guardar registro: {e}")
                self.log_message(f"Error al guardar registro: {e}")

    def on_closing(self):
        """Maneja el cierre de la aplicación"""
        if self.stimuli_log:
            self.save_stimuli_log()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = StimulusTimingGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()