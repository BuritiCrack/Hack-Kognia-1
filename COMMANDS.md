# 🛠️ Comandos Útiles

## Instalación y Configuración

### Crear entorno virtual
```powershell
python -m venv venv
```

### Activar entorno virtual
```powershell
# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat

# Linux/Mac
source venv/bin/activate
```

### Instalar dependencias
```powershell
pip install -r requirements.txt
```

### Actualizar pip
```powershell
python -m pip install --upgrade pip
```

---

## Ejecución

### Iniciar servidor de desarrollo
```powershell
python main.py
```

### Iniciar con uvicorn directamente
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Iniciar en modo producción
```powershell
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## Testing

### Ejecutar script de prueba
```powershell
python test_rag.py
```

### Test de health check
```powershell
curl http://localhost:8000/api/health
```

### Test de status
```powershell
curl http://localhost:8000/api/status
```

### Test con Invoke-WebRequest (PowerShell)
```powershell
Invoke-WebRequest -Uri http://localhost:8000/api/health | ConvertFrom-Json
```

---

## API Testing con curl

### Upload documento
```powershell
curl -X POST http://localhost:8000/api/upload `
  -F "files=@ejemplo_contrato.txt"
```

### Hacer consulta
```powershell
curl -X POST http://localhost:8000/api/query `
  -H "Content-Type: application/json" `
  -d '{\"question\": \"¿Cuál es el objeto del contrato?\"}'
```

### Reiniciar sistema
```powershell
curl -X POST http://localhost:8000/api/reset
```

---

## Git Commands

### Inicializar repositorio
```powershell
git init
git add .
git commit -m "Initial commit: Asistente Legal RAG"
```

### Crear repositorio en GitHub y subir
```powershell
git remote add origin https://github.com/tu-usuario/hack-kognia-rag-legal.git
git branch -M main
git push -u origin main
```

### Actualizar cambios
```powershell
git add .
git commit -m "Descripción del cambio"
git push
```

---

## Deployment Commands

### Render.com (via Git)
```powershell
# 1. Push a GitHub
git push origin main

# 2. En Render.com dashboard:
#    - Conectar repositorio
#    - Auto-deploy habilitado
```

### Railway.app
```powershell
# Instalar CLI
npm install -g @railway/cli

# Login
railway login

# Iniciar proyecto
railway init

# Deploy
railway up
```

### Fly.io
```powershell
# Instalar flyctl
iwr https://fly.io/install.ps1 -useb | iex

# Login
flyctl auth login

# Launch
flyctl launch

# Deploy
flyctl deploy
```

---

## Mantenimiento

### Ver paquetes instalados
```powershell
pip list
```

### Actualizar requirements.txt
```powershell
pip freeze > requirements.txt
```

### Verificar versión de Python
```powershell
python --version
```

### Limpiar cache de Python
```powershell
# Windows
Get-ChildItem -Path . -Include __pycache__ -Recurse -Force | Remove-Item -Force -Recurse

# Linux/Mac
find . -type d -name __pycache__ -exec rm -rf {} +
```

---

## Debugging

### Ver logs en tiempo real
```powershell
# Ejecutar con nivel de log DEBUG
uvicorn main:app --reload --log-level debug
```

### Ver variables de entorno
```powershell
# Windows
Get-Content .env

# Linux/Mac
cat .env
```

### Verificar puertos en uso
```powershell
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000
```

### Matar proceso en puerto
```powershell
# Windows (reemplazar PID)
taskkill /PID <PID> /F

# Linux/Mac
kill -9 $(lsof -t -i:8000)
```

---

## Optimización

### Instalar solo dependencias de producción
```powershell
pip install --no-dev -r requirements.txt
```

### Reducir tamaño de instalación
```powershell
pip install --no-cache-dir -r requirements.txt
```

### Verificar uso de memoria
```powershell
# Durante ejecución, abrir otra terminal:
# Windows
tasklist /FI "IMAGENAME eq python.exe"

# Linux/Mac
ps aux | grep python
```

---

## Desarrollo

### Formatear código con Black
```powershell
pip install black
black *.py
```

### Lint con flake8
```powershell
pip install flake8
flake8 *.py
```

### Type checking con mypy
```powershell
pip install mypy
mypy *.py
```

---

## Documentación

### Generar documentación de API
```powershell
# FastAPI genera automáticamente
# Acceder a:
# http://localhost:8000/docs (Swagger UI)
# http://localhost:8000/redoc (ReDoc)
```

### Ver estructura de directorios
```powershell
# Windows
tree /F

# Linux/Mac
tree
```

---

## Backup y Restauración

### Backup de vector store
```powershell
# Copiar directorio vector_store
Copy-Item -Path vector_store -Destination vector_store_backup -Recurse
```

### Restaurar vector store
```powershell
# Restaurar desde backup
Copy-Item -Path vector_store_backup -Destination vector_store -Recurse
```

### Backup de uploads
```powershell
Copy-Item -Path uploads -Destination uploads_backup -Recurse
```

---

## Variables de Entorno

### Establecer temporalmente (sesión actual)
```powershell
# Windows PowerShell
$env:OPENAI_API_KEY = "sk-tu-key"

# Windows CMD
set OPENAI_API_KEY=sk-tu-key

# Linux/Mac
export OPENAI_API_KEY=sk-tu-key
```

### Cargar desde .env
```powershell
# Ya implementado en main.py con python-dotenv
# Solo asegúrate que .env existe
```

---

## Monitoreo

### Ver uso de CPU y RAM
```powershell
# Durante ejecución en otra terminal
# Windows
Get-Process python

# Linux/Mac
top -p $(pgrep python)
```

### Contar requests
```powershell
# Ver logs y contar
# Implementar logging en main.py si es necesario
```

---

## Troubleshooting Rápido

### Problema: ModuleNotFoundError
```powershell
# Solución: Reinstalar dependencias
pip install -r requirements.txt
```

### Problema: Puerto en uso
```powershell
# Solución: Cambiar puerto en .env
echo "PORT=3000" >> .env
```

### Problema: OpenAI API error
```powershell
# Solución: Verificar API key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print(os.getenv('OPENAI_API_KEY'))"
```

### Problema: Out of memory
```powershell
# Solución: Reducir chunk_size en rag_system.py
# Editar línea 65: chunk_size=500
```

---

## Atajos Útiles

### Todo en uno: Limpiar, instalar y ejecutar
```powershell
# Limpiar
Remove-Item -Path venv -Recurse -Force -ErrorAction SilentlyContinue

# Crear entorno
python -m venv venv

# Activar
venv\Scripts\Activate.ps1

# Instalar
pip install -r requirements.txt

# Ejecutar
python main.py
```

### Verificación completa
```powershell
# 1. Check Python
python --version

# 2. Check env
Get-Content .env

# 3. Check dependencies
pip list

# 4. Test import
python -c "import fastapi, langchain, faiss; print('OK')"

# 5. Run
python main.py
```

---

## Scripts Personalizados

### Crear alias en PowerShell (Opcional)
```powershell
# Agregar a $PROFILE
function Start-RAG {
    cd "D:\jmbur\Documents\Talento Tech\Hack-Kognia 1.0\hack-kognia-rag-legal"
    venv\Scripts\Activate.ps1
    python main.py
}

# Usar con:
Start-RAG
```

---

## Comandos de Producción

### Health check automático
```powershell
# Script de monitoreo
while ($true) {
    $response = Invoke-WebRequest -Uri https://tu-app.onrender.com/api/health
    Write-Host "$(Get-Date): $($response.StatusCode)"
    Start-Sleep -Seconds 60
}
```

### Logs en producción (Render)
```bash
# Ver logs en tiempo real
render logs -a tu-app
```

---

**Guarda este archivo para referencia rápida! 📌**
