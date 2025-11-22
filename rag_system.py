import os
from typing import List, Optional
from pathlib import Path
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from pypdf import PdfReader
import docx
import pickle


class DocumentProcessor:
    """Procesa y carga documentos PDF y DOCX."""
    
    @staticmethod
    def extract_text_from_pdf(file_path: str) -> str:
        """Extrae texto de un archivo PDF."""
        reader = PdfReader(file_path)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"
        return text
    
    @staticmethod
    def extract_text_from_docx(file_path: str) -> str:
        """Extrae texto de un archivo DOCX."""
        doc = docx.Document(file_path)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    @staticmethod
    def extract_text_from_txt(file_path: str) -> str:
        """Extrae texto de un archivo TXT."""
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    
    @classmethod
    def process_document(cls, file_path: str, filename: str) -> str:
        """Procesa un documento y extrae su texto."""
        extension = Path(filename).suffix.lower()
        
        if extension == '.pdf':
            return cls.extract_text_from_pdf(file_path)
        elif extension == '.docx':
            return cls.extract_text_from_docx(file_path)
        elif extension == '.txt':
            return cls.extract_text_from_txt(file_path)
        else:
            raise ValueError(f"Formato de archivo no soportado: {extension}")


class RAGSystem:
    """Sistema RAG para consultas sobre documentos legales usando modelos locales."""
    
    def __init__(self, api_key: str, model_name: str = "huggingface"):
        self.api_key = api_key
        self.model_name = model_name
        
        # Usar embeddings locales gratuitos
        self.embeddings = HuggingFaceEmbeddings(
            model_name="sentence-transformers/all-MiniLM-L6-v2",
            model_kwargs={'device': 'cpu'}
        )
        
        self.vector_store: Optional[FAISS] = None
        self.documents_loaded = []
        
    def add_documents(self, texts: List[str], metadatas: List[dict]):
        """Añade documentos al sistema RAG."""
        # Crear splitter para dividir textos largos
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200,
            length_function=len,
        )
        
        # Crear documentos
        documents = []
        for text, metadata in zip(texts, metadatas):
            splits = text_splitter.split_text(text)
            for i, split in enumerate(splits):
                doc = Document(
                    page_content=split,
                    metadata={**metadata, "chunk": i}
                )
                documents.append(doc)
        
        self.documents_loaded.extend([m['filename'] for m in metadatas])
        
        # Crear o actualizar vector store
        if self.vector_store is None:
            self.vector_store = FAISS.from_documents(documents, self.embeddings)
        else:
            new_store = FAISS.from_documents(documents, self.embeddings)
            self.vector_store.merge_from(new_store)
        
    def query(self, question: str) -> dict:
        """Realiza una consulta al sistema RAG usando búsqueda por similitud."""
        if self.vector_store is None:
            raise ValueError("No hay documentos cargados en el sistema.")
        
        # Buscar documentos similares
        docs_with_scores = self.vector_store.similarity_search_with_score(question, k=4)
        
        # Procesar fuentes
        sources = []
        for doc, score in docs_with_scores:
            sources.append({
                "content": doc.page_content,
                "filename": doc.metadata.get("filename", "Desconocido"),
                "chunk": doc.metadata.get("chunk", 0),
                "score": float(score)
            })
        
        # Crear una respuesta basada en los fragmentos recuperados
        if sources:
            answer_parts = ["Basándome en el documento, he encontrado la siguiente información relevante:\n"]
            for i, source in enumerate(sources[:2], 1):  # Mostrar máximo 2 fragmentos más relevantes
                answer_parts.append(f"\n{i}. {source['content'][:400]}...")
            answer = "".join(answer_parts)
        else:
            answer = "No se encontró información relevante en el documento."
        
        return {
            "answer": answer,
            "sources": sources,
            "confidence": self._calculate_confidence(sources)
        }
    
    def _calculate_confidence(self, sources: List[dict]) -> str:
        """Calcula el nivel de confianza basado en las fuentes."""
        num_sources = len(sources)
        if num_sources >= 3:
            return "Alta"
        elif num_sources >= 2:
            return "Media"
        else:
            return "Baja"
    
    def save_vector_store(self, path: str):
        """Guarda el vector store en disco."""
        if self.vector_store:
            self.vector_store.save_local(path)
    
    def load_vector_store(self, path: str):
        """Carga el vector store desde disco."""
        self.vector_store = FAISS.load_local(
            path,
            self.embeddings,
            allow_dangerous_deserialization=True
        )
    
    def reset(self):
        """Reinicia el sistema RAG."""
        self.vector_store = None
        self.documents_loaded = []
