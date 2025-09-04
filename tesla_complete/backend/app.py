from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
import sqlite3
import json
import os
import asyncio
import httpx
from datetime import datetime, timedelta
import logging
from contextlib import asynccontextmanager
import uvicorn

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Models Pydantic
class ChatMessage(BaseModel):
    message: str
    context: Optional[str] = None
    stage: Optional[str] = "greeting"
    history: Optional[List[Dict]] = []

class ContactForm(BaseModel):
    nombre: str
    telefono: str
    email: Optional[EmailStr] = None
    servicio: str
    mensaje: Optional[str] = None

class Lead(BaseModel):
    nombre: str
    telefono: str
    email: Optional[str] = None
    servicio: str
    presupuesto: Optional[float] = None
    fecha_cita: Optional[str] = None
    estado: str = "nuevo"

class WhatsAppMessage(BaseModel):
    to: str
    message: str
    template: Optional[str] = None

# Base de conocimiento especializada
KNOWLEDGE_BASE = {
    "servicios": {
        "itse": {
            "descripcion": "Inspección Técnica de Seguridad en Edificaciones",
            "tipos": ["ITSE Básica", "ITSE de Detalle", "ITSE Ex-Post"],
            "sectores": {
                "restaurante": {"precio_min": 800, "precio_max": 1200, "tiempo": "7-10 días", "riesgo": "MEDIO"},
                "comercio": {"precio_min": 600, "precio_max": 1000, "tiempo": "5-8 días", "riesgo": "BAJO"},
                "industria": {"precio_min": 1500, "precio_max": 3000, "tiempo": "10-15 días", "riesgo": "ALTO"},
                "vivienda": {"precio_min": 400, "precio_max": 800, "tiempo": "3-5 días", "riesgo": "BAJO"}
            },
            "documentos": ["Planos arquitectónicos", "Memoria descriptiva", "Certificado final"],
            "normativas": ["RNE A.130", "CNE Utilización", "NTP 370.052"]
        },
        "instalaciones": {
            "descripcion": "Instalaciones eléctricas completas",
            "tipos": ["Residencial", "Comercial", "Industrial"],
            "precios": {
                "punto_residencial": 85,
                "punto_comercial": 120,
                "punto_industrial": 150,
                "tablero_principal": 800,
                "acometida": 1200
            },
            "servicios": ["Cableado", "Tableros", "Tomacorrientes", "Iluminación", "Puesta a tierra"]
        },
        "automatizacion": {
            "descripcion": "Sistemas de automatización y domótica",
            "tipos": ["Domótica residencial", "Automatización comercial", "Control industrial"],
            "sistemas": {
                "luces": {"precio": 300, "descripcion": "Control inteligente iluminación"},
                "sensores": {"precio": 150, "descripcion": "Sensores movimiento y presencia"},
                "camaras": {"precio": 500, "descripcion": "Sistema videovigilancia IP"},
                "alarmas": {"precio": 800, "descripcion": "Sistema alarma integrado"},
                "climatizacion": {"precio": 1200, "descripcion": "Control temperatura automático"}
            },
            "paquetes": {
                "basico": {"precio": 2500, "incluye": ["luces", "sensores"]},
                "completo": {"precio": 4500, "incluye": ["luces", "sensores", "camaras"]},
                "premium": {"precio": 7500, "incluye": ["luces", "sensores", "camaras", "alarmas", "climatizacion"]}
            }
        },
        "mantenimiento": {
            "descripcion": "Mantenimiento eléctrico preventivo y correctivo",
            "tipos": ["Preventivo", "Correctivo", "Predictivo"],
            "planes": {
                "mensual": {"precio": 300, "visitas": 1, "incluye": ["Revisión tableros", "Medición voltajes"]},
                "trimestral": {"precio": 800, "visitas": 4, "incluye": ["Todo mensual", "Limpieza contactos"]},
                "semestral": {"precio": 1400, "visitas": 2, "incluye": ["Todo anterior", "Reporte técnico"]}
            }
        }
    }
}

# Configuración API Keys (variables de entorno)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TWILIO_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
WHATSAPP_NUMBER = os.getenv("WHATSAPP_NUMBER", "+14155238886")

class DatabaseManager:
    def __init__(self, db_path: str = "backend/data/tesla.db"):
        self.db_path = db_path
        self.init_database()
    
    def get_connection(self):
        return sqlite3.connect(self.db_path)
    
    def init_database(self):
        """Inicializar base de datos con todas las tablas"""
        # Crear directorio de datos si no existe
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Tabla conversaciones
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS conversations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                message TEXT,
                response TEXT,
                stage TEXT,
                context TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla leads
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                telefono TEXT NOT NULL,
                email TEXT,
                servicio TEXT NOT NULL,
                presupuesto REAL,
                fecha_cita TEXT,
                estado TEXT DEFAULT 'nuevo',
                notas TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Tabla citas
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS citas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                lead_id INTEGER,
                fecha_hora DATETIME,
                especialista TEXT,
                estado TEXT DEFAULT 'programada',
                notas TEXT,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (lead_id) REFERENCES leads (id)
            )
        ''')
        
        # Tabla servicios (para dashboard)
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS servicios_stats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mes INTEGER,
                año INTEGER,
                itse INTEGER DEFAULT 0,
                instalaciones INTEGER DEFAULT 0,
                automatizacion INTEGER DEFAULT 0,
                mantenimiento INTEGER DEFAULT 0
            )
        ''')
        
        # Insertar datos demo para dashboard
        self._insert_demo_data(cursor)
        
        conn.commit()
        conn.close()
    
    def _insert_demo_data(self, cursor):
        """Insertar datos demo para el dashboard"""
        demo_data = [
            (1, 2024, 12, 8, 3, 5),  # Enero
            (2, 2024, 15, 12, 5, 8),  # Febrero
            (3, 2024, 18, 15, 7, 12),  # Marzo
            (4, 2024, 22, 18, 9, 15),  # Abril
            (5, 2024, 28, 22, 12, 18),  # Mayo
            (6, 2024, 25, 20, 8, 14),  # Junio
            (7, 2024, 30, 25, 15, 20),  # Julio
            (8, 2024, 35, 28, 18, 25)  # Agosto
        ]
        
        cursor.execute("SELECT COUNT(*) FROM servicios_stats")
        if cursor.fetchone()[0] == 0:
            cursor.executemany(
                "INSERT INTO servicios_stats (mes, año, itse, instalaciones, automatizacion, mantenimiento) VALUES (?, ?, ?, ?, ?, ?)",
                demo_data
            )

class AIService:
    def __init__(self):
        self.openai_available = bool(OPENAI_API_KEY)
        self.gemini_available = bool(GEMINI_API_KEY)
    
    async def get_ai_response(self, message: str, context: str = None, history: List[Dict] = None) -> Dict:
        """Obtener respuesta de IA con fallback"""
        
        # Preparar contexto especializado
        specialized_context = self._build_context(context, message)
        
        # Intentar OpenAI primero
        if self.openai_available:
            try:
                return await self._openai_response(message, specialized_context, history)
            except Exception as e:
                logger.error(f"OpenAI error: {e}")
        
        # Fallback a Gemini
        if self.gemini_available:
            try:
                return await self._gemini_response(message, specialized_context, history)
            except Exception as e:
                logger.error(f"Gemini error: {e}")
        
        # Fallback local
        return self._local_response(message, context)
    
    def _build_context(self, context: str, message: str) -> str:
        """Construir contexto especializado para Tesla Electricidad"""
        base_context = """
        Eres TeslaBot, asistente especializado de Tesla Electricidad y Automatización S.A.C.
        Empresa líder en servicios eléctricos en Huancayo, Perú.
        
        SERVICIOS PRINCIPALES:
        1. ITSE (Inspección Técnica Seguridad Edificaciones)
        2. Instalaciones eléctricas completas
        3. Automatización y domótica
        4. Mantenimiento eléctrico
        
        PERSONALIDAD: Profesional, técnico, confiable, orientado a resultados.
        OBJETIVO: Convertir consultas en leads calificados para visita técnica.
        
        PRECIOS REFERENCIALES (solo mencionar si preguntan):
        """
        
        # Agregar información específica del servicio si hay contexto
        if context:
            service_info = KNOWLEDGE_BASE["servicios"].get(context, {})
            if service_info:
                base_context += f"\n\nINFORMACIÓN ESPECÍFICA {context.upper()}:\n"
                base_context += json.dumps(service_info, indent=2, ensure_ascii=False)
        
        return base_context
    
    async def _openai_response(self, message: str, context: str, history: List[Dict]) -> Dict:
        """Respuesta usando OpenAI"""
        async with httpx.AsyncClient() as client:
            messages = [{"role": "system", "content": context}]
            
            # Agregar historial
            if history:
                messages.extend(history[-5:])  # Últimos 5 mensajes
            
            messages.append({"role": "user", "content": message})
            
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                json={
                    "model": "gpt-3.5-turbo",
                    "messages": messages,
                    "max_tokens": 500,
                    "temperature": 0.7
                }
            )
            
            data = response.json()
            return {
                "response": data["choices"][0]["message"]["content"],
                "source": "openai",
                "stage": "conversation"
            }
    
    async def _gemini_response(self, message: str, context: str, history: List[Dict]) -> Dict:
        """Respuesta usando Gemini"""
        async with httpx.AsyncClient() as client:
            prompt = f"{context}\n\nUsuario: {message}\nTeslaBot:"
            
            response = await client.post(
                f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={GEMINI_API_KEY}",
                json={
                    "contents": [{
                        "parts": [{"text": prompt}]
                    }],
                    "generationConfig": {
                        "maxOutputTokens": 500,
                        "temperature": 0.7
                    }
                }
            )
            
            data = response.json()
            return {
                "response": data["candidates"][0]["content"]["parts"][0]["text"],
                "source": "gemini", 
                "stage": "conversation"
            }
    
    def _local_response(self, message: str, context: str) -> Dict:
        """Respuesta local usando reglas"""
        msg = message.lower()
        
        # Detección de intenciones
        if any(word in msg for word in ['itse', 'certificado', 'inspección']):
            return self._itse_response(msg)
        elif any(word in msg for word in ['instalación', 'eléctrica', 'cableado']):
            return self._installation_response(msg)
        elif any(word in msg for word in ['automatización', 'domótica', 'smart']):
            return self._automation_response(msg)
        elif any(word in msg for word in ['mantenimiento', 'reparación']):
            return self._maintenance_response(msg)
        elif any(word in msg for word in ['precio', 'costo', 'cotización']):
            return self._price_response(msg)
        else:
            return {
                "response": "¡Hola! Soy TeslaBot de Tesla Electricidad. ¿En qué servicio puedo ayudarte?\n\n• ITSE (Certificados)\n• Instalaciones eléctricas\n• Automatización\n• Mantenimiento",
                "source": "local",
                "stage": "service_identification"
            }
    
    def _itse_response(self, message: str) -> Dict:
        sector = "comercio"  # default
        
        if "restaurante" in message: sector = "restaurante"
        elif "industria" in message: sector = "industria"
        elif "vivienda" in message or "casa" in message: sector = "vivienda"
        
        info = KNOWLEDGE_BASE["servicios"]["itse"]["sectores"][sector]
        
        response = f"""🔍 **ITSE para {sector.title()}**

💰 **Inversión:** S/{info['precio_min']} - S/{info['precio_max']}
⏱️ **Tiempo:** {info['tiempo']}
🎯 **Riesgo:** {info['riesgo']}

📋 **Incluye:**
• Planos arquitectónicos
• Memoria descriptiva eléctrica
• Certificado final ITSE

🔧 **¿Necesitas más información?**
Para cotización exacta necesito:
• Área del local (m²)
• Tipo específico de negocio
• Ubicación

¿Agendamos una visita técnica GRATUITA?"""

        return {
            "response": response,
            "source": "local",
            "stage": "specification_gathering",
            "context": "itse"
        }
    
    def _installation_response(self, message: str) -> Dict:
        tipo = "residencial" if "casa" in message or "vivienda" in message else "comercial"
        precio = KNOWLEDGE_BASE["servicios"]["instalaciones"]["precios"][f"punto_{tipo}"]
        
        response = f"""⚡ **Instalación Eléctrica {tipo.title()}**

💡 **Precio por punto:** S/{precio}

🔧 **Servicios incluidos:**
• Cableado completo
• Tableros eléctricos
• Tomacorrientes y switches
• Iluminación LED
• Puesta a tierra

📊 **Ejemplo cotización:**
• 10 puntos: S/{precio * 10:,}
• 20 puntos: S/{precio * 20:,}
• 30 puntos: S/{precio * 30:,}

🎯 **¿Cuántos puntos necesitas?**
Con esa info te doy cotización exacta.

¿Agendamos visita técnica sin costo?"""

        return {
            "response": response,
            "source": "local", 
            "stage": "specification_gathering",
            "context": "instalaciones"
        }
    
    def _automation_response(self, message: str) -> Dict:
        response = """🏠 **Automatización Tesla**

🎯 **Paquetes disponibles:**

**BÁSICO - S/2,500**
• Control luces inteligente
• Sensores de movimiento

**COMPLETO - S/4,500**
• Todo lo anterior +
• Cámaras IP seguridad
• App móvil control

**PREMIUM - S/7,500**
• Todo lo anterior +
• Alarma integrada
• Control climatización

📱 **Controla todo desde tu celular**

¿Qué paquete te interesa más?
¿Agendamos demostración en tu local?"""

        return {
            "response": response,
            "source": "local",
            "stage": "specification_gathering", 
            "context": "automatizacion"
        }
    
    def _maintenance_response(self, message: str) -> Dict:
        response = """🔧 **Mantenimiento Eléctrico Tesla**

📅 **Planes disponibles:**

**MENSUAL - S/300**
• 1 visita técnica
• Revisión tableros
• Medición voltajes

**TRIMESTRAL - S/800**
• 4 visitas año
• Limpieza contactos
• Reporte básico

**SEMESTRAL - S/1,400**
• 2 visitas año
• Reporte técnico completo
• Garantía 6 meses

⚡ **Previene el 90% de fallas eléctricas**

¿Qué plan se adapta mejor a tu negocio?"""

        return {
            "response": response,
            "source": "local",
            "stage": "specification_gathering",
            "context": "mantenimiento"
        }
    
    def _price_response(self, message: str) -> Dict:
        response = """💰 **Tarifas Tesla Electricidad 2024**

📊 **Precios referenciales:**
• ITSE: S/400 - S/3,000
• Instalaciones: S/85 - S/150 por punto
• Automatización: Desde S/2,500
• Mantenimiento: S/300/mes

🎯 **Para cotización EXACTA necesito:**
• Tipo servicio específico
• Metraje/cantidad puntos
• Ubicación del proyecto

📞 **CONSULTA TÉCNICA GRATUITA**

¿Cuál es tu nombre y WhatsApp?
Te contacto en 5 minutos con cotización personalizada."""

        return {
            "response": response,
            "source": "local",
            "stage": "data_collection"
        }

class WhatsAppService:
    def __init__(self):
        self.twilio_available = bool(TWILIO_SID and TWILIO_TOKEN)
    
    async def send_message(self, to: str, message: str) -> bool:
        """Enviar mensaje por WhatsApp"""
        if not self.twilio_available:
            logger.warning("WhatsApp no configurado, simulando envío")
            return True
        
        try:
            from twilio.rest import Client
            client = Client(TWILIO_SID, TWILIO_TOKEN)
            
            # Formatear número
            if not to.startswith('+'):
                to = f"+51{to}" if len(to) == 9 else f"+{to}"
            
            message = client.messages.create(
                body=message,
                from_=WHATSAPP_NUMBER,
                to=f"whatsapp:{to}"
            )
            
            return True
        except Exception as e:
            logger.error(f"Error enviando WhatsApp: {e}")
            return False
    
    def send_welcome_message(self, phone: str, nombre: str, servicio: str):
        """Enviar mensaje de bienvenida automático"""
        message = f"""¡Hola {nombre}! 👋

Gracias por contactar Tesla Electricidad desde nuestra web.

📋 **Servicio consultado:** {servicio}

🚀 **Próximos pasos:**
1. Revisaré tu consulta
2. Te enviaré cotización preliminar
3. Agendaremos visita técnica GRATUITA

⚡ Respondo en máximo 30 minutos.

*Tesla Electricidad - Energía Inteligente para Huancayo*"""
        
        return asyncio.create_task(self.send_message(phone, message))

# Inicializar servicios
db = DatabaseManager()
ai_service = AIService()
whatsapp_service = WhatsAppService()

# Crear aplicación FastAPI
app = FastAPI(
    title="Tesla Electricidad API",
    description="API Backend para Tesla Electricidad - Sistema Inteligente",
    version="2.0.0"
)

# Middleware CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Endpoints principales
@app.get("/")
async def root():
    return {"message": "Tesla Electricidad API v2.0", "status": "running"}

@app.post("/api/chat")
async def chat_endpoint(message: ChatMessage):
    """Endpoint principal del chatbot"""
    try:
        # Obtener respuesta de IA
        ai_response = await ai_service.get_ai_response(
            message.message, 
            message.context, 
            message.history
        )
        
        # Guardar conversación
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO conversations (user_id, message, response, stage, context) VALUES (?, ?, ?, ?, ?)",
            ("anonymous", message.message, ai_response["response"], ai_response.get("stage"), message.context)
        )
        conn.commit()
        conn.close()
        
        return ai_response
        
    except Exception as e:
        logger.error(f"Error en chat: {e}")
        raise HTTPException(status_code=500, detail="Error procesando mensaje")

@app.post("/api/contact")
async def contact_endpoint(contact: ContactForm, background_tasks: BackgroundTasks):
    """Endpoint para formulario de contacto"""
    try:
        # Guardar lead
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO leads (nombre, telefono, email, servicio, notas) VALUES (?, ?, ?, ?, ?)",
            (contact.nombre, contact.telefono, contact.email, contact.servicio, contact.mensaje)
        )
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        # Enviar WhatsApp en background
        background_tasks.add_task(
            whatsapp_service.send_welcome_message,
            contact.telefono,
            contact.nombre,
            contact.servicio
        )
        
        return {
            "success": True,
            "message": "Contacto recibido. Te escribiremos por WhatsApp en 5 minutos.",
            "lead_id": lead_id
        }
        
    except Exception as e:
        logger.error(f"Error guardando contacto: {e}")
        raise HTTPException(status_code=500, detail="Error procesando contacto")

@app.get("/api/dashboard/{mes}")
async def dashboard_stats(mes: int):
    """Endpoint para estadísticas del dashboard"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT itse, instalaciones, automatizacion, mantenimiento FROM servicios_stats WHERE mes = ?",
            (mes,)
        )
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                "mes": mes,
                "itse": result[0],
                "instalaciones": result[1],
                "automatizacion": result[2], 
                "mantenimiento": result[3]
            }
        else:
            return {"mes": mes, "itse": 0, "instalaciones": 0, "automatizacion": 0, "mantenimiento": 0}
            
    except Exception as e:
        logger.error(f"Error obteniendo estadísticas: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo datos")

@app.get("/api/services")
async def get_services():
    """Endpoint para obtener información de servicios"""
    return {
        "servicios": [
            {
                "id": "itse",
                "nombre": "Certificado ITSE",
                "descripcion": "Inspección Técnica de Seguridad en Edificaciones",
                "imagen": "https://images.unsplash.com/photo-1621905251918-48416bd8575a?w=400",
                "precio_desde": 400
            },
            {
                "id": "instalaciones", 
                "nombre": "Instalaciones Eléctricas",
                "descripcion": "Instalaciones completas residenciales y comerciales",
                "imagen": "https://images.unsplash.com/photo-1621905252507-b35492cc74b4?w=400",
                "precio_desde": 85
            },
            {
                "id": "automatizacion",
                "nombre": "Automatización",
                "descripcion": "Sistemas de domótica y control inteligente", 
                "imagen": "https://images.unsplash.com/photo-1518709268805-4e9042af2176?w=400",
                "precio_desde": 2500
            },
            {
                "id": "mantenimiento",
                "nombre": "Mantenimiento",
                "descripcion": "Mantenimiento preventivo y correctivo",
                "imagen": "https://images.unsplash.com/photo-1621905252472-e1024b75b8ae?w=400", 
                "precio_desde": 300
            }
        ]
    }

@app.get("/api/leads")
async def get_leads():
    """Endpoint para obtener leads (admin)"""
    try:
        conn = db.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, nombre, telefono, email, servicio, estado, created_at FROM leads ORDER BY created_at DESC LIMIT 50"
        )
        
        leads = []
        for row in cursor.fetchall():
            leads.append({
                "id": row[0],
                "nombre": row[1], 
                "telefono": row[2],
                "email": row[3],
                "servicio": row[4],
                "estado": row[5],
                "fecha": row[6]
            })
        
        conn.close()
        return {"leads": leads}
        
    except Exception as e:
        logger.error(f"Error obteniendo leads: {e}")
        raise HTTPException(status_code=500, detail="Error obteniendo leads")

@app.post("/api/whatsapp/send")
async def send_whatsapp(message: WhatsAppMessage):
    """Endpoint para enviar WhatsApp manual"""
    try:
        success = await whatsapp_service.send_message(message.to, message.message)
        return {"success": success}
    except Exception as e:
        logger.error(f"Error enviando WhatsApp: {e}")
        raise HTTPException(status_code=500, detail="Error enviando mensaje")

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)
