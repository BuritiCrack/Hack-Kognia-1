# 🚀 Optimización RAG Avanzada - Respuestas Precisas y Contextuales

## 🔍 Problema Identificado

**Pregunta:** "¿Qué requisitos debe cumplir una persona para obtener una licencia de conducción según la ley?"

**Respuesta anterior:** Fragmentos sobre definiciones de "homologación", "infracción", procedimientos de daños materiales - **NO respondía la pregunta real**.

**Causa raíz:**
- Búsqueda solo por similitud semántica (palabras como "licencia de conducción")
- Sin validación de relevancia del contenido
- Chunks muy pequeños (1000 chars) que perdían contexto
- Sin re-ranking por palabras clave importantes

---

## ✅ Mejoras Implementadas

### 1. **Chunks Más Grandes con Mejor Overlap** 📏

**Antes:**
```python
chunk_size=1000
chunk_overlap=200
```

**Ahora:**
```python
chunk_size=1500  # +50% más contexto
chunk_overlap=300  # Mayor continuidad entre chunks
separators=["\n\n", "\n", ". ", " ", ""]  # Separadores naturales
```

**Beneficio:** Captura contextos más completos (por ejemplo, un artículo legal completo sobre requisitos).

---

### 2. **Expansión de Consultas** 🔄

El sistema ahora genera variaciones de la pregunta usando sinónimos:

**Pregunta original:**
```
"¿Qué requisitos debe cumplir una persona para obtener una licencia de conducción?"
```

**Consultas expandidas:**
1. Original: "requisitos... obtener... licencia de conducción"
2. Variación 1: "condiciones... tramitar... licencia de conducir"
3. Variación 2: "exigencias... solicitar... pase de conducción"

**Diccionario de expansiones:**
- `requisitos` → condiciones, requerimientos, exigencias, debe cumplir
- `obtener` → conseguir, tramitar, solicitar, adquirir
- `licencia de conducción` → licencia de conducir, pase de conducción, permiso de conducir
- `procedimiento` → proceso, trámite, pasos, cómo hacer
- `obligaciones` → deberes, responsabilidades
- `derechos` → facultades, puede hacer
- `sanciones` → multas, penalidades, infracciones
- `plazo` → término, tiempo, fecha límite

---

### 3. **Re-Ranking por Palabras Clave** 🎯

**Proceso:**
1. **Extracción de keywords:** Extrae palabras importantes de la pregunta (ignora stopwords)
   - Pregunta: "¿Qué requisitos debe cumplir una persona para obtener una licencia de conducción?"
   - Keywords: [`requisitos`, `cumplir`, `persona`, `obtener`, `licencia`, `conducción`, `licencia conducción`]

2. **Scoring por keywords:**
   - Cuenta cuántas keywords aparecen en cada chunk
   - Calcula densidad de keywords (keywords / palabras totales)
   - **Prioriza chunks con 2+ keywords relevantes**

3. **Doble ordenamiento:**
   - Primero por keyword_score (más keywords = mejor)
   - Segundo por similarity score (más similar = mejor)

**Resultado:** Chunks con "requisitos para licencia" superan a chunks que solo dicen "licencia de conducción".

---

### 4. **Filtrado de Resultados Irrelevantes** 🛡️

**Criterio de relevancia:**
```python
relevant_sources = [s for s in sources if s['keyword_score'] >= 2]
```

**Efecto:** Solo muestra fragmentos que contienen al menos 2 palabras clave de la pregunta.

**Fallback:** Si el filtro es muy estricto y no encuentra nada, usa los 3 mejores por similitud.

---

### 5. **Preview Inteligente con Contexto** 📖

**Antes:** Mostraba los primeros 500 caracteres del chunk

**Ahora:** Busca dónde aparece la primera keyword y muestra 200 chars antes + 500 chars después

**Ejemplo:**
- Keyword encontrada: "requisitos"
- Preview: "...Para ser conductor profesional se deben cumplir los siguientes **requisitos**: 1) Ser mayor de 21 años, 2) Aprobar examen médico, 3) Curso de conducción profesional..."

---

### 6. **Detección de Tipo de Pregunta Mejorada** 🤖

Ahora detecta específicamente preguntas sobre **requisitos**:

```python
is_requirements = any(word in question_lower for word in 
    ["requisitos", "condiciones", "debe cumplir", "exigencias"])
```

**Formato de respuesta:**
```
📋 **Requisitos según la Ley:**

**Fragmento 1** (Relevancia: 5 términos clave):
...texto relevante centrado en la keyword principal...
```

---

### 7. **Métricas de Relevancia Visibles** 📊

El usuario ahora ve:
- **Similitud semántica:** `(Similitud: 0.85)`
- **Palabras clave encontradas:** `(Palabras clave: 5)`

**Ejemplo:**
```
📄 Código de Tránsito - Fragmento 42
(Similitud: 0.78 | Palabras clave: 5)
```

---

## 🧪 Cómo Probar las Mejoras

### Test Case 1: Requisitos de Licencia

**Pregunta:**
```
¿Qué requisitos debe cumplir una persona para obtener una licencia de conducción según la ley?
```

**Resultado esperado:**
- Fragmentos sobre artículos que mencionen "requisitos" + "licencia"
- NO fragmentos sobre definiciones generales
- Preview centrado en la parte que habla de requisitos

---

### Test Case 2: Procedimiento de Renovación

**Pregunta:**
```
¿Cómo se renueva la licencia de conducción?
```

**Expansión automática:**
- "¿Cómo se renueva..." 
- "¿Cuál es el proceso para renovar..."
- "¿Qué trámite se debe hacer para renovar..."

**Resultado esperado:**
- Fragmentos sobre procedimiento de renovación
- NO fragmentos sobre obtención inicial

---

### Test Case 3: Sanciones por Conducir sin Licencia

**Pregunta:**
```
¿Qué sanciones tiene conducir sin licencia?
```

**Keywords:** `sanciones`, `conducir`, `licencia`

**Resultado esperado:**
- Fragmentos sobre infracciones y multas
- Artículos específicos sobre la sanción
- NO fragmentos sobre requisitos para obtener licencia

---

## 📈 Comparación Antes vs Ahora

| Aspecto | Antes | Ahora |
|---------|-------|-------|
| **Chunk size** | 1000 chars | 1500 chars (+50%) |
| **Overlap** | 200 chars | 300 chars (+50%) |
| **Consultas** | 1 pregunta fija | 3 variaciones con sinónimos |
| **Búsqueda** | Top 6 por similitud | Top 10 por similitud → deduplicar → re-rank |
| **Filtrado** | Ninguno | Mínimo 2 keywords |
| **Preview** | Primeros 500 chars | Contexto alrededor de keyword |
| **Relevancia** | Solo score FAISS | Score FAISS + keyword_score |
| **K documentos** | 6 | 10 candidatos → hasta 15 re-rankeados → 3 mejores |

---

## 🔧 Configuración Avanzada (Opcional)

### Ajustar Umbral de Keywords

En `rag_system.py`, línea donde dice:
```python
relevant_sources = [s for s in sources if s['keyword_score'] >= 2]
```

**Opciones:**
- `>= 1`: Más permisivo (muestra más resultados)
- `>= 2`: Balanceado (actual)
- `>= 3`: Muy estricto (solo resultados muy relevantes)

---

### Ampliar Diccionario de Sinónimos

Edita el método `_expand_query()` para agregar más términos específicos de tu dominio:

```python
expansions = {
    'requisitos': ['condiciones', 'requerimientos', 'exigencias'],
    'contrato': ['acuerdo', 'convenio', 'pacto'],  # NUEVO
    'arrendamiento': ['alquiler', 'renta'],  # NUEVO
    # ... más términos
}
```

---

### Aumentar Número de Chunks Analizados

Cambiar `k=10` a `k=15` o `k=20` para buscar más candidatos:

```python
docs_with_scores = self.vector_store.similarity_search_with_score(query, k=20)
```

**Trade-off:** Más precisión vs más tiempo de procesamiento.

---

## 🚨 Mensajes de Error Mejorados

Si no encuentra información relevante:

```
❌ No se encontró información específica para responder tu pregunta.

Sugerencias:
- Verifica que el documento contenga información sobre este tema
- Intenta usar términos diferentes (ej: 'requisitos' en vez de 'condiciones')
- Asegúrate de que el documento esté correctamente cargado
```

---

## 📊 Interpretación de Métricas

### Similitud (basada en FAISS)
- **0.90-1.00**: Muy alta similitud (casi idéntico)
- **0.70-0.89**: Alta similitud (relevante)
- **0.50-0.69**: Similitud media
- **< 0.50**: Baja similitud (posiblemente irrelevante)

### Palabras Clave
- **5+**: Altamente relevante (múltiples términos de la pregunta)
- **3-4**: Relevante (algunos términos clave)
- **2**: Mínimo aceptable (al menos 2 términos)
- **< 2**: Filtrado automáticamente

### Confianza Final
- **Alta**: Score promedio < 0.5 con 3+ fuentes relevantes
- **Media**: Score promedio < 0.8 con 2+ fuentes
- **Baja**: Otros casos

---

## 🎯 Próximos Pasos Recomendados

### Opción A: Integrar LLM Local para Síntesis
El sistema actual muestra fragmentos directos. Para generar respuestas en lenguaje natural:

1. **Instalar Ollama:**
```powershell
# Descargar desde ollama.ai
ollama pull llama3.2:3b
```

2. **Modificar rag_system.py:**
```python
from langchain_ollama import ChatOllama

llm = ChatOllama(model="llama3.2:3b")
# Usar LLM para sintetizar respuesta desde los chunks relevantes
```

**Beneficio:** Respuestas coherentes y naturales en lugar de fragmentos crudos.

---

### Opción B: Implementar Búsqueda Híbrida (BM25 + Semantic)

Combinar búsqueda por keywords (BM25) con búsqueda semántica (embeddings):

```python
from langchain.retrievers import EnsembleRetriever
from langchain_community.retrievers import BM25Retriever

# Combinar ambos métodos (50% keywords, 50% semántica)
ensemble = EnsembleRetriever(
    retrievers=[bm25_retriever, semantic_retriever],
    weights=[0.5, 0.5]
)
```

---

### Opción C: Caché de Consultas Frecuentes

Para acelerar consultas repetidas:

```python
import json

class QueryCache:
    def __init__(self):
        self.cache = {}
    
    def get(self, question):
        return self.cache.get(question)
    
    def set(self, question, answer):
        self.cache[question] = answer
```

---

## 🧪 Verificación de Cambios

### 1. Revisar que el servidor se haya reiniciado

Deberías ver en el terminal:
```
INFO:     Application startup complete.
```

### 2. Probar con la pregunta problemática

```
Pregunta: ¿Qué requisitos debe cumplir una persona para obtener una licencia de conducción según la ley?
```

### 3. Verificar las métricas

Revisa que aparezca:
- ✅ "Relevancia: 3+ términos clave"
- ✅ Fragmentos que realmente hablen de requisitos
- ✅ Preview centrado en la información relevante

---

## 📝 Archivos Modificados

- **rag_system.py**:
  - Método `add_documents()`: Chunks 1500/300
  - Método `_expand_query()`: Expansión con sinónimos (NUEVO)
  - Método `query()`: Búsqueda expandida + re-ranking (REESCRITO)
  - Método `_extract_keywords()`: Extracción de palabras clave (NUEVO)
  - Método `_rerank_by_keywords()`: Re-ranking por keywords (NUEVO)
  - Método `_create_smart_preview()`: Preview contextual (NUEVO)

- **static/app.js**:
  - Función `addMessage()`: Muestra keyword_score

---

## 💡 Tips para el Usuario Final

### ✅ Preguntas que Funcionan Bien:
- "¿Qué requisitos necesito para obtener una licencia de conducción?"
- "¿Cuáles son las sanciones por conducir sin licencia?"
- "¿Cómo se renueva el permiso de conducir?"
- "¿Cuánto tiempo tengo para notificar un accidente?"

### ❌ Preguntas Difíciles:
- "Dime todo sobre las licencias" (muy amplio)
- "¿Y eso qué implica?" (sin contexto previo)
- "Explícame la ley" (sin foco específico)

### 🎯 Cómo Mejorar una Pregunta:
**Vago:** "¿Qué dice sobre las licencias?"
**Mejor:** "¿Qué requisitos pide la ley para obtener una licencia de conducción?"

**Vago:** "¿Cuáles son las multas?"
**Mejor:** "¿Qué sanciones hay por conducir sin licencia?"

---

¡Ahora tu sistema RAG es **significativamente más preciso** y relevante! 🎉
