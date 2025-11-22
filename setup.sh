#!/bin/bash

echo "🚀 Iniciando configuración del Asistente Legal RAG..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado. Por favor instálalo primero."
    exit 1
fi

echo "✅ Python encontrado: $(python3 --version)"

# Crear entorno virtual
echo "📦 Creando entorno virtual..."
python3 -m venv venv

# Activar entorno virtual
echo "🔧 Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "📥 Instalando dependencias..."
pip install --upgrade pip
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    echo "📝 Creando archivo .env..."
    cp .env.example .env
    echo "⚠️  IMPORTANTE: Edita el archivo .env y agrega tu OPENAI_API_KEY"
fi

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p uploads
mkdir -p vector_store
mkdir -p static

echo ""
echo "✅ ¡Configuración completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Edita el archivo .env y agrega tu OPENAI_API_KEY"
echo "2. Activa el entorno virtual: source venv/bin/activate"
echo "3. Ejecuta la aplicación: python main.py"
echo "4. Abre tu navegador en: http://localhost:8000"
echo ""
