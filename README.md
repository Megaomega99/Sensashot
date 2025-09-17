# Sensashot

**Interfaz de control para envío de triggers sincronizados al sistema de adquisición de datos OpenBCI Cyton + Daisy con estimulaciones visuales integradas.**

## Descripción General

Sensashot es un sistema completo para investigación en neurociencia que permite la sincronización precisa entre:

- **Triggers de control** enviados via Arduino al sistema OpenBCI Cyton + Daisy
- **Estimulaciones visuales** controladas y temporizadas
- **Registro de eventos** para análisis posterior
- **Interfaz intuitiva** para el control experimental

## Versiones Disponibles

### 🏢 **Versión PRO** (`/PRO/`)
Interfaz gráfica completa con funcionalidades avanzadas:

**Características:**
- Interfaz GUI con Tkinter para control intuitivo
- Control de pulsos de 200ms a pines digitales del Arduino (3, 5, 6, 9)
- Presentación sincronizada de imágenes de estímulo
- Registro automático de eventos con timestamps
- Configuración flexible del puerto COM
- Exportación de datos en formato CSV

**Instalación:**
```bash
cd PRO
pip install -r requirements.txt
pio run -t upload  # Cargar código Arduino
python interfaz_cliente.py
```

### ⚡ **Versión MPV** (`/MPV/`)
Versión mínima viable para control básico:

**Características:**
- Control directo por teclado (teclas 1-4)
- Envío de pulsos a pines específicos del Arduino
- Comunicación serie optimizada
- Interfaz minimalista

**Uso:**
```bash
cd MPV
python control_pulsos_simple.py
```

## Configuración del Hardware

**Arduino UNO - Mapeo de Pines:**
- **Pin 3**: Trigger Canal 1 (Tecla '1')
- **Pin 5**: Trigger Canal 2 (Tecla '2')
- **Pin 6**: Trigger Canal 3 (Tecla '3')
- **Pin 9**: Trigger Canal 4 (Tecla '4')

**Conexión OpenBCI:**
- Conectar pines digitales Arduino → Entradas trigger OpenBCI Cyton + Daisy
- Configurar baudrate: 9600

## Casos de Uso

### Investigación EEG
- Presentación de estímulos visuales sincronizados
- Marcado temporal preciso de eventos
- Análisis de potenciales evocados

### Experimentos BCI
- Control de paradigmas P300
- Sincronización estímulo-respuesta
- Registro de sesiones experimentales

## Requisitos del Sistema

- **Hardware**: Arduino UNO, OpenBCI Cyton + Daisy
- **Software**: Python 3.7+, PlatformIO
- **Permisos**: Administrador (Windows) para captura de teclas
- **Dependencias**: Ver `requirements.txt` en cada versión

## Guía de Instalación Completa

### 1. Instalación de Software Base

#### Python 3.7+
```bash
# Descargar desde https://www.python.org/downloads/
# Durante la instalación, marcar "Add Python to PATH"
```

#### PlatformIO Core
```bash
# Opción 1: Instalación independiente
pip install platformio

# Opción 2: VS Code Extension
# Instalar "PlatformIO IDE" desde VS Code Extensions
```

#### Git (Opcional)
```bash
# Descargar desde https://git-scm.com/downloads
```

### 2. Configuración del Proyecto

#### Clonar/Descargar Proyecto
```bash
git clone [URL_DEL_REPOSITORIO]
cd Sensashot
```

#### Instalar Dependencias Python
```bash
# Para versión PRO
cd PRO
pip install -r requirements.txt

# Para versión MPV
cd ../MPV
pip install -r requirements.txt  # si existe
```

### 3. Configuración del Hardware Arduino

#### Cargar Firmware Arduino
```bash
# Desde la carpeta del proyecto con platformio.ini
pio run -t upload

# O usar Arduino IDE con el código .ino correspondiente
```

#### Verificar Puerto COM
```bash
# Windows: Revisar Device Manager > Ports (COM & LPT)
# Actualizar puerto en el código Python si es necesario
```

### 4. Conexiones Hardware

#### Arduino UNO ↔ OpenBCI Cyton + Daisy

Para las conexiones detalladas entre Arduino y OpenBCI, consultar:
- **Documentación oficial**: https://docs.openbci.com/Cyton/CytonExternal/

**Diagrama de Conexiones:**

![Diagrama de conexiones Arduino-OpenBCI](images/arduino-openbci-wiring.png)

**Conexiones específicas del diagrama:**
- Arduino Pin 3 → OpenBCI Digital Input D11 (Cable Celeste)
- Arduino Pin 5 → OpenBCI Digital Input D12 (Cable Rojo)
- Arduino Pin 6 → OpenBCI Digital Input D13 (Cable Verde)
- Arduino Pin 9 → OpenBCI Digital Input D18 (Cable Naranja)
- Arduino GND → OpenBCI GND (Cable Negro)
- Arduino 5V → OpenBCI DVDD (Cable Rojo - Alimentación)

### 5. Prueba del Sistema

#### Verificar Comunicación
```bash
# Ejecutar versión básica para probar conexión
cd MPV
python control_pulsos_simple.py
```

#### Ejecutar Versión Completa
```bash
# Ejecutar interfaz gráfica PRO
cd PRO
python interfaz_cliente.py
```

### 6. Solución de Problemas Comunes

#### Error de Puerto Serie
- Verificar que el Arduino esté conectado
- Confirmar el puerto COM correcto
- Cerrar otras aplicaciones que usen el puerto

#### Permisos en Windows
- Ejecutar como Administrador para captura de teclas
- Configurar antivirus para permitir acceso al puerto serie

#### Dependencias Faltantes
```bash
# Reinstalar dependencias
pip install --upgrade -r requirements.txt
```

### 7. Notas Importantes

- **Baudrate**: Mantener 9600 en Arduino y Python
- **Timing**: Los pulsos están configurados a 200ms
- **Sincronización**: Verificar timestamps en los logs para confirmar precisión
- **Backup**: Guardar configuraciones antes de modificar código

Para más detalles sobre las conexiones específicas de OpenBCI, consultar la documentación oficial en el enlace proporcionado y seguir el diagrama de conexiones de referencia.
