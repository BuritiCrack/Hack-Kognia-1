# 🏗️ Arquitectura del Sistema

## Diagrama de Flujo General

```
┌─────────────────────────────────────────────────────────────┐
│                      USUARIO FINAL                           │
│                    (Navegador Web)                           │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                   FRONTEND (Static)                          │
│  ┌─────────────┬──────────────┬──────────────────────────┐ │
│  │ index.html  │   app.js     │      styles.css          │ │
│  │             │              │                          │ │
│  │ • UI Layout │ • API Calls  │ • Responsive Design      │ │
│  │ • Chat      │ • File       │ • Modern Aesthetics      │ │
│  │   Interface │   Upload     │                          │ │
│  └─────────────┴──────────────┴──────────────────────────┘ │
└────────────────────┬────────────────────────────────────────┘
                     │ HTTP/REST API
                     ▼
┌─────────────────────────────────────────────────────────────┐
│                  BACKEND (FastAPI)                           │
│                       main.py                                │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  API Endpoints:                                      │  │
│  │  • POST /api/upload    - Cargar documentos          │  │
│  │  • POST /api/query     - Hacer consultas            │  │
│  │  • POST /api/reset     - Reiniciar sistema          │  │
│  │  • GET  /api/status    - Estado del sistema         │  │
│  │  • GET  /api/health    - Health check               │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────┬────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────────┐
│              SISTEMA RAG (rag_system.py)                     │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  DocumentProcessor                                   │  │
│  │  • extract_text_from_pdf()                          │  │
│  │  • extract_text_from_docx()                         │  │
│  │  • extract_text_from_txt()                          │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  RAGSystem                                           │  │
│  │  • add_documents()    - Procesar y vectorizar       │  │
│  │  • query()            - Buscar y generar respuesta  │  │
│  │  • reset()            - Limpiar sistema             │  │
│  └──────────────────────────────────────────────────────┘  │
└──────┬─────────────────────┬─────────────────────┬─────────┘
       │                     │                     │
       ▼                     ▼                     ▼
┌─────────────┐    ┌──────────────────┐    ┌─────────────────┐
│  LangChain  │    │  Vector Store    │    │   OpenAI API    │
│             │    │    (FAISS)       │    │                 │
│ • Text      │    │                  │    │ • GPT-4o-mini   │
│   Splitter  │    │ • Embeddings     │    │ • Embeddings    │
│ • Chains    │    │ • Similarity     │    │ • Chat          │
│ • Memory    │    │   Search         │    │   Completion    │
└─────────────┘    └──────────────────┘    └─────────────────┘
```

---

## Flujo de Procesamiento de Documentos

```
┌──────────────┐
│  Usuario     │
│  Sube PDF    │
└──────┬───────┘
       │
       ▼
┌────────────────────────────────────┐
│  1. Recepción (FastAPI)            │
│     • Validar formato              │
│     • Guardar temporalmente        │
└──────┬─────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  2. Extracción (DocumentProcessor) │
│     • pypdf.PdfReader              │
│     • Extraer texto                │
└──────┬─────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  3. Segmentación (LangChain)       │
│     • RecursiveCharacterSplitter   │
│     • Chunks de ~1000 chars        │
│     • Overlap de 200 chars         │
└──────┬─────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  4. Vectorización (OpenAI)         │
│     • text-embedding-3-small       │
│     • Vector de 1536 dimensiones   │
└──────┬─────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  5. Indexación (FAISS)             │
│     • Crear/actualizar index       │
│     • Guardar metadata             │
└──────┬─────────────────────────────┘
       │
       ▼
┌────────────────────────────────────┐
│  6. Confirmación                   │
│     • Respuesta al usuario         │
│     • Sistema listo para queries   │
└────────────────────────────────────┘
```

---

## Flujo de Consulta (Query)

```
┌──────────────────┐
│  Usuario hace    │
│  pregunta        │
└────────┬─────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  1. Recepción de Query (FastAPI)     │
│     • Validar pregunta               │
│     • Verificar documentos cargados  │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  2. Vectorizar Pregunta (OpenAI)     │
│     • Crear embedding de la pregunta │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  3. Búsqueda Semántica (FAISS)       │
│     • Similarity search              │
│     • Top K=4 fragmentos             │
│     • Calcular scores                │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  4. Preparar Contexto (LangChain)    │
│     • Fragmentos relevantes          │
│     • Historial de chat              │
│     • Metadata de fuentes            │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  5. Generar Respuesta (GPT-4o-mini)  │
│     • Prompt con contexto            │
│     • Temperature = 0 (preciso)      │
│     • Respuesta fundamentada         │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  6. Post-procesamiento               │
│     • Extraer fuentes                │
│     • Calcular confianza             │
│     • Formatear respuesta            │
└────────┬─────────────────────────────┘
         │
         ▼
┌──────────────────────────────────────┐
│  7. Respuesta al Usuario             │
│     • Respuesta generada             │
│     • Fuentes citadas                │
│     • Nivel de confianza             │
└──────────────────────────────────────┘
```

---

## Stack Tecnológico Detallado

### Backend
```
FastAPI (0.109.0)
├── uvicorn (servidor ASGI)
├── pydantic (validación de datos)
└── python-multipart (upload de archivos)
```

### RAG System
```
LangChain (0.1.4)
├── langchain-openai (integraciones)
├── langchain-community (utilidades)
└── ConversationalRetrievalChain
```

### Procesamiento
```
Documentos
├── pypdf (PDFs)
├── python-docx (DOCX)
└── tiktoken (tokenización)
```

### Vector Store
```
FAISS (1.7.4)
├── CPU version
├── Similarity search
└── Index persistence
```

### IA
```
OpenAI API
├── GPT-4o-mini (LLM)
└── text-embedding-3-small (embeddings)
```

### Frontend
```
Vanilla Stack
├── HTML5 (estructura)
├── CSS3 (estilos)
└── JavaScript ES6+ (lógica)
```

---

## Modelo de Datos

### Document
```python
{
    "page_content": str,      # Texto del fragmento
    "metadata": {
        "filename": str,      # Nombre del archivo
        "chunk": int,         # Número de fragmento
        "source": str         # Ruta del archivo
    }
}
```

### Query Request
```python
{
    "question": str          # Pregunta del usuario
}
```

### Query Response
```python
{
    "answer": str,           # Respuesta generada
    "sources": [             # Lista de fuentes
        {
            "content": str,  # Texto del fragmento
            "filename": str, # Archivo origen
            "chunk": int     # Número de fragmento
        }
    ],
    "confidence": str        # "Alta", "Media", "Baja"
}
```

---

## Configuración de Parámetros

### Text Splitting
```python
chunk_size = 1000         # Tamaño de cada fragmento
chunk_overlap = 200       # Solapamiento entre fragmentos
length_function = len     # Función para medir longitud
```

### Retrieval
```python
search_type = "similarity"  # Tipo de búsqueda
k = 4                      # Número de fragmentos a recuperar
```

### LLM
```python
model = "gpt-4o-mini"     # Modelo de OpenAI
temperature = 0           # Deterministico (preciso)
max_tokens = None         # Sin límite específico
```

### Embeddings
```python
model = "text-embedding-3-small"  # Modelo de embeddings
dimensions = 1536         # Dimensiones del vector
```

---

## Seguridad y Mejores Prácticas

### Variables de Entorno
```bash
OPENAI_API_KEY=sk-xxxxx   # Nunca en código
OPENAI_MODEL=gpt-4o-mini  # Configurable
PORT=8000                  # Puerto del servidor
```

### CORS
```python
allow_origins=["*"]        # Configurar en producción
allow_credentials=True
allow_methods=["*"]
allow_headers=["*"]
```

### Validación
- Extensiones de archivo permitidas
- Tamaño máximo de archivo
- Validación de input del usuario
- Sanitización de respuestas

---

## Escalabilidad

### Optimizaciones Actuales
- FAISS para búsqueda eficiente O(log n)
- Chunking inteligente con overlap
- Cache de embeddings (implícito en FAISS)
- Streaming de archivos grandes

### Mejoras Futuras
- Redis para cache de consultas
- PostgreSQL + pgvector para persistencia
- Rate limiting con slowapi
- Load balancing con múltiples workers
- CDN para archivos estáticos

---

## Monitoreo y Logs

### Métricas Clave
- Tiempo de procesamiento por documento
- Tiempo de respuesta por query
- Número de tokens consumidos (OpenAI)
- Tasa de error
- Uso de memoria

### Logging
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
```

---

**Arquitectura diseñada para Hack Kognia 1.0** 🚀
