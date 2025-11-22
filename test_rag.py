"""
Script de prueba para verificar el sistema RAG sin interfaz web.
Útil para testing y debugging.
"""

import os
from dotenv import load_dotenv
from rag_system import RAGSystem, DocumentProcessor

# Cargar variables de entorno
load_dotenv()

def test_document_processing():
    """Prueba el procesamiento de documentos."""
    print("=== Test 1: Procesamiento de Documentos ===")
    
    # Procesar documento de ejemplo
    file_path = "ejemplo_contrato.txt"
    
    if not os.path.exists(file_path):
        print(f"❌ Error: Archivo {file_path} no encontrado")
        return
    
    try:
        text = DocumentProcessor.process_document(file_path, file_path)
        print(f"✅ Documento procesado exitosamente")
        print(f"📊 Longitud del texto: {len(text)} caracteres")
        print(f"📄 Primeros 200 caracteres: {text[:200]}...")
        return text
    except Exception as e:
        print(f"❌ Error procesando documento: {e}")
        return None

def test_rag_system(document_text):
    """Prueba el sistema RAG completo."""
    print("\n=== Test 2: Sistema RAG ===")
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("❌ Error: OPENAI_API_KEY no encontrada")
        return
    
    try:
        # Inicializar sistema RAG
        print("🔧 Inicializando sistema RAG...")
        rag = RAGSystem(api_key)
        
        # Añadir documento
        print("📚 Añadiendo documento al sistema...")
        rag.add_documents(
            texts=[document_text],
            metadatas=[{"filename": "ejemplo_contrato.txt"}]
        )
        print("✅ Documento añadido exitosamente")
        
        # Preguntas de prueba
        questions = [
            "¿Cuál es el objeto del contrato?",
            "¿Cuánto dura el contrato?",
            "¿Cuál es el valor mensual que se pagará?",
            "¿Cuáles son las obligaciones del contratista?",
            "¿De quién es la propiedad intelectual del software desarrollado?"
        ]
        
        print("\n=== Test 3: Consultas ===")
        for i, question in enumerate(questions, 1):
            print(f"\n📝 Pregunta {i}: {question}")
            
            try:
                result = rag.query(question)
                
                print(f"💬 Respuesta: {result['answer']}")
                print(f"📊 Confianza: {result['confidence']}")
                print(f"📚 Fuentes encontradas: {len(result['sources'])}")
                
                if result['sources']:
                    print("   Fragmento de fuente:")
                    source = result['sources'][0]
                    print(f"   {source['content'][:100]}...")
                
            except Exception as e:
                print(f"❌ Error en consulta: {e}")
        
        print("\n✅ Todas las pruebas completadas")
        
    except Exception as e:
        print(f"❌ Error en sistema RAG: {e}")

def main():
    """Función principal."""
    print("🚀 Iniciando pruebas del Asistente Legal RAG\n")
    
    # Test 1: Procesamiento de documentos
    document_text = test_document_processing()
    
    if document_text:
        # Test 2 y 3: Sistema RAG y consultas
        test_rag_system(document_text)
    
    print("\n🎉 Pruebas finalizadas")

if __name__ == "__main__":
    main()
