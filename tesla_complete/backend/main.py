from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import os
import uvicorn

app = FastAPI(title="Tesla Electricidad API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ChatMessage(BaseModel):
    message: str

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/tesla.db")
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_message TEXT,
            bot_response TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    conn.commit()
    conn.close()

@app.on_event("startup")
async def startup():
    init_db()
    print("Tesla API iniciada en http://localhost:8000")

@app.get("/")
async def root():
    return {"message": "Tesla Electricidad API", "status": "online"}

@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(message_data: ChatMessage):
    try:
        response = process_chat(message_data.message)
        
        conn = sqlite3.connect("data/tesla.db")
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_message, bot_response) VALUES (?, ?)",
            (message_data.message, response)
        )
        conn.commit()
        conn.close()
        
        return {"success": True, "response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/dashboard")
async def get_dashboard(month: int = 8):
    data = {
        1: {"itse": 15, "pozo_tierra": 8, "mantenimiento": 12, "incendios": 5, "clientes": 25, "satisfaccion": 95},
        2: {"itse": 18, "pozo_tierra": 10, "mantenimiento": 15, "incendios": 7, "clientes": 28, "satisfaccion": 96},
        3: {"itse": 22, "pozo_tierra": 12, "mantenimiento": 18, "incendios": 8, "clientes": 32, "satisfaccion": 97},
        4: {"itse": 25, "pozo_tierra": 14, "mantenimiento": 20, "incendios": 10, "clientes": 35, "satisfaccion": 96},
        5: {"itse": 28, "pozo_tierra": 16, "mantenimiento": 22, "incendios": 12, "clientes": 38, "satisfaccion": 98},
        6: {"itse": 32, "pozo_tierra": 18, "mantenimiento": 25, "incendios": 14, "clientes": 42, "satisfaccion": 97},
        7: {"itse": 35, "pozo_tierra": 20, "mantenimiento": 28, "incendios": 16, "clientes": 45, "satisfaccion": 98},
        8: {"itse": 38, "pozo_tierra": 22, "mantenimiento": 30, "incendios": 18, "clientes": 48, "satisfaccion": 99}
    }
    
    return {"success": True, "data": data.get(month, data[8])}

def process_chat(message: str) -> str:
    lower = message.lower()
    
    if any(word in lower for word in ['itse', 'certificado']):
        return """CERTIFICADO ITSE - Informacion Completa

Costos Referenciales:
• Pago municipalidad: S/ 218.00
• Nuestro servicio: S/ 300.00 - S/ 500.00
• Total aproximado: S/ 518.00 - S/ 718.00

Tiempo estimado: 5-10 dias habiles

Proceso incluye:
1. Evaluacion tecnica completa
2. Elaboracion de planos (si es necesario)  
3. Gestion del tramite municipal
4. Seguimiento hasta obtencion

Te gustaria agendar una visita tecnica gratuita?
WhatsApp: +51 906 315 961"""

    elif any(word in lower for word in ['pozo', 'tierra']):
        return """POZO DE TIERRA - Sistema de Seguridad

Precio referencial: S/ 1,500 - S/ 2,500

El costo varia segun:
• Tipo de terreno (arcilloso, arenoso, rocoso)
• Resistividad del suelo medida
• Profundidad requerida
• Materiales necesarios

Proceso de instalacion:
1. Medicion de resistividad del terreno
2. Diseno del sistema segun normativa
3. Excavacion e instalacion
4. Pruebas y certificacion final

Realizamos visita tecnica gratuita para precio exacto.
WhatsApp: +51 906 315 961"""

    elif any(word in lower for word in ['mantenimiento', 'reparacion']):
        return """MANTENIMIENTO ELECTRICO - Preventivo y Correctivo

Tipos de mantenimiento:
• Preventivo: S/ 200 - S/ 400 - Inspecciones programadas
• Correctivo: S/ 500 - S/ 1,200 - Reparacion de fallas  
• Emergencia 24h: S/ 150/hora + materiales

Que revisamos:
• Tableros electricos y conexiones
• Sistema de proteccion y puesta a tierra
• Medicion de aislamientos
• Limpieza y ajuste de contactos

Plan anual: 15% descuento
WhatsApp: +51 906 315 961"""

    elif any(word in lower for word in ['precio', 'costo']):
        return """LISTA DE PRECIOS REFERENCIALES 2024

CERTIFICADO ITSE:
• Comercio basico: S/ 518 - 718
• Restaurante/Bar: S/ 718 - 1,218  
• Industrial: S/ 1,218 - 2,218

POZO DE TIERRA:
• Residencial: S/ 1,200 - 1,800
• Comercial: S/ 1,500 - 2,500
• Industrial: S/ 2,500 - 4,500

MANTENIMIENTO:
• Preventivo: S/ 200 - 400
• Correctivo: S/ 500 - 1,200
• Plan anual: 15% descuento

SISTEMA CONTRA INCENDIOS:
• Deteccion basica: S/ 1,500+
• Sistema completo: Cotizacion personalizada

Precios incluyen materiales basicos. Pueden variar segun especificaciones.
WhatsApp: +51 906 315 961"""

    else:
        return """Hola! Soy Tesla IA, tu asistente especializado en servicios electricos.

En que puedo ayudarte?
• Certificado ITSE - Gestion completa
• Pozo de Tierra - Seguridad electrica  
• Mantenimiento - Preventivo y correctivo
• Sistema Contra Incendios - Proteccion total
• Consultar precios - Rangos referenciales

Empresa confiable: +10 anos de experiencia, +500 proyectos exitosos
WhatsApp directo: +51 906 315 961

Escribe tu consulta o selecciona un tema de interes."""

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
