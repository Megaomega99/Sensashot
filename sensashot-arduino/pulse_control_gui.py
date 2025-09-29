import tkinter as tk
from tkinter import ttk, messagebox
import serial
import serial.tools.list_ports
import time
import threading
import os
from PIL import Image, ImageTk

class ArduinoPulseGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Arduino Pulse Controller")
        self.root.geometry("400x300")

        self.arduino = None
        self.connected = False

        self.setup_ui()
        self.setup_logo()
        self.update_ports()

    def setup_ui(self):
        # Connection frame
        conn_frame = ttk.LabelFrame(self.root, text="Connection", padding="10")
        conn_frame.pack(fill="x", padx=10, pady=5)

        # Port selection
        ttk.Label(conn_frame, text="Port:").grid(row=0, column=0, sticky="w")
        self.port_var = tk.StringVar()
        self.port_combo = ttk.Combobox(conn_frame, textvariable=self.port_var, width=15)
        self.port_combo.grid(row=0, column=1, padx=5)

        # Refresh and Connect buttons
        ttk.Button(conn_frame, text="Refresh", command=self.update_ports).grid(row=0, column=2, padx=5)
        self.connect_btn = ttk.Button(conn_frame, text="Connect", command=self.toggle_connection)
        self.connect_btn.grid(row=0, column=3, padx=5)

        # Status label
        self.status_label = ttk.Label(conn_frame, text="Disconnected", foreground="red")
        self.status_label.grid(row=1, column=0, columnspan=4, pady=5)

        # Control frame
        control_frame = ttk.LabelFrame(self.root, text="Pulse Control", padding="10")
        control_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Pulse buttons
        button_frame = ttk.Frame(control_frame)
        button_frame.pack(expand=True)

        self.pulse_buttons = []
        pin_mapping = {1: 3, 2: 5, 3: 6, 4: 9}

        for i in range(1, 5):
            btn = ttk.Button(
                button_frame,
                text=f"Pulse {i}\n(Pin {pin_mapping[i]})",
                command=lambda x=i: self.send_pulse(x),
                width=15,
                state="disabled"
            )
            btn.grid(row=(i-1)//2, column=(i-1)%2, padx=10, pady=10)
            self.pulse_buttons.append(btn)

        # Keyboard shortcuts info
        info_frame = ttk.Frame(self.root)
        info_frame.pack(fill="x", padx=10, pady=5)
        ttk.Label(info_frame, text="Keyboard shortcuts: 1, 2, 3, 4 for pulses").pack()

        # Bind keyboard events
        self.root.bind('<Key>', self.on_key_press)
        self.root.focus_set()

    def update_ports(self):
        ports = [port.device for port in serial.tools.list_ports.comports()]
        self.port_combo['values'] = ports
        if ports and not self.port_var.get():
            self.port_var.set(ports[0])

    def toggle_connection(self):
        if self.connected:
            self.disconnect()
        else:
            self.connect()

    def connect(self):
        port = self.port_var.get()
        if not port:
            messagebox.showerror("Error", "Please select a port")
            return

        try:
            self.arduino = serial.Serial(port, 9600, timeout=1)
            time.sleep(2)  # Wait for Arduino to initialize

            self.connected = True
            self.connect_btn.config(text="Disconnect")
            self.status_label.config(text=f"Connected to {port}", foreground="green")

            # Enable pulse buttons
            for btn in self.pulse_buttons:
                btn.config(state="normal")

            messagebox.showinfo("Success", f"Connected to Arduino on {port}")

        except serial.SerialException as e:
            messagebox.showerror("Connection Error", f"Failed to connect to {port}: {e}")

    def disconnect(self):
        if self.arduino:
            self.arduino.close()
            self.arduino = None

        self.connected = False
        self.connect_btn.config(text="Connect")
        self.status_label.config(text="Disconnected", foreground="red")

        # Disable pulse buttons
        for btn in self.pulse_buttons:
            btn.config(state="disabled")

    def send_pulse(self, button_number):
        if not self.connected or not self.arduino:
            messagebox.showerror("Error", "Arduino not connected")
            return

        pin_mapping = {1: 3, 2: 5, 3: 6, 4: 9}
        pin = pin_mapping[button_number]

        try:
            command = f"PULSE_{pin}\n"
            self.arduino.write(command.encode())

            # Read response in a separate thread to avoid blocking UI
            threading.Thread(target=self.read_response, daemon=True).start()

        except Exception as e:
            messagebox.showerror("Error", f"Failed to send pulse: {e}")

    def read_response(self):
        try:
            if self.arduino:
                response = self.arduino.readline().decode().strip()
                if response:
                    print(f"Arduino: {response}")
        except Exception as e:
            print(f"Error reading response: {e}")

    def on_key_press(self, event):
        if event.char in '1234' and self.connected:
            self.send_pulse(int(event.char))

    def setup_logo(self):
        """Configura el logo de Megaomega en la esquina inferior derecha"""
        try:
            # Cargar y redimensionar el logo
            logo_path = os.path.join("imagenes", "Megaomega.png")
            if os.path.exists(logo_path):
                # Cargar imagen
                img = Image.open(logo_path)
                # Redimensionar a tamaño muy pequeño (25x25 pixels)
                img_resized = img.resize((25, 25), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(img_resized)

                # Crear label para el logo en la esquina inferior derecha
                self.logo_label = tk.Label(self.root, image=self.logo_photo)
                self.logo_label.place(relx=1.0, rely=1.0, anchor='se', x=-5, y=-5)
            else:
                print("Logo Megaomega.png no encontrado en la carpeta imagenes")
        except Exception as e:
            print(f"Error cargando logo: {e}")

    def on_closing(self):
        self.disconnect()
        self.root.destroy()

def main():
    root = tk.Tk()
    app = ArduinoPulseGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()

if __name__ == "__main__":
    main()