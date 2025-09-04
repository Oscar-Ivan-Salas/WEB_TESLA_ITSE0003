#!/usr/bin/env python3
"""
Tesla Electricidad - Generador Completo
Sintaxis corregida para VS Code
"""

import os
import subprocess
import sys

def create_tesla_project():
    """Crea el proyecto Tesla completo y funcional"""
    
    # Crear estructura
    os.makedirs("tesla_complete/frontend", exist_ok=True)
    os.makedirs("tesla_complete/backend", exist_ok=True)
    
    print("Creando proyecto Tesla Electricidad...")
    
    # FRONTEND COMPLETO - HTML
    html_content = '''<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tesla Electricidad - Energia Inteligente</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary: #1a1a2e;
            --secondary: #16213e;
            --accent: #0f3460;
            --highlight: #e94560;
            --text: #ffffff;
            --text-muted: #a0a0a0;
            --glass: rgba(255, 255, 255, 0.1);
            --glass-border: rgba(255, 255, 255, 0.2);
        }

        * { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, var(--primary), var(--secondary));
            color: var(--text);
            overflow-x: hidden;
        }

        .container { max-width: 1200px; margin: 0 auto; padding: 0 2rem; }

        /* Header */
        .header {
            position: fixed; top: 0; width: 100%;
            backdrop-filter: blur(20px); background: var(--glass);
            border-bottom: 1px solid var(--glass-border);
            z-index: 1000; padding: 1rem 0;
        }

        .header .container { display: flex; justify-content: space-between; align-items: center; }

        .logo {
            display: flex; align-items: center; gap: 0.5rem;
            font-size: 1.5rem; font-weight: 700; color: var(--highlight);
        }

        .nav { display: flex; gap: 2rem; }
        .nav a { color: var(--text); text-decoration: none; font-weight: 500; transition: color 0.3s ease; }
        .nav a:hover { color: var(--highlight); }

        /* Hero */
        .hero {
            min-height: 100vh; display: grid; grid-template-columns: 1fr 1fr;
            align-items: center; padding: 6rem 2rem 2rem; gap: 3rem;
        }

        .hero-content h1 {
            font-size: 3.5rem; font-weight: 700; margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--text), var(--highlight));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }

        .hero-content p {
            font-size: 1.2rem; color: var(--text-muted);
            margin-bottom: 2rem; line-height: 1.6;
        }

        .cta-btn {
            background: linear-gradient(135deg, var(--highlight), #ff6b6b);
            color: white; border: none; padding: 1rem 2rem; border-radius: 50px;
            font-size: 1.1rem; font-weight: 600; cursor: pointer;
            transition: all 0.3s ease; display: inline-flex;
            align-items: center; gap: 0.5rem;
        }

        .cta-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 10px 30px rgba(233, 69, 96, 0.3);
        }

        /* Dashboard */
        .dashboard-section { padding: 6rem 2rem; }
        .dashboard-section h2 { text-align: center; font-size: 2.5rem; margin-bottom: 3rem; }

        .month-selector {
            display: flex; justify-content: center; gap: 0.5rem;
            margin-bottom: 3rem; flex-wrap: wrap;
        }

        .month-btn {
            background: var(--glass); border: 1px solid var(--glass-border);
            color: var(--text); padding: 0.5rem 1rem; border-radius: 25px;
            cursor: pointer; transition: all 0.3s ease;
        }

        .month-btn.active { background: var(--highlight); border-color: var(--highlight); }

        .metrics-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 2rem;
        }

        .metric-card {
            background: var(--glass); backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border); border-radius: 20px;
            padding: 2rem; text-align: center; transition: transform 0.3s ease;
        }

        .metric-card:hover { transform: translateY(-5px); }
        .metric-card i { font-size: 3rem; color: var(--highlight); margin-bottom: 1rem; }
        .metric-card .value { font-size: 2.5rem; font-weight: 700; color: var(--text); margin-bottom: 0.5rem; }

        /* Services */
        .services-section { padding: 6rem 2rem; background: rgba(0, 0, 0, 0.2); }
        .services-section h2 { text-align: center; font-size: 2.5rem; margin-bottom: 3rem; }

        .services-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;
        }

        .service-card {
            background: var(--glass); backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border); border-radius: 20px;
            padding: 2rem; transition: all 0.3s ease;
        }

        .service-card:hover { transform: translateY(-10px); }

        .service-gallery {
            display: grid; grid-template-columns: repeat(2, 1fr);
            grid-template-rows: repeat(2, 1fr); gap: 8px;
            margin: 0 auto 25px; width: 240px; height: 200px;
        }

        .service-photo {
            border-radius: 10px; background: linear-gradient(135deg, var(--accent), var(--highlight));
            border: 2px solid var(--accent); transition: all 0.3s ease;
            display: flex; align-items: center; justify-content: center;
            font-size: 2rem; color: white;
        }

        .service-photo:hover { transform: scale(1.05); border-color: var(--highlight); }
        .service-photo:nth-child(1) { grid-column: 1 / 2; grid-row: 1 / 3; }
        .service-photo:nth-child(2) { grid-column: 2 / 3; grid-row: 1 / 2; }
        .service-photo:nth-child(3) { grid-column: 2 / 3; grid-row: 2 / 3; }

        .service-card h3 { color: var(--text); font-size: 1.3rem; margin-bottom: 15px; }
        .service-card p { color: var(--text-muted); line-height: 1.6; }

        /* Chatbot */
        .chatbot-container { position: fixed; bottom: 2rem; right: 2rem; z-index: 1000; }

        .chatbot-toggle {
            width: 60px; height: 60px; background: linear-gradient(135deg, var(--highlight), #ff6b6b);
            border: none; border-radius: 50%; color: white; font-size: 1.5rem;
            cursor: pointer; box-shadow: 0 5px 20px rgba(233, 69, 96, 0.3);
            transition: all 0.3s ease;
        }

        .chatbot-toggle:hover { transform: scale(1.1); }

        .chatbot-window {
            position: absolute; bottom: 80px; right: 0; width: 400px; height: 500px;
            background: var(--glass); backdrop-filter: blur(20px);
            border: 1px solid var(--glass-border); border-radius: 20px;
            display: none; flex-direction: column; overflow: hidden;
        }

        .chatbot-window.open { display: flex; }

        .chatbot-header {
            background: linear-gradient(135deg, var(--highlight), #ff6b6b);
            padding: 1rem; display: flex; align-items: center; gap: 1rem;
        }

        .chatbot-messages {
            flex: 1; padding: 1rem; overflow-y: auto;
            display: flex; flex-direction: column; gap: 1rem;
        }

        .message { display: flex; gap: 0.5rem; }
        .message.bot { justify-content: flex-start; }
        .message.user { justify-content: flex-end; }

        .message-bubble {
            max-width: 80%; padding: 0.75rem 1rem; border-radius: 15px;
            font-size: 0.9rem; line-height: 1.4;
        }

        .message.bot .message-bubble { background: rgba(255, 255, 255, 0.1); }
        .message.user .message-bubble { background: var(--highlight); color: white; }

        .quick-actions { display: flex; flex-wrap: wrap; gap: 0.5rem; margin-top: 0.5rem; }

        .quick-btn {
            background: rgba(233, 69, 96, 0.2); border: 1px solid var(--highlight);
            color: var(--highlight); padding: 0.5rem 0.75rem; border-radius: 15px;
            font-size: 0.8rem; cursor: pointer; transition: all 0.3s ease;
        }

        .quick-btn:hover { background: var(--highlight); color: white; }

        .chatbot-input {
            padding: 1rem; display: flex; gap: 0.5rem;
            border-top: 1px solid var(--glass-border);
        }

        .chatbot-input input {
            flex: 1; background: rgba(255, 255, 255, 0.1);
            border: 1px solid var(--glass-border); border-radius: 25px;
            padding: 0.75rem 1rem; color: var(--text); outline: none;
        }

        .chatbot-input button {
            background: var(--highlight); border: none; border-radius: 50%;
            width: 45px; height: 45px; color: white; cursor: pointer;
        }

        /* WhatsApp */
        .whatsapp-float {
            position: fixed; bottom: 2rem; left: 2rem; width: 60px; height: 60px;
            background: #25d366; border-radius: 50%; display: flex;
            align-items: center; justify-content: center; color: white;
            font-size: 1.5rem; text-decoration: none; z-index: 999;
        }

        /* Responsive */
        @media (max-width: 768px) {
            .hero { grid-template-columns: 1fr; text-align: center; }
            .hero-content h1 { font-size: 2.5rem; }
            .nav { display: none; }
        }
    </style>
</head>
<body>
    <header class="header">
        <div class="container">
            <div class="logo">
                <i class="fas fa-bolt"></i>
                Tesla Electricidad
            </div>
            <nav class="nav">
                <a href="#inicio">Inicio</a>
                <a href="#servicios">Servicios</a>
                <a href="#dashboard">Dashboard</a>
            </nav>
        </div>
    </header>

    <section id="inicio" class="hero">
        <div class="hero-content">
            <h1>Energia Inteligente para Huancayo</h1>
            <p>Especialistas en instalaciones electricas, automatizacion y certificaciones ITSE</p>
            <button class="cta-btn" onclick="openChat()">
                <i class="fas fa-robot"></i>
                Cotizar con IA
            </button>
        </div>
    </section>

    <section id="dashboard" class="dashboard-section">
        <div class="container">
            <h2>Nuestro Rendimiento 2024</h2>
            <div class="month-selector">
                <button class="month-btn" data-month="1">Ene</button>
                <button class="month-btn" data-month="2">Feb</button>
                <button class="month-btn" data-month="3">Mar</button>
                <button class="month-btn" data-month="4">Abr</button>
                <button class="month-btn" data-month="5">May</button>
                <button class="month-btn" data-month="6">Jun</button>
                <button class="month-btn" data-month="7">Jul</button>
                <button class="month-btn active" data-month="8">Ago</button>
            </div>
            <div class="metrics-grid" id="metricsGrid"></div>
        </div>
    </section>

    <section id="servicios" class="services-section">
        <div class="container">
            <h2>Servicios Especializados</h2>
            <div class="services-grid">
                <div class="service-card">
                    <div class="service-gallery">
                        <div class="service-photo"><i class="fas fa-certificate"></i></div>
                        <div class="service-photo"><i class="fas fa-file-alt"></i></div>
                        <div class="service-photo"><i class="fas fa-check-circle"></i></div>
                    </div>
                    <h3>Certificado ITSE</h3>
                    <p>Gestion completa para la Inspeccion Tecnica de Seguridad en Edificaciones</p>
                </div>
                
                <div class="service-card">
                    <div class="service-gallery">
                        <div class="service-photo"><i class="fas fa-plug"></i></div>
                        <div class="service-photo"><i class="fas fa-tools"></i></div>
                        <div class="service-photo"><i class="fas fa-shield-alt"></i></div>
                    </div>
                    <h3>Pozo de Tierra</h3>
                    <p>Instalacion y mantenimiento de sistemas de puesta a tierra</p>
                </div>
                
                <div class="service-card">
                    <div class="service-gallery">
                        <div class="service-photo"><i class="fas fa-wrench"></i></div>
                        <div class="service-photo"><i class="fas fa-cogs"></i></div>
                        <div class="service-photo"><i class="fas fa-battery-full"></i></div>
                    </div>
                    <h3>Mantenimiento Electrico</h3>
                    <p>Mantenimiento preventivo y correctivo para instalaciones</p>
                </div>
                
                <div class="service-card">
                    <div class="service-gallery">
                        <div class="service-photo"><i class="fas fa-fire-extinguisher"></i></div>
                        <div class="service-photo"><i class="fas fa-exclamation-triangle"></i></div>
                        <div class="service-photo"><i class="fas fa-bell"></i></div>
                    </div>
                    <h3>Sistema Contra Incendios</h3>
                    <p>Diseno e instalacion de sistemas de deteccion</p>
                </div>
            </div>
        </div>
    </section>

    <div class="chatbot-container">
        <button class="chatbot-toggle" onclick="toggleChat()">
            <i class="fas fa-robot"></i>
        </button>
        <div class="chatbot-window" id="chatbotWindow">
            <div class="chatbot-header">
                <h4>Tesla IA</h4>
                <button onclick="closeChat()" style="background: none; border: none; color: white;">×</button>
            </div>
            <div class="chatbot-messages" id="chatMessages">
                <div class="message bot">
                    <div class="message-bubble">
                        Hola! Soy Tesla IA. En que puedo ayudarte?
                        <div class="quick-actions">
                            <button class="quick-btn" onclick="sendQuickMessage('ITSE')">ITSE</button>
                            <button class="quick-btn" onclick="sendQuickMessage('Pozo')">Pozo</button>
                            <button class="quick-btn" onclick="sendQuickMessage('Precios')">Precios</button>
                        </div>
                    </div>
                </div>
            </div>
            <div class="chatbot-input">
                <input type="text" id="messageInput" placeholder="Escribe tu mensaje...">
                <button onclick="sendMessage()"><i class="fas fa-paper-plane"></i></button>
            </div>
        </div>
    </div>

    <a href="https://wa.me/51906315961" class="whatsapp-float" target="_blank">
        <i class="fab fa-whatsapp"></i>
    </a>

    <script>
        const API_URL = 'http://localhost:8000';
        let apiOnline = false;

        const dashboardData = {
            1: {itse: 15, pozo_tierra: 8, mantenimiento: 12, incendios: 5, clientes: 25, satisfaccion: 95},
            2: {itse: 18, pozo_tierra: 10, mantenimiento: 15, incendios: 7, clientes: 28, satisfaccion: 96},
            3: {itse: 22, pozo_tierra: 12, mantenimiento: 18, incendios: 8, clientes: 32, satisfaccion: 97},
            4: {itse: 25, pozo_tierra: 14, mantenimiento: 20, incendios: 10, clientes: 35, satisfaccion: 96},
            5: {itse: 28, pozo_tierra: 16, mantenimiento: 22, incendios: 12, clientes: 38, satisfaccion: 98},
            6: {itse: 32, pozo_tierra: 18, mantenimiento: 25, incendios: 14, clientes: 42, satisfaccion: 97},
            7: {itse: 35, pozo_tierra: 20, mantenimiento: 28, incendios: 16, clientes: 45, satisfaccion: 98},
            8: {itse: 38, pozo_tierra: 22, mantenimiento: 30, incendios: 18, clientes: 48, satisfaccion: 99}
        };

        document.addEventListener('DOMContentLoaded', function() {
            initDashboard();
        });

        function initDashboard() {
            createMetricsGrid();
            loadDashboardData(8);
            
            document.querySelectorAll('.month-btn').forEach(btn => {
                btn.addEventListener('click', (e) => {
                    const month = parseInt(e.target.dataset.month);
                    selectMonth(month);
                });
            });
        }

        function createMetricsGrid() {
            const grid = document.getElementById('metricsGrid');
            if (!grid) return;
            
            const metrics = [
                {id: 'itse', icon: 'fas fa-certificate', label: 'Certificados ITSE'},
                {id: 'pozo_tierra', icon: 'fas fa-plug', label: 'Pozos de Tierra'},
                {id: 'mantenimiento', icon: 'fas fa-tools', label: 'Mantenimientos'},
                {id: 'incendios', icon: 'fas fa-fire-extinguisher', label: 'Sistemas C.I.'},
                {id: 'clientes', icon: 'fas fa-users', label: 'Clientes Nuevos'},
                {id: 'satisfaccion', icon: 'fas fa-star', label: 'Satisfaccion'}
            ];
            
            grid.innerHTML = metrics.map(metric => 
                '<div class="metric-card">' +
                '<i class="' + metric.icon + '"></i>' +
                '<div class="value" id="metric-' + metric.id + '">0</div>' +
                '<div class="label">' + metric.label + '</div>' +
                '</div>'
            ).join('');
        }

        function selectMonth(month) {
            document.querySelectorAll('.month-btn').forEach(btn => btn.classList.remove('active'));
            document.querySelector('[data-month="' + month + '"]').classList.add('active');
            loadDashboardData(month);
        }

        function loadDashboardData(month) {
            const data = dashboardData[month];
            Object.keys(data).forEach(key => {
                const element = document.getElementById('metric-' + key);
                if (element) {
                    const suffix = key === 'satisfaccion' ? '%' : '';
                    animateValue(element, 0, data[key], suffix);
                }
            });
        }

        function animateValue(element, start, end, suffix) {
            const duration = 1000;
            const startTime = performance.now();
            
            function animate(currentTime) {
                const elapsed = currentTime - startTime;
                const progress = Math.min(elapsed / duration, 1);
                const current = Math.floor(start + (end - start) * progress);
                element.textContent = current + (suffix || '');
                
                if (progress < 1) {
                    requestAnimationFrame(animate);
                }
            }
            
            requestAnimationFrame(animate);
        }

        function toggleChat() {
            document.getElementById('chatbotWindow').classList.toggle('open');
        }

        function openChat() {
            document.getElementById('chatbotWindow').classList.add('open');
        }

        function closeChat() {
            document.getElementById('chatbotWindow').classList.remove('open');
        }

        function sendMessage() {
            const input = document.getElementById('messageInput');
            const message = input.value.trim();
            if (!message) return;
            
            addMessage('user', message);
            input.value = '';
            processMessage(message);
        }

        function sendQuickMessage(message) {
            addMessage('user', message);
            processMessage(message);
        }

        function processMessage(message) {
            setTimeout(() => addMessage('bot', getLocalResponse(message)), 1000);
        }

        function getLocalResponse(message) {
            const lower = message.toLowerCase();
            
            if (lower.includes('itse') || lower.includes('certificado')) {
                return 'CERTIFICADO ITSE<br><br>' +
                       'Costos:<br>' +
                       '• Municipalidad: S/ 218<br>' +
                       '• Nuestro servicio: S/ 300-500<br>' +
                       '• Total: S/ 518-718<br><br>' +
                       'Tiempo: 5-10 dias<br>' +
                       'WhatsApp: +51 906 315 961';
            }
            
            if (lower.includes('pozo') || lower.includes('tierra')) {
                return 'POZO DE TIERRA<br><br>' +
                       'Precio: S/ 1,500 - 2,500<br><br>' +
                       'Varia segun tipo de terreno<br>' +
                       'Visita tecnica gratuita<br>' +
                       'WhatsApp: +51 906 315 961';
            }
            
            if (lower.includes('precio')) {
                return 'PRECIOS REFERENCIALES 2024<br><br>' +
                       'ITSE: S/ 518 - 1,218<br>' +
                       'Pozo Tierra: S/ 1,500 - 2,500<br>' +
                       'Mantenimiento: S/ 200 - 1,200<br>' +
                       'Contra Incendios: Desde S/ 1,500<br><br>' +
                       'WhatsApp: +51 906 315 961';
            }
            
            return 'Soy Tesla IA, especialista en servicios electricos.<br><br>' +
                   'Sobre que necesitas informacion?<br>' +
                   '• Certificado ITSE<br>' +
                   '• Pozo de Tierra<br>' +
                   '• Mantenimiento<br>' +
                   '• Sistema Contra Incendios<br><br>' +
                   'WhatsApp: +51 906 315 961';
        }

        function addMessage(sender, content) {
            const messages = document.getElementById('chatMessages');
            const div = document.createElement('div');
            div.className = 'message ' + sender;
            const bubble = document.createElement('div');
            bubble.className = 'message-bubble';
            bubble.innerHTML = content;
            div.appendChild(bubble);
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>'''
    
    with open("tesla_complete/frontend/index.html", "w", encoding="utf-8") as f:
        f.write(html_content)

    # BACKEND PYTHON COMPLETO
    backend_content = '''from fastapi import FastAPI, HTTPException
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
'''

    with open("tesla_complete/backend/main.py", "w", encoding="utf-8") as f:
        f.write(backend_content)

    # REQUIREMENTS.TXT
    requirements_content = '''fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
'''

    with open("tesla_complete/backend/requirements.txt", "w", encoding="utf-8") as f:
        f.write(requirements_content)

    # SCRIPT DE INICIO
    start_script = '''#!/usr/bin/env python3
import subprocess
import sys
import os
import webbrowser
import time

def main():
    print("Tesla Electricidad - Iniciando proyecto completo...")
    
    try:
        os.chdir("tesla_complete")
        
        print("Instalando dependencias...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"])
        
        print("Iniciando backend...")
        os.chdir("backend")
        backend_process = subprocess.Popen([sys.executable, "main.py"])
        os.chdir("..")
        
        print("Esperando 3 segundos...")
        time.sleep(3)
        
        print("Abriendo frontend...")
        frontend_path = os.path.abspath("frontend/index.html")
        webbrowser.open(f"file://{frontend_path}")
        
        print("\\nProyecto iniciado:")
        print("- Backend: http://localhost:8000")
        print("- Frontend: Abierto en navegador")
        print("- API Docs: http://localhost:8000/docs")
        print("\\nTu chatbot Tesla esta listo!")
        print("\\nPresiona Ctrl+C para detener")
        
        try:
            backend_process.wait()
        except KeyboardInterrupt:
            print("\\nProyecto detenido")
            backend_process.terminate()
            
    except Exception as e:
        print(f"Error: {e}")
        print("Asegurate de estar en el directorio correcto")

if __name__ == "__main__":
    main()
'''

    with open("tesla_complete/start.py", "w", encoding="utf-8") as f:
        f.write(start_script)

    # README
    readme_content = '''# Tesla Electricidad - Chatbot IA Completo

## Inicio Rapido

```bash
python start.py
```

## Estructura
```
tesla_complete/
├── frontend/
│   └── index.html      # Web completa con chatbot
├── backend/
│   ├── main.py         # API FastAPI
│   └── requirements.txt
└── start.py           # Script de inicio
```

## Funcionalidades

### Frontend
- Dashboard interactivo con metricas
- Chatbot Tesla IA completamente funcional
- Respuestas especializadas en servicios electricos
- Integracion WhatsApp
- Diseno responsivo moderno

### Backend  
- API FastAPI con SQLite
- Procesador de chat inteligente
- Base de conocimiento especializada
- Almacenamiento de conversaciones

### Servicios Incluidos
- Certificado ITSE (S/ 518-718)
- Pozo de Tierra (S/ 1,500-2,500)  
- Mantenimiento (S/ 200-1,200)
- Sistema Contra Incendios (Desde S/ 1,500)

## URLs
- Frontend: Abre automaticamente en navegador
- Backend API: http://localhost:8000  
- Docs: http://localhost:8000/docs

Tu chatbot Tesla esta listo para convertir visitantes en clientes!
'''

    with open("tesla_complete/README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

    print("✅ PROYECTO TESLA COMPLETO GENERADO - SINTAXIS CORREGIDA")
    print("\n🚀 Para ejecutar:")
    print("   cd tesla_complete")
    print("   python start.py")
    print("\n📁 Archivos creados:")
    print("   - Frontend completo con chatbot IA")  
    print("   - Backend FastAPI con SQLite")
    print("   - Script de inicio automatico")
    print("\n🎯 Resultado: Web funcional + Chatbot especializado + API")

if __name__ == "__main__":
    create_tesla_project()