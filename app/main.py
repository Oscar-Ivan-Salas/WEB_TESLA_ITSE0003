from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pathlib import Path
import uvicorn

# Crear la aplicación FastAPI
app = FastAPI(
    title="Tesla Electricidad API",
    description="API para el sistema de Tesla Electricidad",
    version="1.0.0"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar archivos estáticos
app.mount(
    "/static",
    StaticFiles(directory=str(Path(__file__).parent / "static")),
    name="static"
)

# Configurar templates
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# Ruta principal
@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Ruta de salud
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# Si se ejecuta este archivo directamente
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
