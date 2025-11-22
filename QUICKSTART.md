# 🚀 Guía Rápida de Inicio

## Instalación en 3 Pasos

### 1️⃣ Configurar Entorno

**Windows:**
```powershell
# Ejecutar script de instalación
.\setup.bat
```

**Linux/Mac:**
```bash
# Dar permisos y ejecutar
chmod +x setup.sh
./setup.sh
```

**O manualmente:**
```powershell
# Crear entorno virtual
python -m venv venv

# Activar (Windows)
venv\Scripts\activate

# Activar (Linux/Mac)
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

### 2️⃣ Configurar OpenAI API Key

1. Copia el archivo de ejemplo:
   ```powershell
   copy .env.example .env
   ```

2. Edita `.env` y agrega tu API key:
   ```env
   OPENAI_API_KEY=sk-tu-api-key-aqui
   OPENAI_MODEL=gpt-4o-mini
   ```

3. Obtén tu API key en: https://platform.openai.com/api-keys

### 3️⃣ Ejecutar la Aplicación

```powershell
python main.py
```

Abre tu navegador en: **http://localhost:8000**

---

## 🎯 Uso Rápido

### Paso 1: Cargar Documentos
- Arrastra archivos PDF, DOCX o TXT
- O haz clic en "Seleccionar Archivos"
- Click en "Subir y Procesar Documentos"

### Paso 2: Hacer Preguntas
- Escribe tu pregunta en el chat
- Presiona Enter o "Enviar"
- Revisa la respuesta y las fuentes

### Paso 3: Análisis
- Verifica las fuentes citadas
- Revisa el nivel de confianza
- Continúa la conversación

---

## 📄 Documento de Prueba

Incluimos un contrato de ejemplo: `ejemplo_contrato.txt`

**Preguntas sugeridas:**
1. ¿Cuál es el objeto del contrato?
2. ¿Cuánto dura el contrato?
3. ¿Cuál es el valor mensual?
4. ¿Cuáles son las obligaciones del contratista?
5. ¿De quién es la propiedad intelectual?

---

## 🌐 Despliegue en Internet

### Opción 1: Render.com (Gratis)

1. Sube el código a GitHub
2. Crea cuenta en https://render.com
3. New Web Service → Conecta tu repo
4. Configura:
   - Build: `pip install -r requirements.txt`
   - Start: `uvicorn main:app --host 0.0.0.0 --port $PORT`
5. Agrega `OPENAI_API_KEY` en Environment
6. Deploy

Ver guía completa: `DEPLOYMENT.md`

---

## ⚙️ Configuración Avanzada

### Cambiar Modelo de IA
Edita `.env`:
```env
OPENAI_MODEL=gpt-4  # Más potente (más caro)
OPENAI_MODEL=gpt-4o-mini  # Balance precio/calidad
```

### Ajustar Tamaño de Chunks
Edita `rag_system.py` línea 65:
```python
chunk_size=1000,  # Aumentar para textos más largos
chunk_overlap=200,  # Aumentar para mejor contexto
```

### Cambiar Puerto
Edita `.env`:
```env
PORT=3000
```

---

## 🔍 Verificación

### Test de Salud
```powershell
curl http://localhost:8000/api/health
```

Respuesta esperada:
```json
{
  "status": "healthy",
  "model": "gpt-4o-mini",
  "documents_loaded": 0
}
```

---

## ❗ Solución de Problemas

### Error: "OPENAI_API_KEY no encontrada"
✅ Verifica que `.env` existe y tiene la API key correcta

### Error: "Module not found"
✅ Activa el entorno virtual: `venv\Scripts\activate`
✅ Reinstala: `pip install -r requirements.txt`

### Error al cargar PDF
✅ Verifica que el PDF tiene texto extraíble (no imagen)
✅ Prueba con el archivo `ejemplo_contrato.txt` incluido

### App muy lenta
✅ Reduce `chunk_size` en `rag_system.py`
✅ Verifica tu plan de OpenAI (rate limits)

---

## 📊 Estructura del Proyecto

```
hack-kognia-rag-legal/
├── main.py              # API FastAPI
├── rag_system.py        # Sistema RAG (LangChain + FAISS)
├── requirements.txt     # Dependencias Python
├── .env.example         # Plantilla de configuración
├── Procfile            # Configuración para deploy
├── static/
│   ├── index.html      # Interfaz web
│   ├── app.js          # Lógica frontend
│   └── styles.css      # Estilos
├── README.md           # Documentación completa
├── DEPLOYMENT.md       # Guía de despliegue
├── TESTING.md          # Guía de testing
└── ejemplo_contrato.txt # Documento de prueba
```

---

## 🎓 Recursos

- **Documentación LangChain**: https://python.langchain.com
- **OpenAI API**: https://platform.openai.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **FAISS**: https://github.com/facebookresearch/faiss

---

## 📞 Soporte

¿Problemas? Revisa:
1. ✅ `.env` configurado correctamente
2. ✅ Entorno virtual activado
3. ✅ Todas las dependencias instaladas
4. ✅ Puerto 8000 disponible
5. ✅ API key de OpenAI válida

---

## 📝 Checklist

- [ ] Python 3.9+ instalado
- [ ] Entorno virtual creado
- [ ] Dependencias instaladas
- [ ] Archivo `.env` configurado
- [ ] OpenAI API key válida
- [ ] Aplicación corriendo en localhost:8000
- [ ] Documento de prueba cargado
- [ ] Primera consulta exitosa

---

**¡Listo para usar! 🎉**

Para más información: `README.md` | `DEPLOYMENT.md` | `TESTING.md`
