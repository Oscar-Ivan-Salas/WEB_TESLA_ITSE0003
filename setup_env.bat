@echo off
echo Configurando entorno para Tesla Electricidad...

:: Verificar si Python está instalado
python --version >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Error: Python no está instalado o no está en el PATH.
    echo Por favor, instala Python 3.8 o superior desde https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Crear y activar entorno virtual
echo Creando entorno virtual...
python -m venv venv
call venv\Scripts\activate

:: Instalar dependencias
echo Instalando dependencias...
pip install --upgrade pip
pip install -r backend/requirements.txt

echo.
echo ¡Configuración completada con éxito!
echo.
echo Para activar el entorno virtual, ejecuta:
echo venv\Scripts\activate

echo.
echo Para iniciar el proyecto, ejecuta:
echo docker-compose up --build

pause
