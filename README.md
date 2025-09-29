# Sensashot

**Sistema modular para control de triggers sincronizados y registro de estímulos sensoriales.**

## Descripción General

Sensashot ofrece dos versiones distintas para diferentes necesidades de investigación:

1. **Versión Arduino**: Control directo de hardware con triggers al OpenBCI
2. **Versión Web**: Interfaz web para registro temporal sin hardware

## Versiones Disponibles

### 🔌 **Versión Arduino** (`/sensashot-arduino/`)
Sistema completo con control de hardware para OpenBCI Cyton + Daisy:

**Características:**
- Control de Arduino via puerto serie
- Envío de pulsos de 200ms a pines digitales (3, 5, 6, 9)
- Interfaz GUI con Tkinter (versión PRO)
- Presentación sincronizada de imágenes de estímulo
- Registro automático de eventos con timestamps
- Exportación de datos en formato CSV
- Versión MPV minimalista incluida

**Instalación:**
```bash
cd sensashot-arduino
pip install -r requirements.txt
pio run -t upload  # Cargar código Arduino
python interfaz_cliente.py
```

### 🌐 **Versión Web** (`/sensashot-web/`)
Interfaz web pura sin dependencias de hardware:

**Características:**
- Interfaz web moderna HTML/CSS/JavaScript
- Registro de estímulos olfativos, hápticos y visuales
- Timestamps precisos en milisegundos
- Sin dependencias de Arduino o hardware externo
- Configuración flexible de tiempo de exposición
- Funciona en cualquier dispositivo con navegador
- Exportación CSV automática

**Uso:**
```bash
cd sensashot-web
python -m http.server 8000
# Abrir: http://localhost:8000
```

## Casos de Uso

### Investigación EEG/BCI
- **Versión Arduino**: Triggers precisos para OpenBCI, análisis de potenciales evocados
- **Versión Web**: Registro temporal para correlación posterior con datos EEG

### Estudios de Percepción Sensorial
- **Estímulos olfativos**: Registro temporal de aplicación de aromas
- **Estímulos hápticos**: Timing de estímulos táctiles/vibratorios
- **Estímulos visuales**: Presentación controlada de imágenes

### Aplicaciones Clínicas
- **Versión Arduino**: Paradigmas P300, sincronización estímulo-respuesta
- **Versión Web**: Registro móvil, estudios en campo

## Comparación de Versiones

| Característica | Arduino | Web |
|----------------|---------|-----|
| Hardware requerido | ✅ Arduino + OpenBCI | ❌ Solo navegador |
| Triggers hardware | ✅ Sí | ❌ No |
| Multiplataforma | ⚠️ Python requerido | ✅ Cualquier dispositivo |
| Precisión timing | ✅ Alta (hardware) | ⚠️ Dependiente del navegador |
| Facilidad uso | ⚠️ Instalación requerida | ✅ Inmediato |
| Costo setup | ⚠️ Hardware adicional | ✅ Gratis |

## Requisitos

### Versión Arduino
- Arduino UNO + OpenBCI Cyton + Daisy
- Python 3.7+ con PlatformIO
- Windows: Permisos de administrador

### Versión Web
- Navegador moderno (Chrome 70+, Firefox 65+, Safari 12+)
- Opcional: Servidor local (Python, Node.js, etc.)

## Instalación Rápida

### Versión Arduino
```bash
# 1. Clonar repositorio
git clone [URL_DEL_REPOSITORIO]
cd Sensashot/sensashot-arduino

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. Cargar código Arduino
pio run -t upload

# 4. Ejecutar interfaz
python interfaz_cliente.py
```

### Versión Web
```bash
# 1. Navegar al directorio web
cd Sensashot/sensashot-web

# 2. Iniciar servidor local
python -m http.server 8000

# 3. Abrir navegador
# http://localhost:8000
```

## Configuración Hardware (Solo Versión Arduino)

**Mapeo de Pines Arduino UNO:**
- Pin 3 → OpenBCI D11 (Canal 1)
- Pin 5 → OpenBCI D12 (Canal 2)
- Pin 6 → OpenBCI D13 (Canal 3)
- Pin 9 → OpenBCI D18 (Canal 4)
- GND → OpenBCI GND
- 5V → OpenBCI DVDD

**Diagrama de Conexiones:**

<img width="1219" height="1112" alt="image" src="https://github.com/user-attachments/assets/14f23aee-3cd4-477f-ac1b-f52db0a1c79a" />

## Documentación Detallada

- **Arduino**: Ver `sensashot-arduino/README.md`
- **Web**: Ver `sensashot-web/README.md`
- **OpenBCI**: https://docs.openbci.com/Cyton/CytonExternal/
