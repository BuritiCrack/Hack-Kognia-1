# 🎥 Script para Demo del Asistente Legal RAG

## Preparación (Antes de la demo)

### ✅ Checklist Pre-Demo
- [ ] Aplicación corriendo en URL pública (Render/Railway)
- [ ] Navegador abierto en la URL
- [ ] Documento de prueba listo (ejemplo_contrato.txt)
- [ ] Preguntas preparadas
- [ ] Conexión a internet estable
- [ ] Audio y video funcionando

---

## 🎬 Guión de Demostración (5 minutos)

### Introducción (30 segundos)

> "Hola, les presento el **Asistente Legal Inteligente**, un sistema RAG (Retrieval-Augmented Generation) que permite consultar documentos legales de manera inteligente usando IA."

**Mostrar:**
- Pantalla principal de la aplicación
- Título y descripción

---

### Parte 1: Arquitectura y Tecnología (1 minuto)

> "El sistema está construido con:"
> - "**Backend**: FastAPI con Python"
> - "**IA**: LangChain + OpenAI GPT-4o-mini"
> - "**Base Vectorial**: FAISS para búsqueda semántica"
> - "**Frontend**: JavaScript puro, sin frameworks"

**Mostrar:**
- Diagrama de arquitectura (puede ser en diapositiva)
- O mencionar verbalmente mientras se ve la interfaz

---

### Parte 2: Carga de Documentos (1 minuto)

> "Vamos a cargar un contrato de prestación de servicios profesionales."

**Acciones:**
1. Click en "Seleccionar Archivos"
2. Seleccionar `ejemplo_contrato.txt`
3. Mostrar archivo seleccionado en la lista
4. Click en "Subir y Procesar Documentos"
5. Esperar mensaje de confirmación

**Narración mientras procesa:**
> "El sistema está:"
> - "Extrayendo el texto del documento"
> - "Dividiéndolo en fragmentos inteligentes"
> - "Creando embeddings vectoriales"
> - "Indexándolo en la base vectorial FAISS"

**Mostrar:**
- Estado cambia a "X documento(s) cargado(s)"
- Campo de pregunta se activa

---

### Parte 3: Consultas Inteligentes (2.5 minutos)

#### Pregunta 1: Información Básica
**Escribir:** "¿Cuál es el objeto del contrato?"

**Narración:**
> "El sistema busca en el documento y genera una respuesta contextualizada."

**Mostrar:**
- Respuesta generada
- Fuentes citadas del documento
- Nivel de confianza

---

#### Pregunta 2: Información Específica
**Escribir:** "¿Cuánto se paga mensualmente y cuándo?"

**Narración:**
> "Observen cómo extrae información específica de múltiples secciones."

**Mostrar:**
- Respuesta con valor y fechas
- Fragmentos relevantes del contrato

---

#### Pregunta 3: Análisis Complejo
**Escribir:** "¿Cuáles son las principales obligaciones del contratista?"

**Narración:**
> "Ahora una pregunta que requiere analizar y sintetizar información."

**Mostrar:**
- Lista de obligaciones
- Múltiples fuentes citadas
- Nivel de confianza alto

---

#### Pregunta 4: Tema Legal
**Escribir:** "¿Qué dice sobre la propiedad intelectual?"

**Narración:**
> "El sistema entiende conceptos legales y encuentra cláusulas específicas."

**Mostrar:**
- Explicación de la cláusula
- Fuente exacta

---

### Parte 4: Transparencia y Confianza (30 segundos)

**Destacar:**
1. **Fuentes visibles**: Cada respuesta muestra de dónde viene
2. **Nivel de confianza**: Alta, Media o Baja
3. **Fragmentos originales**: Se pueden ver los textos exactos
4. **Sin invención**: Solo responde con base en documentos

> "A diferencia de ChatGPT normal, este sistema **NO inventa información**.
> Todo está fundamentado en los documentos cargados."

---

### Cierre (30 segundos)

> "En resumen, este Asistente Legal:"
> - "✅ Procesa documentos PDF, DOCX y TXT"
> - "✅ Responde preguntas en lenguaje natural"
> - "✅ Cita fuentes y muestra confianza"
> - "✅ Es 100% transparente y verificable"
> - "✅ Está desplegado en la nube y accesible 24/7"

**Mostrar:**
- Pantalla final con varias consultas realizadas
- URL pública de la aplicación

> "Gracias. ¿Preguntas?"

---

## 🎯 Preguntas Alternativas (Backup)

Si hay tiempo o preguntas del jurado:

1. "¿Cuál es la duración del contrato y es renovable?"
2. "¿Qué sucede si alguna parte incumple el contrato?"
3. "¿Hay alguna cláusula sobre confidencialidad?"
4. "¿Quién asume los gastos e impuestos?"
5. "¿Cómo se resuelven las controversias?"

---

## 💡 Puntos Clave a Destacar

### Diferenciadores
1. **RAG vs LLM Simple**: No inventa, solo usa documentos cargados
2. **Transparencia**: Muestra fuentes exactas
3. **Múltiples documentos**: Puede buscar en varios archivos
4. **Confianza medible**: Sistema de scoring

### Aspectos Técnicos (Si preguntan)
- Chunks de 1000 caracteres con overlap de 200
- Embeddings con OpenAI text-embedding-3-small
- Retrieval de top 4 fragmentos más relevantes
- Zero-shot prompting para respuestas precisas

### Escalabilidad
- Backend preparado para producción
- Base vectorial FAISS eficiente
- Fácil agregar PostgreSQL para persistencia
- Puede manejar cientos de documentos

---

## 🚨 Manejo de Problemas Comunes

### Si la carga es lenta:
> "El sistema está procesando el documento y creando los embeddings vectoriales, 
> lo cual toma unos segundos para garantizar búsquedas precisas."

### Si una respuesta tarda:
> "El sistema está buscando en todos los fragmentos del documento y consultando
> el modelo GPT-4o-mini para generar la respuesta más precisa."

### Si no encuentra información:
> "Como pueden ver, cuando el sistema no encuentra información relevante en el
> documento, lo indica honestamente en lugar de inventar una respuesta."

---

## 📊 Datos para Mencionar

- **Tecnología**: LangChain + FAISS + GPT-4o-mini
- **Tiempo de desarrollo**: Para hackathon
- **Costo operativo**: ~$0.01-0.10 por consulta
- **Formatos soportados**: PDF, DOCX, TXT
- **Deployment**: Render.com (gratis)
- **URL pública**: [Tu URL aquí]

---

## 🎤 Tips para la Presentación

1. **Practicar antes**: Cronometrar para estar en 5 minutos
2. **Tener backup**: Si falla internet, tener video grabado
3. **Ser concreto**: Mostrar > Explicar
4. **Destacar valor**: Cómo ayuda a abogados realmente
5. **Preparar para preguntas**: Conocer limitaciones

---

## ✨ Posibles Mejoras a Mencionar (Si preguntan)

1. **PostgreSQL**: Para persistencia de documentos
2. **Autenticación**: Sistema de usuarios
3. **Multi-idioma**: Soporte para inglés, francés, etc.
4. **Analytics**: Dashboard de consultas frecuentes
5. **Comparación**: Comparar cláusulas entre documentos
6. **Export**: Generar reportes en PDF
7. **OCR**: Para PDFs escaneados

---

**¡Éxito en la demo! 🚀**
