# Control de Pulsos Arduino desde Python

Este proyecto permite enviar pulsos de 200ms a los pines digitales del Arduino UNO desde Python presionando las teclas 1-4.

## Configuración del Hardware

- **Pin 3**: Controlado por la tecla '1'
- **Pin 5**: Controlado por la tecla '2'
- **Pin 6**: Controlado por la tecla '3'
- **Pin 9**: Controlado por la tecla '4'

## Instalación

1. **Código Arduino:**
   ```bash
   pio run -t upload
   ```

2. **Dependencias Python:**
   ```bash
   pip install -r requirements.txt
   ```

## Uso

1. Conecta el Arduino UNO al puerto COM3 (o modifica el puerto en `control_pulsos.py`)
2. Carga el código Arduino usando PlatformIO
3. Ejecuta el script Python:
   ```bash
   python control_pulsos.py
   ```
4. Presiona las teclas 1-4 para enviar pulsos a los pines correspondientes
5. Presiona 'q' para salir

## Notas

- El programa requiere permisos de administrador en Windows para capturar las teclas
- Los pulsos tienen una duración de 200ms
- La comunicación serie se establece a 9600 baudios