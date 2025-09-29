# 🚀 Guía de Instalación Rápida - Sensashot PRO Web

Esta guía te ayudará a tener el sistema funcionando en menos de 5 minutos.

## ⚡ Instalación Express (Recomendada)

### 1. Descargar Python (si no lo tienes)
- Ir a [python.org](https://python.org/downloads/)
- Descargar e instalar Python 3.x
- **Importante**: Marcar "Add Python to PATH" durante instalación

### 2. Ejecutar el Sistema
```bash
# 1. Abrir terminal/símbolo del sistema
# 2. Navegar a la carpeta del proyecto
cd ruta/a/tu/proyecto/stimulus_logger/web_interface

# 3. Iniciar servidor
python -m http.server 8000

# 4. Abrir navegador en:
http://localhost:8000
```

¡Listo! El sistema ya está funcionando.

## 🖥️ Otras Opciones de Instalación

### Opción A: Node.js
```bash
# Instalar Node.js desde nodejs.org
npm install -g http-server
cd stimulus_logger/web_interface
http-server -p 8000
```

### Opción B: VS Code (Más fácil)
1. Instalar VS Code
2. Instalar extensión "Live Server"
3. Abrir carpeta `web_interface`
4. Clic derecho en `index.html` → "Open with Live Server"

### Opción C: XAMPP/WAMP (Windows)
1. Instalar XAMPP
2. Copiar carpeta `web_interface` a `htdocs`
3. Iniciar Apache
4. Ir a `http://localhost/web_interface`

## 🎯 Verificación de Funcionamiento

### ✅ Checklist Post-Instalación
- [ ] La página carga sin errores
- [ ] Los botones responden al click
- [ ] Las estadísticas se actualizan
- [ ] El log muestra mensajes
- [ ] Las teclas 1, 2, 3 funcionan
- [ ] Se puede exportar CSV
- [ ] Las imágenes cargan (estímulo visual)

### 🔧 Si algo no funciona:

#### Problema: "ERR_FILE_NOT_FOUND"
**Solución**: Usar servidor web, no abrir archivo directamente.

#### Problema: Las imágenes no cargan
**Solución**: Verificar que las imágenes están en `assets/images/`

#### Problema: No se descarga el CSV
**Solución**: Permitir descargas en el navegador

## 📱 Uso en Dispositivos Móviles

### Configuración WiFi Local
```bash
# En lugar de localhost, usar IP local
python -m http.server 8000

# Encontrar tu IP:
# Windows: ipconfig
# Mac/Linux: ifconfig

# Acceder desde móvil:
http://192.168.1.XXX:8000
```

## 🌐 Instalación en Red Local

### Para Múltiples Computadoras
1. Instalar en una computadora "servidor"
2. Otros dispositivos acceden vía IP local
3. Ideal para estudios con múltiples investigadores

### Configuración Servidor
```bash
# Permitir acceso desde cualquier IP
python -m http.server 8000 --bind 0.0.0.0

# Acceso desde red:
http://IP-DEL-SERVIDOR:8000
```

## 🔒 Consideraciones de Seguridad

### Uso en Red Institucional
- El sistema funciona completamente offline
- No envía datos a internet
- Todos los datos se quedan en el dispositivo local
- Cumple con protocolos de privacidad

### Backup de Datos
- Los CSV se descargan automáticamente
- Hacer backup regular de la carpeta del proyecto
- Los datos se almacenan solo mientras el navegador esté abierto

## 🎨 Personalización Rápida

### Cambiar Imágenes de Estímulos
1. Ir a `assets/images/`
2. Reemplazar archivos existentes
3. Mantener los mismos nombres de archivo
4. O editar lista en `app.js` línea ~200

### Modificar Tiempos Default
En `app.js`, cambiar:
```javascript
// Línea ~15
exposureTime: tk.IntVar(value=5000)  // Cambiar 5000 por valor deseado
```

## ⚡ Solución de Problemas Rápidos

### Error: "Python no se reconoce"
```bash
# Windows: Reinstalar Python marcando "Add to PATH"
# O usar ruta completa:
C:\Python39\python.exe -m http.server 8000
```

### Error: "Puerto en uso"
```bash
# Cambiar puerto:
python -m http.server 8080
# Acceder en: http://localhost:8080
```

### Rendimiento Lento
- Cerrar otras pestañas del navegador
- Usar modo incógnito
- Limpiar log periódicamente

## 📞 Soporte Técnico

### Para Asistencia:
1. **Error específico**: Anotar mensaje exacto
2. **Navegador**: Chrome/Firefox/Safari + versión
3. **Sistema**: Windows/Mac/Linux
4. **Pasos**: Qué se estaba haciendo cuando falló

### Logs de Depuración:
- Abrir Developer Tools (F12)
- Ir a Console
- Copiar mensajes de error

---

## 🎉 ¡Ya está listo!

Una vez funcionando, el sistema es completamente autónomo:
- ✅ Interfaz intuitiva y profesional
- ✅ Registro preciso de timestamps
- ✅ Exportación automática de datos
- ✅ Compatible con análisis estadístico
- ✅ Ideal para producción

**¿Tienes preguntas?** Consulta el `README.md` completo para funcionalidades avanzadas.