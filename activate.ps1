# Script de activación para PowerShell

# Verificar si el entorno virtual existe
$venvPath = ".\venv"
if (-not (Test-Path $venvPath)) {
    Write-Host "❌ No se encontró el entorno virtual. Ejecuta primero setup_project.py" -ForegroundColor Red
    exit 1
}

# Activar el entorno virtual
$activateScript = "$venvPath\Scripts\Activate.ps1"
if (Test-Path $activateScript) {
    Write-Host "✅ Activando entorno virtual..." -ForegroundColor Green
    . $activateScript
    
    # Verificar que se activó correctamente
    if ($env:VIRTUAL_ENV) {
        Write-Host "✅ Entorno virtual activado: $($env:VIRTUAL_ENV)" -ForegroundColor Green
        Write-Host "📌 Para desactivar, escribe: deactivate" -ForegroundColor Cyan
        
        # Iniciar el servidor de desarrollo
        $startServer = Read-Host "¿Deseas iniciar el servidor de desarrollo? (s/n)"
        if ($startServer -eq 's') {
            Write-Host "🚀 Iniciando servidor de desarrollo..." -ForegroundColor Cyan
            uvicorn app.main:app --reload
        }
    } else {
        Write-Host "❌ No se pudo activar el entorno virtual" -ForegroundColor Red
    }
} else {
    Write-Host "❌ No se encontró el script de activación" -ForegroundColor Red
}
