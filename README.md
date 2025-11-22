# ⚖️ Hack-Kognia RAG — Asistente Legal Inteligente

Una aplicación RAG (Retrieval-Augmented Generation) para responder consultas sobre documentos legales. Este proyecto fue desarrollado como demo para Hack Kognia 1.0 y permite cargar documentos (PDF, DOCX, TXT), indexarlos mediante embeddings y responder preguntas con contexto extraído de los documentos.

## 👥 Integrantes del Proyecto

- 👨‍💻 Andrés Gutiérrez
- 👩‍💻 Manuela Cardona
- 👨‍💻 José Buritica

## 🚀 Mejoras Recientes (v2.0)

### Sistema RAG Optimizado para Precisión y Relevancia

**Problema resuelto:** El sistema anterior devolvía fragmentos con palabras similares pero no respondía la pregunta real.

**Mejoras implementadas:**

1. **📏 Chunks más grandes** (1000→1500 chars) con mejor overlap (200→300 chars)
2. **🔄 Expansión de consultas** con sinónimos automáticos (ej: "requisitos"→"condiciones", "exigencias")
3. **🎯 Re-ranking por palabras clave** - prioriza fragmentos con términos relevantes de la pregunta
4. **🛡️ Filtrado inteligente** - solo muestra fragmentos con 2+ palabras clave relevantes
5. **📖 Preview contextual** - muestra contexto alrededor de las keywords encontradas
6. **📊 Métricas visibles** - similitud semántica + contador de palabras clave

**Resultado:** Respuestas hasta **3x más relevantes** para preguntas específicas.

👉 **Ver detalles completos:** [OPTIMIZACION_RAG_AVANZADA.md](./OPTIMIZACION_RAG_AVANZADA.md)

---

## 🙏 Agradecimientos

Muchas gracias a la organización **TalentoTech y Kognia** por el apoyo y la confianza en nosotros durante el desarrollo de este proyecto.
**Estado**: Proyecto local / demo. No está desplegado en Render debido al uso de un modelo de HuggingFace que requiere almacenamiento grande (se llenaba el disco del servicio) y la cuenta gratuita no fue suficiente para las pruebas.

**Contenido rápido**

- **Backend**: FastAPI + LangChain + FAISS
- **Frontend**: HTML/CSS + JavaScript (vanilla)
- **Modelos/Embeddings**: HuggingFace (modelo local) / OpenAI embeddings según configuración

**Objetivo**: Demostrar un flujo RAG completo: carga de documentos → chunking → embeddings → búsqueda semántica → respuesta contextualizada.

**Directorio principal**

- `backend/` — API y procesamiento RAG (Python, FastAPI)
- `frontend/` — Interfaz web estática

**¿Por qué NO está en Render?**
Usamos un modelo de HuggingFace que almacena pesos grandes localmente. Al intentar desplegar en Render el almacenamiento se llenó rápidamente y la capa gratuita no cubre el espacio/tiempo de cómputo requerido. Por eso el servicio se mantiene para ejecución local o en entornos con GPU/espacio suficiente.

**Índice**

- **Qué hace**
- **Tecnologías**
- **Instalación y ejecución (local, Windows)**
- **Variables de entorno**
- **Endpoints principales**
- **Notas de despliegue y limitaciones**
- **Contribuir**
- **Licencia y autoría**

**Qué se hizo (resumen)**

- Implementación de backend en FastAPI que procesa documentos, crea embeddings, guarda vectores en FAISS y expone endpoints para upload, consulta, estado y reinicio.
- Frontend simple que permite subir archivos y consultar mediante un chat.
- Pipeline de extracción y chunking de documentos (PDF/DOCX/TXT).
- Integración con LangChain para orquestar recuperación + generación.

**Características principales**

- Carga de múltiples documentos en una sola sesión
- Tokenización/segmentación (chunking) configurable
- Indexado en FAISS (búsqueda semántica rápida)
- Respuestas con referencias a fragmentos fuente

**Tecnologías y librerías**

- Lenguaje: Python 3.9+
- Framework: `FastAPI`
- Orquestador RAG: `langchain`
- Vector DB: `faiss` (o `faiss-cpu` según instalación)
- Procesamiento PDF: `pypdf`
- Procesamiento DOCX: `python-docx`
- Server: `uvicorn`
- Frontend: HTML5, CSS3, JavaScript (vanilla)

**Instalación y ejecución (Local — Windows PowerShell)**

1. Clonar repositorio:

```powershell
git clone https://github.com/AndresFGutierrez/hack-kognia-rag-legal.git
cd hack-kognia-rag-legal
```

2. Crear y activar entorno virtual (Windows PowerShell):

```powershell
python -m venv venv
venv\Scripts\Activate
```

3. Instalar dependencias:

```powershell
pip install -r requirements.txt
```

4. Copiar archivo de ejemplo de variables de entorno y editar:

```powershell
copy .env.example .env
# Abrir .env y completar las variables (ver sección siguiente)
```

5. Ejecutar la API (modo desarrollo):

```powershell
# Opción 1: Ejecutar el script principal
python main.py

# Opción 2: Con uvicorn (recarga automática)
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

6. Abrir frontend en el navegador (si ejecutas frontend dev):

```powershell
cd frontend
# si hay un script npm para el frontend, usarlo; por ejemplo:
npm install
npm run dev
```

Luego abrir `http://localhost:8000` (o la url que indique el backend/frontend según configuración).

**Variables de entorno (ejemplo)**

- `OPENAI_API_KEY` — (opcional) si usas OpenAI para embeddings o LLM.
- `HF_MODEL_PATH` — ruta local al modelo HuggingFace (si usas modelo local).
- `OPENAI_MODEL` — nombre del modelo OpenAI, si aplica.
- `CHUNK_SIZE` y `CHUNK_OVERLAP` — parámetros de chunking (si están soportados por la app).

Edita `.env` según tus necesidades.

**Endpoints principales**

- `GET /` — Interfaz web principal
- `GET /api/health` — Estado del servicio
- `POST /api/upload` — Subir y procesar documentos (multipart/form-data)
- `POST /api/query` — Preguntar al sistema: `{"question":"..."}`
- `POST /api/reset` — Limpiar índice y documentos cargados
- `GET /api/status` — Estado interno y número de documentos cargados

Ejemplo de `POST /api/query` (JSON):

```json
{ "question": "¿Qué dice el documento sobre cláusulas de rescisión?" }
```

Respuesta esperada: objeto JSON con texto de respuesta, fragmentos fuente y nivel de confianza.

**Notas sobre despliegue y limitaciones**

- El proyecto funciona bien localmente o en servidores con espacio/CPU suficientes. No está desplegado en Render por la siguiente razón:
  - Usamos un modelo de `HuggingFace` con pesos grandes que se almacenan localmente. Durante intentos de despliegue en Render el almacenamiento se llenó rápidamente y la capa gratuita no fue suficiente para realizar las pruebas. Por ello recomendamos desplegar en infra con disco persistente y/o instancias con GPU (AWS, GCP, Azure, o servidores propios).
- Para probar de forma económica: usar modelos más pequeños, embeddings externos (OpenAI), o alojar los vectores en un servicio gestionado.

**Sugerencias para producción**

- Usar un servicio gestionado para vectores (Pinecone, Milvus Cloud, etc.) para evitar uso intensivo de disco.
- Separar almacenamiento de modelos y de la app (NFS, S3, o discos persistentes grandes).
- Limitar el tamaño máximo de archivos en uploads y controlar el uso de memoria.

**Contribuir**

- Fork del repo → crear rama `feature/mi-mejora` → PR con descripción clara y tests si aplica.

**Soporte y troubleshooting**

- Si la app no arranca, revisa:
  - `requirements.txt` instalado correctamente
  - Variables de entorno en `.env`
  - Disponibilidad de espacio en disco si usas modelo local HuggingFace
  - Logs en consola (FastAPI / Uvicorn)

**Autor**

- Proyecto desarrollado para Hackaton Kognia 1.0
