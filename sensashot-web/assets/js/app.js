// Sensashot PRO - Stimulus Timing System
class StimulusLogger {
    constructor() {
        this.stimuliLog = [];
        this.sessionStartTime = new Date();
        this.availableImages = [];
        this.usedImages = [];
        this.sessionTimer = null;

        this.counters = {
            olfactory: 0,
            haptic: 0,
            visual: 0,
            total: 0
        };

        this.init();
    }

    init() {
        this.setupEventListeners();
        this.startSessionTimer();
        this.loadImages();
        this.updateExposureTimeDisplay();
        this.logMessage('Sistema iniciado - Listo para registrar estímulos', 'system');
    }

    setupEventListeners() {
        // Stimulus buttons
        document.getElementById('olfactoryBtn').addEventListener('click', () => this.logStimulus('olfactory'));
        document.getElementById('hapticBtn').addEventListener('click', () => this.logStimulus('haptic'));
        document.getElementById('visualBtn').addEventListener('click', () => this.logVisualStimulus());

        // Configuration controls
        const exposureTimeSlider = document.getElementById('exposureTime');
        exposureTimeSlider.addEventListener('input', () => this.updateExposureTimeDisplay());

        // Session controls
        document.getElementById('resetBtn').addEventListener('click', () => this.resetSession());
        document.getElementById('exportBtn').addEventListener('click', () => this.exportData());

        // Log controls
        document.getElementById('clearLogBtn').addEventListener('click', () => this.clearLog());

        // Instructions toggle
        document.getElementById('toggleInstructions').addEventListener('click', () => this.toggleInstructions());

        // Visual modal close
        document.getElementById('visualModal').addEventListener('click', () => this.closeVisualModal());

        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => this.handleKeyboardShortcuts(e));

        // Prevent context menu on stimulus buttons for better UX
        document.querySelectorAll('.stimulus-btn').forEach(btn => {
            btn.addEventListener('contextmenu', (e) => e.preventDefault());
        });
    }

    handleKeyboardShortcuts(e) {
        // Only trigger if not typing in an input
        if (e.target.tagName === 'INPUT') return;

        switch(e.key) {
            case '1':
                e.preventDefault();
                this.logStimulus('olfactory');
                break;
            case '2':
                e.preventDefault();
                this.logStimulus('haptic');
                break;
            case '3':
                e.preventDefault();
                this.logVisualStimulus();
                break;
            case 'Escape':
                this.closeVisualModal();
                break;
        }
    }

    startSessionTimer() {
        this.sessionTimer = setInterval(() => {
            const now = new Date();
            const elapsed = now - this.sessionStartTime;
            const hours = Math.floor(elapsed / 3600000);
            const minutes = Math.floor((elapsed % 3600000) / 60000);
            const seconds = Math.floor((elapsed % 60000) / 1000);

            const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            document.getElementById('sessionTime').textContent = timeString;
        }, 1000);
    }

    logStimulus(type) {
        const timestamp = new Date();
        const timestampString = this.formatTimestamp(timestamp);

        const stimulusEntry = {
            timestamp: timestampString,
            type: this.capitalizeFirst(type),
            exposureTimeMs: null,
            imageShown: null,
            notes: ''
        };

        this.stimuliLog.push(stimulusEntry);
        this.counters[type]++;
        this.counters.total++;

        // Visual feedback
        this.animateButton(type);
        this.playFeedbackSound();

        // Log message
        this.logMessage(`ESTÍMULO ${type.toUpperCase()} registrado`, type);

        // Update UI
        this.updateStatistics();
        this.updateCounters();
    }

    logVisualStimulus() {
        const timestamp = new Date();
        const timestampString = this.formatTimestamp(timestamp);
        const exposureTime = parseInt(document.getElementById('exposureTime').value);
        const showImages = document.getElementById('showImages').checked;

        let imageShown = null;

        if (showImages) {
            imageShown = this.showRandomImage(exposureTime);
        }

        const stimulusEntry = {
            timestamp: timestampString,
            type: 'Visual',
            exposureTimeMs: exposureTime,
            imageShown: imageShown,
            notes: ''
        };

        this.stimuliLog.push(stimulusEntry);
        this.counters.visual++;
        this.counters.total++;

        // Visual feedback
        this.animateButton('visual');
        this.playFeedbackSound();

        // Log message
        const imageInfo = imageShown ? ` - Imagen: ${imageShown}` : '';
        this.logMessage(`ESTÍMULO VISUAL registrado (${exposureTime}ms)${imageInfo}`, 'visual');

        // Update UI
        this.updateStatistics();
        this.updateCounters();
    }

    showRandomImage(exposureTime) {
        if (this.availableImages.length === 0) {
            this.logMessage('No hay imágenes disponibles para mostrar', 'system');
            return null;
        }

        // Reset cycle if no images available
        if (this.availableImages.length === 0) {
            this.availableImages = [...this.usedImages];
            this.usedImages = [];
            this.logMessage(`Reiniciando ciclo de imágenes. Total: ${this.availableImages.length} imágenes`, 'system');
        }

        // Select random image
        const randomIndex = Math.floor(Math.random() * this.availableImages.length);
        const selectedImage = this.availableImages[randomIndex];

        // Move to used images
        this.availableImages.splice(randomIndex, 1);
        this.usedImages.push(selectedImage);

        const remaining = this.availableImages.length;
        this.logMessage(`Mostrando imagen: ${selectedImage} por ${exposureTime}ms (Quedan ${remaining})`, 'visual');

        // Display image
        this.displayImage(selectedImage, exposureTime);

        return selectedImage;
    }

    displayImage(imageName, exposureTime) {
        const modal = document.getElementById('visualModal');
        const img = document.getElementById('stimulusImage');

        // Set image source
        img.src = `assets/images/${imageName}`;
        img.onerror = () => {
            // Fallback to a placeholder or hide modal
            this.logMessage(`Error al cargar imagen: ${imageName}`, 'system');
            this.closeVisualModal();
        };

        // Show modal
        modal.classList.add('active');

        // Auto-close after exposure time
        setTimeout(() => {
            this.closeVisualModal();
        }, exposureTime);
    }

    closeVisualModal() {
        const modal = document.getElementById('visualModal');
        modal.classList.remove('active');
    }

    loadImages() {
        // Simulated image list - in a real implementation, this would load from the images directory
        const defaultImages = [
            'aura_bg.png',
            'design-a-wallpaper-for-a-biomedical-engineer--with.png',
            'dino-biomedical-engineer-cute-orange-in-his-lab-of.png',
            'logo_uniandes.PNG',
            'noBgBlack.png',
            'noBgColor.png',
            'noBgWhite.png',
            'vtp.jpg',
            'with_padding.png'
        ];

        this.availableImages = [...defaultImages];
        this.logMessage(`Cargadas ${this.availableImages.length} imágenes para estímulos visuales`, 'system');
    }

    animateButton(type) {
        const button = document.getElementById(`${type}Btn`);
        button.style.transform = 'scale(0.95)';

        setTimeout(() => {
            button.style.transform = '';
        }, 150);

        // Add pulse effect
        button.classList.add('pulse');
        setTimeout(() => {
            button.classList.remove('pulse');
        }, 600);
    }

    playFeedbackSound() {
        if (!document.getElementById('soundFeedback').checked) return;

        // Create a simple beep sound using Web Audio API
        try {
            const audioContext = new (window.AudioContext || window.webkitAudioContext)();
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();

            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);

            oscillator.frequency.setValueAtTime(800, audioContext.currentTime);
            oscillator.type = 'sine';

            gainNode.gain.setValueAtTime(0, audioContext.currentTime);
            gainNode.gain.linearRampToValueAtTime(0.1, audioContext.currentTime + 0.01);
            gainNode.gain.exponentialRampToValueAtTime(0.001, audioContext.currentTime + 0.1);

            oscillator.start(audioContext.currentTime);
            oscillator.stop(audioContext.currentTime + 0.1);
        } catch (e) {
            console.log('Audio feedback not available');
        }
    }

    updateExposureTimeDisplay() {
        const value = document.getElementById('exposureTime').value;
        const seconds = (value / 1000).toFixed(1);
        document.getElementById('exposureValue').textContent = `${seconds}s`;
    }

    updateStatistics() {
        document.getElementById('olfactoryTotal').textContent = this.counters.olfactory;
        document.getElementById('hapticTotal').textContent = this.counters.haptic;
        document.getElementById('visualTotal').textContent = this.counters.visual;
        document.getElementById('sessionTotal').textContent = this.counters.total;
    }

    updateCounters() {
        document.getElementById('olfactoryCounter').textContent = this.counters.olfactory;
        document.getElementById('hapticCounter').textContent = this.counters.haptic;
        document.getElementById('visualCounter').textContent = this.counters.visual;
        document.getElementById('totalStimuli').textContent = this.counters.total;
    }

    logMessage(message, type = 'system') {
        const logContainer = document.getElementById('activityLog');
        const timestamp = this.formatTimeOnly(new Date());

        const logEntry = document.createElement('div');
        logEntry.className = `log-entry ${type}`;
        logEntry.innerHTML = `<span class="timestamp">[${timestamp}]</span><span class="message">${message}</span>`;

        logContainer.appendChild(logEntry);
        logContainer.scrollTop = logContainer.scrollHeight;

        // Limit log entries to prevent performance issues
        const entries = logContainer.children;
        if (entries.length > 100) {
            logContainer.removeChild(entries[0]);
        }
    }

    clearLog() {
        const logContainer = document.getElementById('activityLog');
        logContainer.innerHTML = '';
        this.logMessage('Log de actividad limpiado', 'system');
    }

    toggleInstructions() {
        const panel = document.querySelector('.instructions-panel .panel-content');
        const button = document.getElementById('toggleInstructions');
        const icon = button.querySelector('i');

        if (panel.style.display === 'none') {
            panel.style.display = 'block';
            icon.className = 'fas fa-chevron-up';
        } else {
            panel.style.display = 'none';
            icon.className = 'fas fa-chevron-down';
        }
    }

    resetSession() {
        if (this.stimuliLog.length === 0) {
            this.logMessage('No hay datos para reiniciar', 'system');
            return;
        }

        const confirmReset = confirm(`¿Desea reiniciar la sesión?\n\nSe perderán ${this.stimuliLog.length} registros no guardados.`);

        if (confirmReset) {
            // Export current data before reset
            this.exportData();

            // Reset all data
            this.stimuliLog = [];
            this.counters = { olfactory: 0, haptic: 0, visual: 0, total: 0 };
            this.availableImages = [...this.usedImages, ...this.availableImages];
            this.usedImages = [];
            this.sessionStartTime = new Date();

            // Update UI
            this.updateStatistics();
            this.updateCounters();
            this.clearLog();

            this.logMessage('Sesión reiniciada. Datos anteriores exportados.', 'system');
        }
    }

    exportData() {
        if (this.stimuliLog.length === 0) {
            alert('No hay datos para exportar');
            return;
        }

        const csv = this.generateCSV();
        const timestamp = this.formatFilename(new Date());
        const filename = `registro_estimulos_${timestamp}.csv`;

        this.downloadCSV(csv, filename);
        this.logMessage(`Datos exportados: ${this.stimuliLog.length} estímulos en ${filename}`, 'system');
    }

    generateCSV() {
        const headers = ['timestamp', 'type', 'exposure_time_ms', 'image_shown', 'notes'];
        const csvRows = [headers.join(',')];

        this.stimuliLog.forEach(entry => {
            const row = [
                `"${entry.timestamp}"`,
                `"${entry.type}"`,
                entry.exposureTimeMs || '',
                entry.imageShown ? `"${entry.imageShown}"` : '',
                `"${entry.notes}"`
            ];
            csvRows.push(row.join(','));
        });

        return csvRows.join('\n');
    }

    downloadCSV(content, filename) {
        const blob = new Blob([content], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');

        if (link.download !== undefined) {
            const url = URL.createObjectURL(blob);
            link.setAttribute('href', url);
            link.setAttribute('download', filename);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        } else {
            alert('Su navegador no soporta la descarga automática. Por favor copie los datos manualmente.');
        }
    }

    formatTimestamp(date) {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');
        const milliseconds = date.getMilliseconds().toString().padStart(3, '0');

        return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}.${milliseconds}`;
    }

    formatTimeOnly(date) {
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');
        const milliseconds = date.getMilliseconds().toString().padStart(3, '0');

        return `${hours}:${minutes}:${seconds}.${milliseconds}`;
    }

    formatFilename(date) {
        const year = date.getFullYear();
        const month = (date.getMonth() + 1).toString().padStart(2, '0');
        const day = date.getDate().toString().padStart(2, '0');
        const hours = date.getHours().toString().padStart(2, '0');
        const minutes = date.getMinutes().toString().padStart(2, '0');
        const seconds = date.getSeconds().toString().padStart(2, '0');

        return `${year}${month}${day}_${hours}${minutes}${seconds}`;
    }

    capitalizeFirst(str) {
        return str.charAt(0).toUpperCase() + str.slice(1);
    }
}

// CSS for pulse animation
const style = document.createElement('style');
style.textContent = `
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
        100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
    }
    .pulse {
        animation: pulse 0.6s;
    }
`;
document.head.appendChild(style);

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.stimulusLogger = new StimulusLogger();

    // Add keyboard shortcuts info to console
    console.log('Sensashot PRO - Atajos de teclado:');
    console.log('1 - Estímulo Olfativo');
    console.log('2 - Estímulo Háptico');
    console.log('3 - Estímulo Visual');
    console.log('ESC - Cerrar modal visual');
});