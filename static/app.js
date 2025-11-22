// Estado de la aplicación
const state = {
    selectedFiles: [],
    documentsLoaded: false
};

// Elementos del DOM
const elements = {
    fileInput: document.getElementById('fileInput'),
    selectFilesBtn: document.getElementById('selectFilesBtn'),
    uploadArea: document.getElementById('uploadArea'),
    filesList: document.getElementById('filesList'),
    uploadBtn: document.getElementById('uploadBtn'),
    chatMessages: document.getElementById('chatMessages'),
    questionInput: document.getElementById('questionInput'),
    sendBtn: document.getElementById('sendBtn'),
    resetBtn: document.getElementById('resetBtn'),
    statusText: document.getElementById('statusText'),
    statusDot: document.getElementById('statusDot'),
    loadingOverlay: document.getElementById('loadingOverlay'),
    loadingText: document.getElementById('loadingText')
};

// Inicialización
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    checkSystemStatus();
});

// Event Listeners
function initializeEventListeners() {
    // File input
    elements.selectFilesBtn.addEventListener('click', () => elements.fileInput.click());
    elements.fileInput.addEventListener('change', handleFileSelect);
    
    // Drag and drop
    elements.uploadArea.addEventListener('dragover', handleDragOver);
    elements.uploadArea.addEventListener('dragleave', handleDragLeave);
    elements.uploadArea.addEventListener('drop', handleDrop);
    elements.uploadArea.addEventListener('click', () => elements.fileInput.click());
    
    // Upload button
    elements.uploadBtn.addEventListener('click', uploadDocuments);
    
    // Chat input
    elements.questionInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendQuestion();
        }
    });
    elements.sendBtn.addEventListener('click', sendQuestion);
    
    // Reset button
    elements.resetBtn.addEventListener('click', resetSystem);
}

// File handling
function handleFileSelect(e) {
    const files = Array.from(e.target.files);
    addFiles(files);
}

function handleDragOver(e) {
    e.preventDefault();
    elements.uploadArea.classList.add('dragover');
}

function handleDragLeave(e) {
    e.preventDefault();
    elements.uploadArea.classList.remove('dragover');
}

function handleDrop(e) {
    e.preventDefault();
    elements.uploadArea.classList.remove('dragover');
    
    const files = Array.from(e.dataTransfer.files);
    addFiles(files);
}

function addFiles(files) {
    const validExtensions = ['.pdf', '.docx', '.txt'];
    const newFiles = files.filter(file => {
        const ext = '.' + file.name.split('.').pop().toLowerCase();
        return validExtensions.includes(ext);
    });
    
    state.selectedFiles = [...state.selectedFiles, ...newFiles];
    updateFilesList();
    elements.uploadBtn.disabled = state.selectedFiles.length === 0;
}

function removeFile(index) {
    state.selectedFiles.splice(index, 1);
    updateFilesList();
    elements.uploadBtn.disabled = state.selectedFiles.length === 0;
}

function updateFilesList() {
    if (state.selectedFiles.length === 0) {
        elements.filesList.innerHTML = '';
        return;
    }
    
    elements.filesList.innerHTML = state.selectedFiles.map((file, index) => `
        <div class="file-item">
            <span class="file-name">📄 ${file.name}</span>
            <button class="remove-btn" onclick="removeFile(${index})">×</button>
        </div>
    `).join('');
}

// Upload documents
async function uploadDocuments() {
    if (state.selectedFiles.length === 0) return;
    
    const formData = new FormData();
    state.selectedFiles.forEach(file => {
        formData.append('files', file);
    });
    
    showLoading('Procesando documentos...');
    
    try {
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification(`✅ ${data.message}`, 'success');
            state.selectedFiles = [];
            updateFilesList();
            elements.uploadBtn.disabled = true;
            await checkSystemStatus();
            
            // Limpiar mensajes de bienvenida
            const welcomeMsg = elements.chatMessages.querySelector('.welcome-message');
            if (welcomeMsg) {
                welcomeMsg.remove();
            }
        } else {
            showNotification(`❌ Error: ${data.detail}`, 'error');
        }
    } catch (error) {
        showNotification('❌ Error de conexión con el servidor', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Check system status
async function checkSystemStatus() {
    try {
        const response = await fetch('/api/status');
        const data = await response.json();
        
        if (data.status === 'ready') {
            state.documentsLoaded = true;
            elements.statusText.textContent = data.message;
            elements.statusDot.classList.add('active');
            elements.questionInput.disabled = false;
            elements.sendBtn.disabled = false;
        } else {
            state.documentsLoaded = false;
            elements.statusText.textContent = data.message;
            elements.statusDot.classList.remove('active');
            elements.questionInput.disabled = true;
            elements.sendBtn.disabled = true;
        }
    } catch (error) {
        console.error('Error checking status:', error);
    }
}

// Send question
async function sendQuestion() {
    const question = elements.questionInput.value.trim();
    
    if (!question || !state.documentsLoaded) return;
    
    // Add user message
    addMessage(question, 'user');
    elements.questionInput.value = '';
    elements.questionInput.disabled = true;
    elements.sendBtn.disabled = true;
    
    showLoading('Buscando respuesta...');
    
    try {
        const response = await fetch('/api/query', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ question })
        });
        
        const data = await response.json();
        
        if (response.ok) {
            addMessage(data.answer, 'assistant', data.sources, data.confidence);
        } else {
            addMessage(`Error: ${data.detail}`, 'assistant');
        }
    } catch (error) {
        addMessage('Error de conexión con el servidor', 'assistant');
        console.error('Error:', error);
    } finally {
        hideLoading();
        elements.questionInput.disabled = false;
        elements.sendBtn.disabled = false;
        elements.questionInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender, sources = null, confidence = null) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message message-${sender}`;
    
    // Convertir markdown básico a HTML
    let formattedText = text
        .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')  // Bold
        .replace(/---/g, '<hr style="margin: 10px 0; border: none; border-top: 1px solid #e0e0e0;">')  // Separadores
        .replace(/\n\n/g, '</p><p>')  // Párrafos
        .replace(/\n/g, '<br>');  // Saltos de línea
    
    formattedText = `<p>${formattedText}</p>`;
    
    let sourcesHTML = '';
    if (sources && sources.length > 0) {
        sourcesHTML = `
            <div class="message-sources">
                <h4>📚 Fuentes consultadas (${sources.length} fragmentos):</h4>
                ${sources.slice(0, 3).map((source, index) => `
                    <div class="source-item">
                        <div class="source-filename">
                            📄 ${source.filename} - Fragmento ${source.chunk + 1}
                            <span class="source-score">(Similitud: ${(1 - source.score).toFixed(2)}${source.keyword_score ? ` | Palabras clave: ${Math.floor(source.keyword_score)}` : ''})</span>
                        </div>
                        <div class="source-content">"${truncateText(source.content, 150)}"</div>
                    </div>
                `).join('')}
                ${confidence ? `
                    <div class="confidence-badge confidence-${confidence.toLowerCase()}">
                        Confianza: ${confidence}
                    </div>
                ` : ''}
            </div>
        `;
    }
    
    messageDiv.innerHTML = `
        <div class="message-bubble">${formattedText}</div>
        ${sourcesHTML}
    `;
    
    elements.chatMessages.appendChild(messageDiv);
    elements.chatMessages.scrollTop = elements.chatMessages.scrollHeight;
}

// Reset system
async function resetSystem() {
    if (!confirm('¿Estás seguro de reiniciar el sistema? Se eliminarán todos los documentos cargados.')) {
        return;
    }
    
    showLoading('Reiniciando sistema...');
    
    try {
        const response = await fetch('/api/reset', {
            method: 'POST'
        });
        
        const data = await response.json();
        
        if (response.ok) {
            showNotification('✅ Sistema reiniciado exitosamente', 'success');
            
            // Reset UI
            elements.chatMessages.innerHTML = `
                <div class="welcome-message">
                    <p>👋 Sistema reiniciado</p>
                    <p>Carga nuevos documentos para comenzar.</p>
                </div>
            `;
            
            state.selectedFiles = [];
            updateFilesList();
            await checkSystemStatus();
        } else {
            showNotification(`❌ Error: ${data.detail}`, 'error');
        }
    } catch (error) {
        showNotification('❌ Error de conexión con el servidor', 'error');
        console.error('Error:', error);
    } finally {
        hideLoading();
    }
}

// Utility functions
function showLoading(text) {
    elements.loadingText.textContent = text;
    elements.loadingOverlay.classList.add('active');
}

function hideLoading() {
    elements.loadingOverlay.classList.remove('active');
}

function showNotification(message, type) {
    // Simple notification - you can enhance this
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        padding: 15px 20px;
        background: ${type === 'success' ? '#10b981' : '#ef4444'};
        color: white;
        border-radius: 8px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        z-index: 2000;
        animation: slideIn 0.3s ease;
    `;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.style.animation = 'slideOut 0.3s ease';
        setTimeout(() => notification.remove(), 300);
    }, 3000);
}

function truncateText(text, maxLength) {
    if (text.length <= maxLength) return text;
    return text.substring(0, maxLength) + '...';
}

// Make removeFile available globally
window.removeFile = removeFile;
