#!/usr/bin/env python3
"""
Script de configuración para Tesla Electricidad
Configura el entorno de desarrollo e instala dependencias
"""

import os
import sys
import subprocess
import platform
import venv
from pathlib import Path

# Configuración
PROJECT_NAME = "tesla_electricidad"
VENV_DIR = "venv"
REQUIREMENTS = [
    # Backend
    "fastapi==0.104.1",
    "uvicorn==0.24.0",
    "sqlalchemy==2.0.23",
    "python-jose[cryptography]==3.3.0",
    "passlib[bcrypt]==1.7.4",
    "python-multipart==0.0.6",
    "aiofiles==23.2.1",
    
    # IA APIs
    "openai==1.3.0",
    "google-generativeai==0.3.1",
    
    # Comunicación
    "twilio==8.12.0",
    "sendgrid==6.11.0",
    "python-dotenv==1.0.0",
    
    # Base de datos
    "databases[sqlite]==0.8.0",
    "alembic==1.12.1",
    
    # Desarrollo
    "pytest==7.4.3",
    "black==23.11.0",
    "isort==5.12.0",
    "mypy==1.7.0",
]

def print_header(text):
    """Muestra un encabezado estilizado"""
    print(f"\n{'='*50}")
    print(f"{text.upper()}")
    print(f"{'='*50}")

def check_python_version():
    """Verifica la versión de Python"""
    print_header("Verificando versión de Python")
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        sys.exit(1)
    print(f"✅ Python {sys.version}")

def create_virtualenv():
    """Crea un entorno virtual"""
    print_header("Creando entorno virtual")
    if os.path.exists(VENV_DIR):
        print(f"✅ El entorno virtual ya existe en {VENV_DIR}")
        return
    
    print(f"Creando entorno virtual en {VENV_DIR}...")
    venv.create(VENV_DIR, with_pip=True)
    print("✅ Entorno virtual creado")

def install_dependencies():
    """Instala las dependencias del proyecto"""
    print_header("Instalando dependencias")
    
    # Determinar el comando de pip según el SO
    pip_cmd = os.path.join(VENV_DIR, "Scripts" if os.name == 'nt' else "bin", "pip")
    if os.name == 'nt':
        pip_cmd += ".exe"
    
    # Instalar dependencias
    try:
        subprocess.check_call([pip_cmd, "install", "--upgrade", "pip"])
        subprocess.check_call([pip_cmd, "install"] + REQUIREMENTS)
        print("✅ Dependencias instaladas correctamente")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        sys.exit(1)

def create_env_file():
    """Crea el archivo .env con variables de ejemplo"""
    env_file = ".env"
    if os.path.exists(env_file):
        print("✅ El archivo .env ya existe")
        return
    
    env_content = """# Configuración de la aplicación
DEBUG=True
SECRET_KEY=tu_clave_secreta_muy_segura_aqui

# Base de datos
DATABASE_URL=sqlite:///./tesla_electricidad.db

# OpenAI
OPENAI_API_KEY=tu_api_key_aqui

# Google Generative AI
GOOGLE_API_KEY=tu_api_key_aqui

# Twilio (WhatsApp)
TWILIO_ACCOUNT_SID=tu_account_sid
TWILIO_AUTH_TOKEN=tu_auth_token
TWILIO_WHATSAPP_NUMBER=+1234567890

# SendGrid
SENDGRID_API_KEY=tu_api_key_aqui
EMAIL_FROM=noreply@teslaelectricidad.com
"""
    try:
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Archivo .env creado con valores de ejemplo")
    except Exception as e:
        print(f"❌ Error al crear el archivo .env: {e}")

def create_project_structure():
    """Crea la estructura de directorios del proyecto"""
    print_header("Creando estructura del proyecto")
    dirs = [
        "app",
        "app/api",
        "app/core",
        "app/models",
        "app/schemas",
        "app/services",
        "app/static",
        "app/static/css",
        "app/static/js",
        "app/static/images",
        "app/templates",
        "tests",
        "migrations",
    ]
    
    for directory in dirs:
        try:
            os.makedirs(directory, exist_ok=True)
            print(f"✅ Directorio creado: {directory}")
        except Exception as e:
            print(f"❌ Error al crear el directorio {directory}: {e}")

def create_vscode_settings():
    """Crea la configuración de VS Code"""
    vscode_dir = ".vscode"
    settings_file = os.path.join(vscode_dir, "settings.json")
    
    try:
        os.makedirs(vscode_dir, exist_ok=True)
        
        settings = {
            "python.defaultInterpreterPath": "${workspaceFolder}/venv/Scripts/python.exe" if os.name == 'nt' else "${workspaceFolder}/venv/bin/python",
            "python.linting.enabled": True,
            "python.linting.pylintEnabled": False,
            "python.linting.mypyEnabled": True,
            "python.formatting.provider": "black",
            "python.formatting.blackPath": "${workspaceFolder}/venv/Scripts/black" if os.name == 'nt' else "${workspaceFolder}/venv/bin/black",
            "python.linting.mypyPath": "${workspaceFolder}/venv/Scripts/mypy" if os.name == 'nt' else "${workspaceFolder}/venv/bin/mypy",
            "editor.formatOnSave": True,
            "editor.codeActionsOnSave": {
                "source.organizeImports": True
            },
            "python.analysis.typeCheckingMode": "basic",
            "files.exclude": {
                "**/__pycache__": True,
                "**/.pytest_cache": True,
                "**/*.pyc": True,
                "**/*.pyo": True,
                "**/*.pyd": True,
                "**/.mypy_cache": True,
                "**/.venv": True,
                "venv": True
            }
        }
        
        with open(settings_file, 'w') as f:
            import json
            json.dump(settings, f, indent=4)
            
        print("✅ Configuración de VS Code creada")
    except Exception as e:
        print(f"❌ Error al crear la configuración de VS Code: {e}")

def create_readme():
    """Crea o actualiza el archivo README.md"""
    readme_content = """# Tesla Electricidad - Proyecto de Automatización

Sistema integral para la gestión de servicios eléctricos con chatbot inteligente.

## 🚀 Características

- Chatbot conversacional con IA
- Gestión de clientes y citas
- Integración con WhatsApp y correo electrónico
- Dashboard administrativo
- API RESTful con FastAPI

## 🛠️ Requisitos

- Python 3.8+
- Node.js 16+ (para el frontend)
- Docker (opcional, para desarrollo con contenedores)

## 🚀 Instalación

1. Clona el repositorio:
   ```bash
   git clone https://github.com/tu-usuario/tesla-electricidad.git
   cd tesla-electricidad
   ```

2. Configura el entorno de desarrollo:
   ```bash
   # En Windows
   .\setup_project.py
   
   # En Linux/MacOS
   python3 setup_project.py
   ```

3. Activa el entorno virtual:
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/MacOS
   source venv/bin/activate
   ```

4. Configura las variables de entorno en el archivo `.env`

5. Inicia el servidor de desarrollo:
   ```bash
   uvicorn app.main:app --reload
   ```

6. Abre tu navegador en http://localhost:8000

## 🧪 Ejecutar pruebas

```bash
pytest
```

## 🏗️ Estructura del Proyecto

```
.
├── app/                    # Código fuente de la aplicación
│   ├── api/               # Endpoints de la API
│   ├── core/              # Configuración y utilidades
│   ├── models/            # Modelos de base de datos
│   ├── schemas/           # Esquemas Pydantic
│   ├── services/          # Lógica de negocio
│   ├── static/            # Archivos estáticos (CSS, JS, imágenes)
│   └── templates/         # Plantillas HTML
├── tests/                 # Pruebas unitarias e integrales
├── migrations/            # Migraciones de base de datos
├── .env                   # Variables de entorno
├── .gitignore
├── requirements.txt       # Dependencias de Python
└── README.md              # Este archivo
```

## 📝 Licencia

Este proyecto está bajo la Licencia MIT.
"""
    
    try:
        with open("README.md", "w", encoding="utf-8") as f:
            f.write(readme_content)
        print("✅ Archivo README.md creado")
    except Exception as e:
        print(f"❌ Error al crear el archivo README.md: {e}")

def main():
    """Función principal"""
    try:
        print_header("Iniciando configuración del proyecto Tesla Electricidad")
        
        # Verificar versión de Python
        check_python_version()
        
        # Crear entorno virtual
        create_virtualenv()
        
        # Instalar dependencias
        install_dependencies()
        
        # Crear archivo .env
        create_env_file()
        
        # Crear estructura de directorios
        create_project_structure()
        
        # Configurar VS Code
        create_vscode_settings()
        
        # Crear README
        create_readme()
        
        print_header("✅ Configuración completada con éxito")
        print("\n📌 Siguientes pasos:")
        print("1. Activa el entorno virtual:")
        print("   - Windows: .\\venv\\Scripts\\activate")
        print("   - Linux/Mac: source venv/bin/activate")
        print("\n2. Configura las variables en el archivo .env")
        print("3. Ejecuta la aplicación con: uvicorn app.main:app --reload")
        print("\n¡Listo para desarrollar! 🚀")
        
    except Exception as e:
        print(f"\n❌ Error durante la configuración: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
