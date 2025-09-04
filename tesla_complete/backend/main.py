from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, validator, EmailStr
from typing import List, Optional, Dict, Any
from datetime import datetime, time
import sqlite3
import os
import re
import uvicorn
from enum import Enum

app = FastAPI(title="Tesla Electricidad API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class ServicioEnum(str, Enum):
    ITSE = "itse"
    POZO_TIERRA = "pozo_tierra"
    MANTENIMIENTO = "mantenimiento"
    INCENDIOS = "incendios"
    TABLEROS = "tableros"
    SUMINISTROS = "suministros"

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None
    servicio_interes: Optional[ServicioEnum] = None

class Lead(BaseModel):
    nombre: str = Field(..., min_length=3, max_length=100)
    ruc: str = Field(..., min_length=11, max_length=11)
    telefono: str = Field(..., min_length=9, max_length=15)
    email: EmailStr
    tipo_negocio: str
    direccion: str
    metraje: float
    licencia_funcionamiento: bool
    servicio_interes: ServicioEnum

    @validator('ruc')
    def validate_ruc(cls, v):
        if not v.isdigit() or len(v) != 11:
            raise ValueError('El RUC debe tener exactamente 11 dígitos')
        return v

class Cita(BaseModel):
    lead_id: int
    fecha_preferida: str  # Formato: YYYY-MM-DD
    hora_preferida: str   # Formato: HH:MM
    tipo_visita: str
    urgencia: str = Field(..., regex='^(baja|media|alta)$')
    notas: Optional[str] = None

class CotizacionRequest(BaseModel):
    lead_id: int
    servicio: ServicioEnum
    metraje: float
    detalles_adicionales: Optional[Dict[str, Any]] = None

def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect("data/tesla.db")
    cursor = conn.cursor()
    
    # Tabla de conversaciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_message TEXT,
            bot_response TEXT,
            servicio_interes TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de leads (clientes potenciales)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            ruc TEXT UNIQUE NOT NULL,
            telefono TEXT NOT NULL,
            email TEXT NOT NULL,
            tipo_negocio TEXT NOT NULL,
            direccion TEXT NOT NULL,
            metraje REAL NOT NULL,
            licencia_funcionamiento BOOLEAN NOT NULL,
            servicio_interes TEXT NOT NULL,
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Tabla de citas
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS citas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            fecha DATE NOT NULL,
            hora TIME NOT NULL,
            tipo_visita TEXT NOT NULL,
            urgencia TEXT NOT NULL,
            notas TEXT,
            estado TEXT DEFAULT 'pendiente',
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
    """)
    
    # Tabla de cotizaciones
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            lead_id INTEGER NOT NULL,
            servicio TEXT NOT NULL,
            metraje REAL NOT NULL,
            monto_total REAL NOT NULL,
            detalles TEXT,
            fecha_creacion DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
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

@app.post("/api/chat")
async def chat(message_data: ChatMessage):
    try:
        # Procesar el mensaje con lógica de chatbot mejorada
        response, servicio_interes = process_chat_avanzado(message_data.message, message_data.servicio_interes)
        
        # Generar un ID de sesión si no existe
        session_id = message_data.session_id or f"sess_{os.urandom(8).hex()}"
        
        # Guardar en la base de datos
        conn = sqlite3.connect("data/tesla.db")
        cursor = conn.cursor()
        cursor.execute(
            """INSERT INTO conversations 
               (session_id, user_message, bot_response, servicio_interes) 
               VALUES (?, ?, ?, ?)""",
            (session_id, message_data.message, response, 
             servicio_interes.value if servicio_interes else None)
        )
        conn.commit()
        conn.close()
        
        return {
            "success": True, 
            "response": response,
            "session_id": session_id,
            "servicio_interes": servicio_interes
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/lead")
async def crear_lead(lead: Lead):
    try:
        conn = sqlite3.connect("data/tesla.db")
        cursor = conn.cursor()
        
        # Verificar si el RUC ya existe
        cursor.execute("SELECT id FROM leads WHERE ruc = ?", (lead.ruc,))
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El RUC ya está registrado"
            )
        
        # Insertar nuevo lead
        cursor.execute(
            """INSERT INTO leads 
               (nombre, ruc, telefono, email, tipo_negocio, direccion, metraje, licencia_funcionamiento, servicio_interes)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (lead.nombre, lead.ruc, lead.telefono, lead.email, lead.tipo_negocio, 
             lead.direccion, lead.metraje, lead.licencia_funcionamiento, lead.servicio_interes.value)
        )
        
        lead_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True, 
            "message": "Lead registrado exitosamente",
            "lead_id": lead_id
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cita")
async def agendar_cita(cita: Cita):
    try:
        # Validar formato de fecha y hora
        try:
            fecha = datetime.strptime(cita.fecha_preferida, "%Y-%m-%d").date()
            hora = datetime.strptime(cita.hora_preferida, "%H:%M").time()
            
            # Validar que sea una hora laboral (8am - 6pm)
            if hora < time(8, 0) or hora > time(18, 0):
                raise ValueError("Las citas son de lunes a viernes de 8:00 AM a 6:00 PM")
                
            # Validar que no sea fin de semana
            if fecha.weekday() >= 5:  # 5 = sábado, 6 = domingo
                raise ValueError("No se pueden agendar citas los fines de semana")
                
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
        
        # Verificar disponibilidad
        conn = sqlite3.connect("data/tesla.db")
        cursor = conn.cursor()
        
        # Verificar si hay citas en la misma hora (margen de 1 hora)
        cursor.execute(
            """SELECT id FROM citas 
               WHERE fecha = ? AND 
               (time(hora) BETWEEN time(?, '-30 minutes') AND time(?, '+30 minutes'))
               AND estado = 'pendiente'""",
            (cita.fecha_preferida, cita.hora_preferida, cita.hora_preferida)
        )
        
        if cursor.fetchone():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe una cita programada en ese horario. Por favor, seleccione otro horario."
            )
        
        # Insertar la cita
        cursor.execute(
            """INSERT INTO citas 
               (lead_id, fecha, hora, tipo_visita, urgencia, notas)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (cita.lead_id, cita.fecha_preferida, cita.hora_preferida, 
             cita.tipo_visita, cita.urgencia, cita.notas)
        )
        
        cita_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True, 
            "message": "Cita agendada exitosamente",
            "cita_id": cita_id,
            "fecha": cita.fecha_preferida,
            "hora": cita.hora_preferida
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/servicios")
async def listar_servicios():
    try:
        # Obtener la ruta base para las imágenes
        base_url = "/static/assets/servicios/"
        
        servicios = [
            {
                "id": "itse",
                "nombre": "Certificado ITSE",
                "descripcion": "Gestión completa para la Inspección Técnica de Seguridad en Edificaciones.",
                "precio_referencial": "S/ 518 - S/ 2,218",
                "tiempo_estimado": "5-10 días hábiles",
                "imagenes": [f"{base_url}itse/foto1.jpg", f"{base_url}itse/foto2.jpg"],
                "detalles": [
                    "Evaluación técnica completa",
                    "Elaboración de planos (si es necesario)",
                    "Gestión del trámite municipal"
                ]
            },
            {
                "id": "pozo_tierra",
                "nombre": "Pozo de Tierra",
                "descripcion": "Sistema de puesta a tierra para protección de equipos y personas.",
                "precio_referencial": "S/ 1,200 - S/ 4,500",
                "tiempo_estimado": "1-2 días",
                "imagenes": [f"{base_url}pozo_tierra/foto1.jpg", f"{base_url}pozo_tierra/foto2.jpg"],
                "detalles": [
                    "Medición de resistividad del terreno",
                    "Diseño según normativa",
                    "Instalación y certificación"
                ]
            },
            {
                "id": "mantenimiento",
                "nombre": "Mantenimiento Eléctrico",
                "descripcion": "Servicios de mantenimiento preventivo y correctivo.",
                "precio_referencial": "S/ 200 - S/ 1,200",
                "tiempo_estimado": "2-4 horas (depende del servicio)",
                "imagenes": [f"{base_url}mantenimiento/foto1.jpg", f"{base_url}mantenimiento/foto2.jpg"],
                "detalles": [
                    "Inspección de tableros eléctricos",
                    "Pruebas de continuidad y aislamiento",
                    "Limpieza y ajuste de conexiones"
                ]
            },
            {
                "id": "incendios",
                "nombre": "Sistema Contra Incendios",
                "descripcion": "Diseño e instalación de sistemas de protección contra incendios.",
                "precio_referencial": "A consultar",
                "tiempo_estimado": "Variable según proyecto",
                "imagenes": [f"{base_url}incendios/foto1.jpg", f"{base_url}incendios/foto2.jpg"],
                "detalles": [
                    "Diseño personalizado",
                    "Instalación de equipos",
                    "Capacitación y certificación"
                ]
            },
            {
                "id": "tableros",
                "nombre": "Diseño de Tableros",
                "descripcion": "Fabricación e instalación de tableros eléctricos.",
                "precio_referencial": "A consultar",
                "tiempo_estimado": "Variable según complejidad",
                "imagenes": [f"{base_url}tableros/foto1.jpg", f"{base_url}tableros/foto2.jpg"],
                "detalles": [
                    "Diseño según necesidades",
                    "Fabricación con materiales de calidad",
                    "Pruebas y certificación"
                ]
            },
            {
                "id": "suministros",
                "nombre": "Suministros Eléctricos",
                "descripcion": "Venta de materiales y equipos eléctricos.",
                "precio_referencial": "Variable",
                "tiempo_estimado": "Inmediato (en stock)",
                "imagenes": [f"{base_url}suministros/foto1.jpg", f"{base_url}suministros/foto2.jpg"],
                "detalles": [
                    "Amplio catálogo de productos",
                    "Marcas de calidad",
                    "Asesoría técnica especializada"
                ]
            }
        ]
        
        return {"success": True, "servicios": servicios}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/cotizacion")
async def generar_cotizacion(cotizacion: CotizacionRequest):
    try:
        conn = sqlite3.connect("data/tesla.db")
        cursor = conn.cursor()
        
        # Obtener información del lead
        cursor.execute("SELECT * FROM leads WHERE id = ?", (cotizacion.lead_id,))
        lead = cursor.fetchone()
        
        if not lead:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Lead no encontrado"
            )
        
        # Calcular cotización según el servicio y metraje
        cotizacion_info = calcular_cotizacion(
            cotizacion.servicio, 
            cotizacion.metraje, 
            lead[5]  # tipo_negocio
        )
        
        # Guardar la cotización en la base de datos
        cursor.execute(
            """INSERT INTO cotizaciones 
               (lead_id, servicio, metraje, monto_total, detalles)
               VALUES (?, ?, ?, ?, ?)""",
            (
                cotizacion.lead_id,
                cotizacion.servicio.value,
                cotizacion.metraje,
                cotizacion_info["monto_total"],
                str(cotizacion.detalles_adicionales) if cotizacion.detalles_adicionales else None
            )
        )
        
        cotizacion_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "cotizacion_id": cotizacion_id,
            **cotizacion_info
        }
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def calcular_cotizacion(servicio: ServicioEnum, metraje: float, tipo_negocio: str) -> dict:
    """Calcula el monto de la cotización según el servicio y metraje"""
    # Factores de ajuste según tipo de negocio
    factores = {
        'residencial': 1.0,
        'comercial': 1.2,
        'industrial': 1.5,
        'oficina': 1.1
    }
    
    factor = factores.get(tipo_negocio.lower(), 1.0)
    
    # Lógica de precios por servicio
    if servicio == ServicioEnum.ITSE:
        base = 500.0
        monto = base * factor
        descripcion = "CERTIFICADO ITSE - Incluye inspección, documentación y trámite municipal."
    
    elif servicio == ServicioEnum.POZO_TIERRA:
        base = 1500.0 + (metraje * 5)
        monto = base * factor
        descripcion = "POZO DE TIERRA - Incluye materiales, instalación y certificación."
    
    elif servicio == ServicioEnum.MANTENIMIENTO:
        base = 300.0 + (metraje * 2)
        monto = base * factor
        descripcion = "MANTENIMIENTO ELÉCTRICO - Incluye inspección y ajustes."
    
    elif servicio == ServicioEnum.INCENDIOS:
        base = 2000.0 + (metraje * 10)
        monto = base * factor
        descripcion = "SISTEMA CONTRA INCENDIOS - Incluye diseño e instalación."
    
    elif servicio == ServicioEnum.TABLEROS:
        base = 1000.0 + (metraje * 8)
        monto = base * factor
        descripcion = "DISEÑO DE TABLEROS - Incluye materiales y mano de obra."
    
    elif servicio == ServicioEnum.SUMINISTROS:
        base = metraje * 15  # Precio por m2
        monto = base * factor
        descripcion = "SUMINISTROS ELÉCTRICOS - Materiales de calidad garantizada."
    
    return {
        "servicio": servicio.value,
        "metraje": metraje,
        "tipo_negocio": tipo_negocio,
        "monto_base": base,
        "factor_ajuste": factor,
        "monto_total": round(monto, 2),
        "descripcion": descripcion,
        "validez": 30,  # días
        "condiciones": "Precio sujeto a verificación técnica in situ"
    }

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

def process_chat_avanzado(message: str, servicio_interes: Optional[ServicioEnum] = None) -> tuple[str, Optional[ServicioEnum]]:
    """
    Procesa el mensaje del usuario y devuelve una respuesta del chatbot.
    Retorna una tupla con (respuesta, servicio_interes)
    """
    lower = message.lower()
    
    # Detectar servicio de interés si no está definido
    if not servicio_interes:
        if any(word in lower for word in ['itse', 'certificado', 'licencia']):
            servicio_interes = ServicioEnum.ITSE
        elif any(word in lower for word in ['pozo', 'tierra', 'aterramiento']):
            servicio_interes = ServicioEnum.POZO_TIERRA
        elif any(word in lower for word in ['mantenimiento', 'reparacion', 'reparación']):
            servicio_interes = ServicioEnum.MANTENIMIENTO
        elif any(word in lower for word in ['incendio', 'extintor', 'sprinkler']):
            servicio_interes = ServicioEnum.INCENDIOS
        elif any(word in lower for word in ['tablero', 'tableros', 'cuadro electrico']):
            servicio_interes = ServicioEnum.TABLEROS
        elif any(word in lower for word in ['suministro', 'materiales', 'cables', 'cableado']):
            servicio_interes = ServicioEnum.SUMINISTROS
    
    # Generar respuesta basada en el servicio de interés
    if servicio_interes == ServicioEnum.ITSE:
        response = """📋 CERTIFICADO ITSE - Información Completa

Para brindarte una cotización exacta, necesito algunos datos adicionales:

1. ¿Qué tipo de local tienes? (Restaurante, tienda, oficina, etc.)
2. ¿Cuál es el área total del local en m²?
3. ¿Ya cuentas con plano arquitectónico?

Costos referenciales:
• Pago municipal: S/ 218.00
• Nuestro servicio: S/ 300.00 - S/ 500.00
• Total aproximado: S/ 518.00 - S/ 718.00

Tiempo estimado: 5-10 días hábiles

¿Te gustaría que te ayude con el proceso?"""

    elif servicio_interes == ServicioEnum.POZO_TIERRA:
        response = """⚡ POZO DE TIERRA - Sistema de Seguridad

Para calcular el precio exacto, necesito saber:

1. ¿Qué tipo de terreno tienes? (arcilloso, arenoso, rocoso)
2. ¿Cuál es el área aproximada del terreno?
3. ¿Es para uso residencial, comercial o industrial?

Precio referencial: S/ 1,500 - S/ 2,500

El costo varía según:
• Tipo de terreno
• Resistividad del suelo
• Profundidad requerida
• Materiales necesarios

¿Te gustaría agendar una visita técnica sin costo?"""

    elif servicio_interes == ServicioEnum.MANTENIMIENTO:
        response = """🔧 MANTENIMIENTO ELÉCTRICO - Preventivo y Correctivo

Para ofrecerte el mejor servicio, necesito que me indiques:

1. ¿Qué tipo de mantenimiento necesitas? (preventivo, correctivo, emergencia)
2. ¿Cuál es el área aproximada de las instalaciones?
3. ¿Qué tipo de instalación es? (casa, oficina, industria, etc.)

Nuestros servicios incluyen:
• Revisión de tableros eléctricos
• Medición de parámetros eléctricos
• Identificación de riesgos
• Reporte detallado

¿Te gustaría que te envíe un técnico?"""

    elif servicio_interes in [ServicioEnum.INCENDIOS, ServicioEnum.TABLEROS, ServicioEnum.SUMINISTROS]:
        servicios = {
            ServicioEnum.INCENDIOS: "SISTEMA CONTRA INCENDIOS",
            ServicioEnum.TABLEROS: "DISEÑO DE TABLEROS",
            ServicioEnum.SUMINISTROS: "SUMINISTROS ELÉCTRICOS"
        }
        servicio_nombre = servicios[servicio_interes]
        
        response = f"""🏢 {servicio_nombre}

Para brindarte información más precisa, necesito que me indiques:

1. ¿Qué tipo de proyecto es? (residencial, comercial, industrial)
2. ¿Cuál es el área aproximada del lugar?
3. ¿Tienes algún requerimiento específico?

Nuestro equipo se pondrá en contacto contigo para ofrecerte una cotización personalizada.

¿Podrías proporcionarme estos datos?"""

    elif any(word in lower for word in ['precio', 'costo', 'cuanto cuesta', 'tarifa']):
        response = """💰 LISTA DE PRECIOS REFERENCIALES 2024

CERTIFICADO ITSE:
• Comercio básico: S/ 518 - 718
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
• Detección básica: S/ 1,500+
• Sistema completo: Cotización personalizada

Precios incluyen materiales básicos. ¿Te interesa algún servicio en particular?"""

    else:
        response = """👋 ¡Hola! Soy Tesla IA, tu asistente especializado en servicios eléctricos.

¿En qué puedo ayudarte hoy? Puedo asistirte con:

• 📋 Certificado ITSE - Gestión completa
• ⚡ Pozo de Tierra - Seguridad eléctrica  
• 🔧 Mantenimiento - Preventivo y correctivo
• 🚒 Sistema Contra Incendios - Protección total
• 💡 Consultar precios - Rangos referenciales

Solo dime qué necesitas y con gusto te ayudaré."""
    
    return response, servicio_interes

# Función de compatibilidad hacia atrás
def process_chat(message: str) -> str:
    response, _ = process_chat_avanzado(message)
    return response
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
