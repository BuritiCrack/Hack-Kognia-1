@echo off
echo 🚀 Iniciando configuración del Asistente Legal RAG...

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python no está instalado. Por favor instálalo primero.
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Crear entorno virtual
echo 📦 Creando entorno virtual...
python -m venv venv

REM Activar entorno virtual
echo 🔧 Activando entorno virtual...
call venv\Scripts\activate.bat

REM Instalar dependencias
echo 📥 Instalando dependencias...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Crear archivo .env si no existe
if not exist .env (
    echo 📝 Creando archivo .env...
    copy .env.example .env
    echo ⚠️  IMPORTANTE: Edita el archivo .env y agrega tu OPENAI_API_KEY
)

REM Crear directorios necesarios
echo 📁 Creando directorios...
if not exist uploads mkdir uploads
if not exist vector_store mkdir vector_store
if not exist static mkdir static

echo.
echo ✅ ¡Configuración completada!
echo.
echo 📋 Próximos pasos:
echo 1. Edita el archivo .env y agrega tu OPENAI_API_KEY
echo 2. Activa el entorno virtual: venv\Scripts\activate
echo 3. Ejecuta la aplicación: python main.py
echo 4. Abre tu navegador en: http://localhost:8000
echo.
pause
