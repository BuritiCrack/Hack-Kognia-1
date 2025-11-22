# ⚖️ Asistente Legal Inteligente - RAG System

Sistema de Recuperación Aumentada por Generación (RAG) para consultas inteligentes sobre documentos legales, desarrollado para Hack Kognia 1.0.

## 🎯 Características

- **Carga múltiple de documentos**: Soporta PDF, DOCX y TXT
- **Procesamiento inteligente**: Divide documentos en fragmentos y crea embeddings vectoriales
- **Búsqueda semántica**: Utiliza FAISS para búsqueda eficiente de información relevante
- **Respuestas contextualizadas**: GPT-4o-mini genera respuestas basadas en los documentos
- **Interfaz tipo chat**: Interfaz web moderna y responsive
- **Transparencia**: Muestra fuentes y nivel de confianza de cada respuesta

## 🏗️ Arquitectura

### Backend
- **FastAPI**: API REST de alto rendimiento
- **LangChain**: Framework para aplicaciones LLM
- **FAISS**: Base de datos vectorial para búsqueda semántica
- **OpenAI**: GPT-4o-mini para generación de respuestas

### Frontend
- **HTML5/CSS3**: Interfaz moderna y responsive
- **JavaScript Vanilla**: Sin dependencias, código limpio y eficiente

### Procesamiento
1. **Carga**: Recepción de documentos PDF/DOCX/TXT
2. **Extracción**: Parsing y extracción de texto
3. **Segmentación**: División en chunks de ~1000 caracteres
4. **Vectorización**: Creación de embeddings con OpenAI
5. **Indexación**: Almacenamiento en FAISS
6. **Consulta**: Recuperación de fragmentos relevantes
7. **Generación**: Respuesta contextualizada con GPT-4o-mini

## 🚀 Instalación Local

### Requisitos Previos
- Python 3.9 o superior
- Cuenta de OpenAI con API key

### Pasos

1. **Clonar el repositorio**
```bash
git clone https://github.com/AndresFGutierrez/hack-kognia-rag-legal.git
cd hack-kognia-rag-legal
```

2. **Crear entorno virtual**
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar variables de entorno**
```bash
# Copiar archivo de ejemplo
copy .env.example .env

# Editar .env y agregar tu API key de OpenAI
OPENAI_API_KEY=tu_api_key_aqui
```

5. **Ejecutar la aplicación**
```bash
python main.py
```

6. **Acceder a la aplicación**
```
http://localhost:8000
```

## 📦 Despliegue en Producción

### Render.com (Recomendado)

1. **Crear cuenta en Render.com**
2. **Conectar repositorio de GitHub**
3. **Configurar Web Service**:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`
4. **Agregar variables de entorno**:
   - `OPENAI_API_KEY`: Tu API key de OpenAI
5. **Deploy**

### Railway.app

1. **Crear cuenta en Railway.app**
2. **New Project → Deploy from GitHub**
3. **Agregar variables de entorno**:
   - `OPENAI_API_KEY`: Tu API key de OpenAI
4. **Deploy automático**

### Vercel (Solo Frontend)

Para frontend estático, puedes usar Vercel y un backend separado.

## 📚 Uso

### 1. Cargar Documentos
- Arrastra archivos o haz clic en "Seleccionar Archivos"
- Formatos: PDF, DOCX, TXT
- Puedes cargar múltiples documentos

### 2. Realizar Consultas
- Escribe tu pregunta en lenguaje natural
- Presiona Enter o haz clic en "Enviar"
- El sistema buscará en los documentos y generará una respuesta

### 3. Revisar Respuestas
- Lee la respuesta generada
- Revisa las fuentes citadas
- Verifica el nivel de confianza

### 4. Reiniciar Sistema
- Haz clic en "Reiniciar" para limpiar documentos
- Carga nuevos documentos para empezar de nuevo

## 🔧 API Endpoints

### GET `/`
Sirve la interfaz web principal

### GET `/api/health`
Verifica el estado del sistema
```json
{
  "status": "healthy",
  "model": "gpt-4o-mini",
  "documents_loaded": 3
}
```

### POST `/api/upload`
Carga y procesa documentos
- **Input**: Multipart form data con archivos
- **Output**: Confirmación y número de documentos cargados

### POST `/api/query`
Realiza una consulta
- **Input**: `{"question": "¿Qué dice sobre...?"}`
- **Output**: Respuesta con fuentes y confianza

### POST `/api/reset`
Reinicia el sistema
- **Output**: Confirmación de reinicio

### GET `/api/status`
Obtiene estado del sistema
- **Output**: Estado y documentos cargados

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Backend Framework | FastAPI | 0.109.0 |
| LLM Framework | LangChain | 0.1.4 |
| Vector Store | FAISS | 1.7.4 |
| LLM | OpenAI GPT-4o-mini | API |
| Embeddings | OpenAI text-embedding-3-small | API |
| PDF Processing | pypdf | 4.0.1 |
| DOCX Processing | python-docx | 1.1.0 |
| Server | Uvicorn | 0.27.0 |

## 📝 Configuración Avanzada

### Cambiar Modelo LLM
Edita `.env`:
```env
OPENAI_MODEL=gpt-4  # Más potente pero más costoso
```

### Ajustar Chunking
Edita `rag_system.py`:
```python
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1500,  # Aumentar para chunks más grandes
    chunk_overlap=300,
)
```

### Cambiar Número de Fuentes
Edita `rag_system.py`:
```python
retriever=self.vector_store.as_retriever(
    search_kwargs={"k": 6}  # Recuperar más fragmentos
)
```

## 🔒 Seguridad

- **API Keys**: Nunca commits tu `.env` al repositorio
- **CORS**: Configurado para desarrollo, ajustar en producción
- **Rate Limiting**: Considera implementar para producción
- **Validación**: Los archivos son validados antes de procesarse

## 📊 Limitaciones Conocidas

- Máximo tamaño de archivo: ~50MB por limitaciones de memoria
- Idioma: Optimizado para español, funciona con otros idiomas
- Costo: Cada consulta consume tokens de OpenAI
- Persistencia: Los documentos se pierden al reiniciar (sin DB permanente)

## 🤝 Contribuciones

Este es un proyecto para Hack Kognia 1.0. Sugerencias y mejoras son bienvenidas.

## 📄 Licencia

MIT License - Ver archivo LICENSE para más detalles

## 👥 Autor

Desarrollado para Hack Kognia 1.0

## 🙏 Agradecimientos

- Talento Tech por la organización del hackathon
- OpenAI por las APIs de LLM
- LangChain por el framework RAG
- La comunidad open source

## 📞 Soporte

Para problemas o preguntas:
1. Revisa la documentación
2. Verifica la configuración de variables de entorno
3. Consulta los logs de error
4. Abre un issue en GitHub

---

**Hack Kognia 1.0** - Asistente Legal Inteligente RAG
