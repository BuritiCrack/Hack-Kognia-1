# ⚠️ IMPORTANTE - Lee Antes de Comenzar

## 🔐 Configuración Obligatoria

### 1. OpenAI API Key (REQUERIDO)

Este proyecto **requiere** una API key de OpenAI para funcionar. Sin ella, la aplicación no podrá procesar documentos ni responder preguntas.

#### Cómo obtener tu API key:

1. **Crear cuenta en OpenAI**
   - Ve a: https://platform.openai.com
   - Regístrate o inicia sesión

2. **Obtener API key**
   - Dashboard → API keys
   - Click en "Create new secret key"
   - Copia la key (empieza con `sk-...`)
   - ⚠️ **IMPORTANTE**: Guárdala, no se mostrará de nuevo

3. **Configurar en el proyecto**
   ```powershell
   # Copiar archivo de ejemplo
   copy .env.example .env
   
   # Editar .env y pegar tu key
   OPENAI_API_KEY=sk-tu-key-aqui
   ```

#### Costos de OpenAI:
- **Cuenta nueva**: $5 de crédito gratis
- **Por consulta**: ~$0.01-0.10 (varía según longitud)
- **Recomendación**: Monitorear uso en dashboard de OpenAI

---

## 💰 Presupuesto del Proyecto

### Desarrollo
- ✅ **$0** - Todo open source

### Hosting (Opciones)
- ✅ **Render.com**: $0/mes (free tier)
- 💵 **Railway**: $5-10/mes
- 💵 **Heroku**: $7/mes mínimo

### API de OpenAI
- 💵 **Embeddings**: ~$0.02 por 1,000 documentos procesados
- 💵 **GPT-4o-mini**: ~$0.01-0.10 por consulta

**Total para demo/hackathon**: < $10

---

## 🚨 Problemas Comunes y Soluciones

### Error: "OPENAI_API_KEY not found"
**Causa**: No has configurado el archivo `.env`

**Solución**:
```powershell
# Verificar que .env existe
Test-Path .env

# Si no existe, copiar de ejemplo
copy .env.example .env

# Editar .env con tu API key
notepad .env
```

---

### Error: "Invalid API key"
**Causa**: La API key es incorrecta o está mal copiada

**Solución**:
1. Verificar que la key empieza con `sk-`
2. No debe tener espacios antes/después
3. Generar nueva key en OpenAI si es necesario

---

### Error: "Module not found: langchain/faiss/etc"
**Causa**: Dependencias no instaladas o entorno virtual no activado

**Solución**:
```powershell
# Activar entorno virtual
venv\Scripts\Activate.ps1

# Reinstalar dependencias
pip install -r requirements.txt
```

---

### Error: "Port 8000 is already in use"
**Causa**: Otro proceso está usando el puerto

**Solución**:
```powershell
# Opción 1: Cambiar puerto en .env
echo "PORT=3000" >> .env

# Opción 2: Matar proceso en puerto 8000
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

---

### Error: "Rate limit exceeded"
**Causa**: Demasiadas peticiones a OpenAI API

**Solución**:
1. Esperar 1 minuto
2. Verificar límites en dashboard de OpenAI
3. Considerar upgrade de plan si es necesario

---

### Error: "Out of memory"
**Causa**: Documento muy grande o muchos documentos

**Solución**:
1. Reducir `chunk_size` en `rag_system.py` (línea 65)
2. Procesar documentos más pequeños
3. Usar plan de hosting con más RAM

---

## 📋 Checklist Pre-Ejecución

Antes de ejecutar `python main.py`, verifica:

- [ ] Python 3.9+ instalado (`python --version`)
- [ ] Entorno virtual creado (`Test-Path venv`)
- [ ] Entorno virtual activado (terminal muestra `(venv)`)
- [ ] Dependencias instaladas (`pip list` muestra fastapi, langchain, etc)
- [ ] Archivo `.env` existe (`Test-Path .env`)
- [ ] OPENAI_API_KEY configurada en `.env`
- [ ] Puerto 8000 libre (o configurado otro en `.env`)

---

## 🔒 Seguridad

### ⚠️ NUNCA hagas esto:
1. ❌ Subir `.env` a GitHub
2. ❌ Compartir tu API key públicamente
3. ❌ Hacer commit de tu API key en el código
4. ❌ Usar la misma key en múltiples proyectos públicos

### ✅ Buenas prácticas:
1. ✅ Usa `.env` para variables sensibles
2. ✅ Mantén `.env` en `.gitignore`
3. ✅ Rota tu API key periódicamente
4. ✅ Monitorea uso en dashboard de OpenAI
5. ✅ Configura límites de gasto en OpenAI

---

## 📊 Límites y Restricciones

### Límites del Sistema
- **Tamaño máximo de archivo**: ~50 MB
- **Formatos soportados**: PDF, DOCX, TXT
- **Memoria**: Depende del plan de hosting
- **Velocidad**: 3-10 segundos por consulta

### Límites de OpenAI (Free Tier)
- **Requests por minuto**: 3-20 (varía por modelo)
- **Tokens por minuto**: 40,000-200,000
- **Crédito inicial**: $5

### Hosting Free Tier (Render.com)
- **RAM**: 512 MB
- **CPU**: Compartida
- **Inactividad**: Se suspende después de 15 min
- **Ancho de banda**: 100 GB/mes

---

## 🎯 Recomendaciones para Demo

### Antes de la demo:
1. ✅ Deploy la app con antelación
2. ✅ Verifica que funciona visitando la URL
3. ✅ Carga el documento de ejemplo previamente
4. ✅ Prueba todas las preguntas que harás
5. ✅ Ten backup de internet (hotspot móvil)
6. ✅ Graba video de la demo por si falla internet

### Durante la demo:
1. ✅ Usa preguntas preparadas del `TESTING.md`
2. ✅ Explica mientras la IA procesa
3. ✅ Destaca las fuentes y confianza
4. ✅ Ten plan B (video pregrabado)

---

## 🆘 Contacto de Emergencia

### Si algo falla el día del hackathon:

1. **Verificación rápida**:
   ```powershell
   curl https://tu-app.onrender.com/api/health
   ```

2. **Logs en Render**:
   - Dashboard → Tu app → Logs
   - Buscar errores recientes

3. **Reinicio rápido**:
   - Render dashboard → Manual Deploy
   - O commit vacío: `git commit --allow-empty -m "redeploy"`

4. **Plan B**:
   - Usar video pregrabado de la demo
   - Ejecutar local en laptop (asegurar tener todo listo)

---

## 💡 Consejos de Último Minuto

### Para Presentación
- 🎤 Ensaya tu pitch de 30 segundos
- 📝 Ten notas sobre arquitectura
- 💻 Cierra tabs innecesarias del navegador
- 🔇 Silencia notificaciones
- 🔋 Asegura carga completa de laptop

### Para Jurado
Prepara respuestas para:
- "¿Por qué usaste esta arquitectura?"
- "¿Cómo escala el sistema?"
- "¿Cuáles son las limitaciones?"
- "¿Qué mejoras futuras consideras?"
- "¿Cuál es el costo operativo?"

---

## 📚 Recursos de Aprendizaje

### Si quieres aprender más:
- **LangChain**: https://python.langchain.com/docs
- **FastAPI**: https://fastapi.tiangolo.com/tutorial/
- **FAISS**: https://github.com/facebookresearch/faiss/wiki
- **RAG**: https://www.pinecone.io/learn/retrieval-augmented-generation/
- **OpenAI**: https://platform.openai.com/docs

---

## ✅ Verificación Final

Antes de considerar el proyecto completo:

```powershell
# Test 1: Health check
curl http://localhost:8000/api/health

# Test 2: Cargar documento
# Via UI: Cargar ejemplo_contrato.txt

# Test 3: Hacer consulta
# Via UI: "¿Cuál es el objeto del contrato?"

# Test 4: Verificar respuesta con fuentes
# Debe mostrar respuesta + fuentes + confianza
```

Si todos los tests pasan: **✅ ¡Listo para la demo!**

---

## 🎊 ¡Éxito en el Hackathon!

Recuerda:
- 💪 **Confía en tu trabajo** - Has construido algo funcional
- 🗣️ **Comunica claramente** - La demo es tan importante como el código
- 🐛 **Ten plan B** - Si algo falla, mantén la calma
- 🎯 **Enfócate en el valor** - Explica cómo ayuda a usuarios reales
- 🙌 **Disfruta la experiencia** - Es un aprendizaje invaluable

---

**¿Listo? ¡A brillar! ⭐**

Para comenzar: `python main.py`  
Para dudas: Revisa `QUICKSTART.md`  
Para deploy: Revisa `DEPLOYMENT.md`
