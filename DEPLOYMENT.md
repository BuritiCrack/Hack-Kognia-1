# Guía de Despliegue - Asistente Legal RAG

## 🌐 Opciones de Despliegue

### 1. Render.com (Recomendado - Gratuito)

#### Paso a Paso

1. **Crear cuenta en Render.com**
   - Visita: https://render.com
   - Regístrate con GitHub

2. **Conectar repositorio**
   - Dashboard → New → Web Service
   - Conecta tu cuenta de GitHub
   - Selecciona el repositorio `hack-kognia-rag-legal`

3. **Configurar el servicio**
   ```
   Name: asistente-legal-rag
   Region: Oregon (US West)
   Branch: main
   Runtime: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

4. **Variables de entorno**
   - Click en "Environment"
   - Agregar:
     ```
     OPENAI_API_KEY = tu_api_key_de_openai
     OPENAI_MODEL = gpt-4o-mini
     ```

5. **Plan**
   - Selecciona "Free" ($0/mes)
   - Free tier limitations:
     - 512 MB RAM
     - Shared CPU
     - Inactivity spin down (15 min)

6. **Deploy**
   - Click "Create Web Service"
   - Espera 5-10 minutos
   - Tu URL será: `https://asistente-legal-rag.onrender.com`

#### Limitaciones del Free Tier
- Se suspende después de 15 min de inactividad
- Primera carga puede tardar ~1 minuto
- 512 MB RAM (suficiente para el proyecto)

---

### 2. Railway.app (Alternativa)

#### Paso a Paso

1. **Crear cuenta en Railway.app**
   - Visita: https://railway.app
   - Sign up con GitHub

2. **Nuevo proyecto**
   - Dashboard → New Project
   - Deploy from GitHub repo
   - Selecciona `hack-kognia-rag-legal`

3. **Configuración automática**
   - Railway detecta automáticamente Python
   - Usa el `Procfile` para configurar start command

4. **Variables de entorno**
   - Click en tu servicio → Variables
   - Agregar:
     ```
     OPENAI_API_KEY = tu_api_key_de_openai
     OPENAI_MODEL = gpt-4o-mini
     ```

5. **Generar dominio**
   - Settings → Generate Domain
   - Tu URL será: `https://hack-kognia-rag-legal.up.railway.app`

#### Pricing
- $5 crédito gratuito mensual
- Uso basado en recursos consumidos
- ~$5-10/mes para uso moderado

---

### 3. Fly.io

#### Paso a Paso

1. **Instalar flyctl**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Mac/Linux
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   flyctl auth login
   ```

3. **Crear app**
   ```bash
   cd hack-kognia-rag-legal
   flyctl launch
   ```

4. **Configurar fly.toml**
   ```toml
   app = "asistente-legal-rag"
   
   [build]
   
   [env]
     PORT = "8000"
   
   [[services]]
     internal_port = 8000
     protocol = "tcp"
   
     [[services.ports]]
       port = 80
       handlers = ["http"]
   
     [[services.ports]]
       port = 443
       handlers = ["tls", "http"]
   ```

5. **Agregar secrets**
   ```bash
   flyctl secrets set OPENAI_API_KEY=tu_api_key
   flyctl secrets set OPENAI_MODEL=gpt-4o-mini
   ```

6. **Deploy**
   ```bash
   flyctl deploy
   ```

---

### 4. Heroku

#### Paso a Paso

1. **Crear cuenta en Heroku**
   - https://heroku.com

2. **Instalar Heroku CLI**
   ```bash
   # Windows
   https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **Login y crear app**
   ```bash
   heroku login
   cd hack-kognia-rag-legal
   heroku create asistente-legal-rag
   ```

4. **Configurar variables**
   ```bash
   heroku config:set OPENAI_API_KEY=tu_api_key
   heroku config:set OPENAI_MODEL=gpt-4o-mini
   ```

5. **Deploy**
   ```bash
   git push heroku main
   ```

#### Pricing
- Free tier eliminado en 2022
- Mínimo $7/mes (Eco Dynos)

---

### 5. Google Cloud Run

#### Paso a Paso

1. **Crear Dockerfile**
   ```dockerfile
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   COPY . .
   
   CMD uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

2. **Build y push**
   ```bash
   gcloud builds submit --tag gcr.io/PROJECT_ID/asistente-legal-rag
   ```

3. **Deploy**
   ```bash
   gcloud run deploy asistente-legal-rag \
     --image gcr.io/PROJECT_ID/asistente-legal-rag \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars OPENAI_API_KEY=tu_key
   ```

#### Pricing
- 2 millones de requests gratis/mes
- Pay as you go después

---

## ⚙️ Configuración Post-Despliegue

### 1. Verificar Deployment
```bash
# Test health endpoint
curl https://tu-app-url.com/api/health
```

### 2. Test de funcionalidad
1. Visita la URL de tu app
2. Carga un documento de prueba
3. Realiza una consulta
4. Verifica respuesta y fuentes

### 3. Monitoreo
- **Render**: Dashboard → Logs
- **Railway**: Service → Logs
- **Fly.io**: `flyctl logs`

### 4. Custom Domain (Opcional)
- Render: Settings → Custom Domain
- Railway: Settings → Domains
- Agrega CNAME record en tu DNS

---

## 🔧 Troubleshooting

### Error: "Module not found"
- Verifica que `requirements.txt` esté completo
- Rebuild la aplicación

### Error: "OpenAI API key not found"
- Verifica variables de entorno
- Reinicia el servicio

### App muy lenta
- Plan gratuito tiene limitaciones
- Considera upgrade a paid tier
- Optimiza chunk_size en `rag_system.py`

### Out of Memory
- Reduce `chunk_size`
- Limita número de documentos simultáneos
- Upgrade a plan con más RAM

---

## 📊 Costos Estimados

| Plataforma | Free Tier | Paid (Básico) | Límites Free |
|------------|-----------|---------------|--------------|
| Render.com | ✅ Gratis | $7/mes | 512 MB RAM |
| Railway.app | $5 crédito | ~$10/mes | Uso medido |
| Fly.io | $5 crédito | ~$5/mes | Uso medido |
| Heroku | ❌ No | $7/mes | N/A |
| Cloud Run | ✅ Gratis | Pay-as-go | 2M requests |

**Costos adicionales:**
- OpenAI API: ~$0.01-0.10 por consulta (depende de uso)
- Dominio custom: ~$12/año (opcional)

---

## 🎯 Recomendación Final

**Para Hackathon/Demo:**
- **Primera opción**: Render.com (free tier)
  - Fácil setup
  - URL pública inmediata
  - No requiere tarjeta de crédito

**Para Producción:**
- **Railway.app** o **Google Cloud Run**
  - Mejor performance
  - Escalabilidad
  - Monitoreo avanzado

---

## 📝 Checklist de Despliegue

- [ ] Código pusheado a GitHub
- [ ] `.env` no incluido en repo (verificar `.gitignore`)
- [ ] `requirements.txt` actualizado
- [ ] `Procfile` configurado
- [ ] Cuenta creada en plataforma elegida
- [ ] Repositorio conectado
- [ ] Variables de entorno configuradas
- [ ] OPENAI_API_KEY válida
- [ ] Build exitoso
- [ ] URL pública funcionando
- [ ] Test de carga de documento
- [ ] Test de consulta
- [ ] Logs sin errores

---

## 🆘 Soporte

Si tienes problemas con el despliegue:
1. Revisa los logs del servicio
2. Verifica variables de entorno
3. Consulta documentación de la plataforma
4. Abre un issue en el repositorio
