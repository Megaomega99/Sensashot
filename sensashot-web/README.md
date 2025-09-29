# Sensashot PRO - Interfaz Web Profesional

Sistema web profesional para el registro de estímulos sensoriales, diseñado para uso en producción en entornos de investigación y aplicaciones clínicas.

## 🚀 Características Principales

### ✨ Interfaz Moderna y Profesional
- **Diseño responsive**: Adaptable a cualquier dispositivo (desktop, tablet, móvil)
- **UI/UX intuitiva**: Interfaz clara y fácil de usar
- **Animaciones fluidas**: Feedback visual profesional
- **Tema moderno**: Gradientes y colores profesionales

### 🎯 Funcionalidades Avanzadas
- **Registro de alta precisión**: Timestamps con milisegundos
- **Tres tipos de estímulos**: Olfativo, Háptico y Visual
- **Configuración flexible**: Tiempo de exposición visual configurable
- **Atajos de teclado**: Acceso rápido (1, 2, 3)
- **Retroalimentación sonora**: Audio opcional para confirmación
- **Sistema de imágenes**: Rotación sin repetición hasta completar ciclo

### 📊 Monitoreo y Analytics
- **Estadísticas en tiempo real**: Contadores por tipo de estímulo
- **Cronómetro de sesión**: Tiempo transcurrido desde inicio
- **Log de actividad**: Registro detallado con timestamps
- **Exportación CSV**: Descarga automática de datos

### 🔧 Características Técnicas
- **Sin dependencias**: Funciona completamente offline
- **Compatible**: Todos los navegadores modernos
- **Ligero**: Carga rápida y rendimiento optimizado
- **Seguro**: No requiere permisos especiales

## 📁 Estructura del Proyecto

```
web_interface/
├── index.html              # Página principal
├── assets/
│   ├── css/
│   │   └── style.css       # Estilos principales
│   ├── js/
│   │   └── app.js          # Funcionalidad JavaScript
│   └── images/             # Banco de imágenes para estímulos
├── README.md               # Documentación
└── SETUP.md               # Guía de instalación
```

## 🏗️ Instalación y Configuración

### Requisitos Mínimos
- **Navegador web moderno** (Chrome 70+, Firefox 65+, Safari 12+, Edge 79+)
- **Servidor web local** (opcional pero recomendado)

### Opción 1: Usar con Servidor Web Local (Recomendado)

#### Python (incluido en la mayoría de sistemas)
```bash
# Navegar al directorio web_interface
cd stimulus_logger/web_interface

# Python 3
python -m http.server 8000

# Python 2 (legacy)
python -m SimpleHTTPServer 8000

# Abrir navegador en: http://localhost:8000
```

#### Node.js
```bash
# Instalar servidor simple
npm install -g http-server

# Navegar al directorio
cd stimulus_logger/web_interface

# Iniciar servidor
http-server -p 8000

# Abrir navegador en: http://localhost:8000
```

#### PHP
```bash
# Navegar al directorio
cd stimulus_logger/web_interface

# Iniciar servidor PHP
php -S localhost:8000

# Abrir navegador en: http://localhost:8000
```

### Opción 2: Archivo Local (Limitaciones)
1. Abrir directamente `index.html` en el navegador
2. **Nota**: Las imágenes pueden no cargar debido a políticas CORS

### Opción 3: Extensión Live Server (VS Code)
1. Instalar extensión "Live Server" en VS Code
2. Hacer clic derecho en `index.html`
3. Seleccionar "Open with Live Server"

## 🎮 Guía de Uso

### Inicio Rápido
1. **Abrir la aplicación** en el navegador
2. **Leer las instrucciones** en el panel superior (colapsible)
3. **Configurar parámetros** (tiempo de exposición, opciones)
4. **Comenzar a registrar** estímulos usando los botones

### Tipos de Estímulos

#### 🌬️ Estímulo Olfativo
- **Propósito**: Registrar aplicación de olores/aromas
- **Uso**: Presionar botón inmediatamente al aplicar estímulo
- **Atajo**: Tecla `1`

#### ✋ Estímulo Háptico
- **Propósito**: Registrar estímulos táctiles, vibratorios o de textura
- **Uso**: Presionar botón al momento del contacto
- **Atajo**: Tecla `2`

#### 👁️ Estímulo Visual
- **Propósito**: Presentar imágenes con duración controlada
- **Uso**: Presionar botón para mostrar imagen
- **Atajo**: Tecla `3`
- **Configuración**: Tiempo ajustable (0.5-30 segundos)

### Configuración Avanzada

#### Tiempo de Exposición Visual
- **Rango**: 500ms - 30,000ms (0.5 - 30 segundos)
- **Incrementos**: 500ms
- **Default**: 5 segundos
- **Aplicación**: Se aplica a todos los estímulos visuales siguientes

#### Opciones del Sistema
- **Mostrar imágenes**: Habilitar/deshabilitar visualización de imágenes
- **Retroalimentación sonora**: Audio de confirmación al registrar
- **Atajos de teclado**: Siempre activos (1, 2, 3, ESC)

### Gestión de Sesión

#### Estadísticas en Tiempo Real
- **Contadores individuales**: Por tipo de estímulo
- **Total de sesión**: Suma de todos los estímulos
- **Cronómetro**: Tiempo transcurrido desde inicio

#### Exportación de Datos
- **Formato**: CSV compatible con Excel/análisis estadístico
- **Contenido**: Timestamp, tipo, duración, imagen, notas
- **Nomenclatura**: `registro_estimulos_YYYYMMDD_HHMMSS.csv`

#### Reinicio de Sesión
- **Función**: Guarda datos actuales y reinicia contadores
- **Seguridad**: Solicita confirmación antes de proceder
- **Backup**: Exporta automáticamente antes de reiniciar

## 📊 Formato de Datos de Salida

### Estructura del CSV
```csv
timestamp,type,exposure_time_ms,image_shown,notes
"2024-09-28 14:30:45.123","Olfativo","","",""
"2024-09-28 14:31:02.456","Visual","5000","imagen1.jpg",""
"2024-09-28 14:31:15.789","Haptico","","",""
```

### Descripción de Campos
- **timestamp**: Fecha y hora exacta (YYYY-MM-DD HH:MM:SS.mmm)
- **type**: Tipo de estímulo (Olfativo, Haptico, Visual)
- **exposure_time_ms**: Duración en milisegundos (solo Visual)
- **image_shown**: Nombre del archivo de imagen (solo Visual)
- **notes**: Campo reservado para anotaciones futuras

## 🎨 Personalización

### Agregar Nuevas Imágenes
1. Colocar archivos en `assets/images/`
2. Formatos soportados: PNG, JPG, JPEG, GIF, BMP
3. Actualizar lista en `app.js` (función `loadImages()`)

### Modificar Colores/Tema
- Editar variables CSS en `style.css`
- Colores principales definidos como gradientes
- Responsivo: breakpoints en 768px y 480px

### Agregar Nuevos Tipos de Estímulos
1. Añadir botón en HTML
2. Implementar handler en JavaScript
3. Actualizar estadísticas y contadores
4. Definir estilos CSS correspondientes

## 🔧 Solución de Problemas

### Las imágenes no cargan
- **Causa**: Política CORS del navegador
- **Solución**: Usar servidor web local (no abrir archivo directamente)

### Los sonidos no funcionan
- **Causa**: Política de autoplay del navegador
- **Solución**: Interactuar con la página antes (es normal)

### El CSV no se descarga
- **Causa**: Bloqueador de descargas
- **Solución**: Permitir descargas en configuración del navegador

### Rendimiento lento
- **Causa**: Muchas entradas en log
- **Solución**: Usar botón "Limpiar Log" periódicamente

## 🌐 Compatibilidad

### Navegadores Soportados
- ✅ Chrome 70+
- ✅ Firefox 65+
- ✅ Safari 12+
- ✅ Edge 79+

### Características Utilizadas
- ES6+ JavaScript
- CSS Grid y Flexbox
- Web Audio API (opcional)
- Blob API (para descarga CSV)
- Local Storage (futuro)

## 📝 Notas de Desarrollo

### Arquitectura
- **Patrón**: Clase principal `StimulusLogger`
- **Eventos**: Event listeners para toda la interacción
- **Estado**: Manejo local sin dependencias externas
- **Performance**: Optimizado para sesiones largas

### Seguridad
- **XSS**: HTML escapado en logs
- **CORS**: Funcionamiento offline completo
- **Privacidad**: Sin telemetría ni tracking

## 🤝 Contribuciones

Para mejoras o reportar problemas:
1. Documentar el problema específico
2. Incluir navegador y versión
3. Proporcionar pasos para reproducir
4. Sugerir solución si es posible

## 📄 Licencia

Sistema desarrollado para uso académico y profesional en investigación sensorial.

---

**Sensashot PRO** - Sistema Profesional de Registro de Estímulos
*Versión Web 1.0*