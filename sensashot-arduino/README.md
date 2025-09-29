# Sensashot Arduino Version

Sistema completo de control de triggers sincronizados con Arduino para OpenBCI Cyton + Daisy.

## Características

- **Interfaz GUI completa** con Tkinter (`interfaz_cliente.py`)
- **Control Arduino** via puerto serie para envío de pulsos
- **Estimulación visual** con presentación de imágenes sincronizada
- **Registro de eventos** con timestamps precisos en CSV
- **Versión PRO** con funcionalidades avanzadas
- **Versión MPV** (Minimum Viable Product) para control básico

## Archivos Principales

### Versión PRO (Completa)
- `interfaz_cliente.py` - Interfaz gráfica principal
- `control_pulsos.py` - Control avanzado de pulsos
- `control_pulsos_simple.py` - Control básico de pulsos
- `platformio.ini` - Configuración del proyecto Arduino
- `src/main.cpp` - Código Arduino principal
- `imagenes/` - Directorio de imágenes de estímulo

### Versión MPV (Básica)
- `arduino_pulse_control.py` - Control directo de Arduino
- `pulse_control_gui.py` - Interfaz GUI simple
- `mpv_control_pulsos_simple.py` - Control minimalista
- `arduino_sketch.ino` - Código Arduino básico

## Requisitos

### Hardware
- Arduino UNO
- OpenBCI Cyton + Daisy
- Cables de conexión

### Software
- Python 3.7+
- PlatformIO Core o Arduino IDE

## Instalación

1. **Instalar dependencias Python:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cargar código Arduino:**
   ```bash
   # Con PlatformIO
   pio run -t upload

   # O usar Arduino IDE con el archivo .ino
   ```

3. **Verificar puerto COM:**
   - Windows: Device Manager > Ports (COM & LPT)
   - Actualizar puerto en el código Python

## Uso

### Versión PRO
```bash
python interfaz_cliente.py
```

### Versión MPV
```bash
python pulse_control_gui.py
# O para control por teclado:
python mpv_control_pulsos_simple.py
```

## Mapeo de Pines Arduino

- **Pin 3**: Trigger Canal 1 (Tecla '1')
- **Pin 5**: Trigger Canal 2 (Tecla '2')
- **Pin 6**: Trigger Canal 3 (Tecla '3')
- **Pin 9**: Trigger Canal 4 (Tecla '4')

## Configuración OpenBCI

Conectar pines digitales Arduino → Entradas trigger OpenBCI:
- Arduino Pin 3 → OpenBCI Digital Input D11
- Arduino Pin 5 → OpenBCI Digital Input D12
- Arduino Pin 6 → OpenBCI Digital Input D13
- Arduino Pin 9 → OpenBCI Digital Input D18
- Arduino GND → OpenBCI GND
- Arduino 5V → OpenBCI DVDD

**Baudrate**: 9600
**Duración de pulsos**: 200ms

## Solución de Problemas

- **Error puerto serie**: Verificar conexión Arduino y puerto COM
- **Permisos Windows**: Ejecutar como Administrador
- **Dependencias**: Reinstalar con `pip install --upgrade -r requirements.txt`