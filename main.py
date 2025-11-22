from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv
from rag_system import RAGSystem, DocumentProcessor

# Cargar variables de entorno
load_dotenv()

# Crear directorios necesarios
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

VECTOR_STORE_DIR = Path("vector_store")
VECTOR_STORE_DIR.mkdir(exist_ok=True)

STATIC_DIR = Path("static")
STATIC_DIR.mkdir(exist_ok=True)

# Inicializar FastAPI
app = FastAPI(
    title="Asistente Legal RAG",
    description="Sistema de consulta inteligente sobre documentos legales",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Inicializar sistema RAG
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY no encontrada en variables de entorno")

rag_system = RAGSystem(
    api_key=API_KEY,
    model_name=os.getenv("LLM_MODEL", "huggingface")
)

# Modelos Pydantic
class QueryRequest(BaseModel):
    question: str

class QueryResponse(BaseModel):
    answer: str
    sources: List[dict]
    confidence: str

class StatusResponse(BaseModel):
    status: str
    documents_loaded: List[str]
    message: str


@app.get("/")
async def root():
    """Sirve la interfaz web principal."""
    return FileResponse("static/index.html")


@app.get("/api/health")
async def health_check():
    """Verifica el estado del sistema."""
    return {
        "status": "healthy",
        "model": os.getenv("LLM_MODEL", "huggingface"),
        "documents_loaded": len(rag_system.documents_loaded)
    }


@app.post("/api/upload")
async def upload_documents(files: List[UploadFile] = File(...)):
    """
    Carga y procesa uno o varios documentos.
    Formatos soportados: PDF, DOCX, TXT
    """
    if not files:
        raise HTTPException(status_code=400, detail="No se enviaron archivos")
    
    processed_files = []
    texts = []
    metadatas = []
    
    try:
        for file in files:
            # Validar extensión
            filename = file.filename
            extension = Path(filename).suffix.lower()
            
            if extension not in ['.pdf', '.docx', '.txt']:
                raise HTTPException(
                    status_code=400,
                    detail=f"Formato no soportado: {extension}. Use PDF, DOCX o TXT"
                )
            
            # Guardar archivo temporalmente
            file_path = UPLOAD_DIR / filename
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            # Procesar documento
            text = DocumentProcessor.process_document(str(file_path), filename)
            
            if not text.strip():
                raise HTTPException(
                    status_code=400,
                    detail=f"El archivo {filename} está vacío o no se pudo leer"
                )
            
            texts.append(text)
            metadatas.append({"filename": filename})
            processed_files.append(filename)
            
            # Opcional: eliminar archivo después de procesarlo
            # file_path.unlink()
        
        # Añadir documentos al sistema RAG
        rag_system.add_documents(texts, metadatas)
        
        return {
            "status": "success",
            "message": f"Se cargaron {len(processed_files)} documento(s) exitosamente",
            "files": processed_files,
            "total_documents": len(rag_system.documents_loaded)
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando documentos: {str(e)}")


@app.post("/api/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """
    Realiza una consulta sobre los documentos cargados.
    """
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="La pregunta no puede estar vacía")
    
    if rag_system.vector_store is None:
        raise HTTPException(
            status_code=400,
            detail="No hay documentos cargados. Por favor, cargue documentos primero."
        )
    
    try:
        result = rag_system.query(request.question)
        return QueryResponse(**result)
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error procesando consulta: {str(e)}")


@app.post("/api/reset")
async def reset_system():
    """
    Reinicia el sistema, eliminando todos los documentos cargados.
    """
    try:
        rag_system.reset()
        
        # Limpiar archivos subidos (opcional)
        for file in UPLOAD_DIR.glob("*"):
            if file.is_file():
                file.unlink()
        
        return {
            "status": "success",
            "message": "Sistema reiniciado exitosamente"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reiniciando sistema: {str(e)}")


@app.get("/api/status", response_model=StatusResponse)
async def get_status():
    """
    Obtiene el estado actual del sistema.
    """
    has_documents = rag_system.vector_store is not None
    
    return StatusResponse(
        status="ready" if has_documents else "waiting_for_documents",
        documents_loaded=rag_system.documents_loaded,
        message=f"{len(rag_system.documents_loaded)} documento(s) cargado(s)" if has_documents 
                else "No hay documentos cargados"
    )


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(
        "main:app",
        host=os.getenv("HOST", "0.0.0.0"),
        port=port,
        reload=True
    )
