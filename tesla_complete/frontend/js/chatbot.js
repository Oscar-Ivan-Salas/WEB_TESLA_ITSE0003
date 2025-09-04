// Tesla Electricidad Chatbot - Sistema de atención al cliente

class TeslaChatbot {
    constructor() {
        this.apiUrl = 'http://localhost:8000/api/chat';
        this.conversationHistory = [];
        this.currentStage = 'greeting';
        this.userData = {};
        this.serviceContext = null;
        
        // Base de conocimiento especializada
        this.knowledgeBase = {
            servicios: {
                itse: {
                    tipos: ['ITSE Básica', 'ITSE de Detalle', 'ITSE Ex-Post'],
                    sectores: ['restaurante', 'comercio', 'industria', 'vivienda'],
                    precios: {
                        restaurante: { min: 800, max: 1200, tiempo: '7-10 días' },
                        comercio: { min: 600, max: 1000, tiempo: '5-8 días' },
                        industria: { min: 1500, max: 3000, tiempo: '10-15 días' },
                        vivienda: { min: 400, max: 800, tiempo: '3-5 días' }
                    }
                },
                instalaciones: {
                    tipos: ['Residencial', 'Comercial', 'Industrial'],
                    precios_punto: { residencial: 85, comercial: 120, industrial: 150 },
                    servicios: ['Cableado', 'Tableros', 'Tomacorrientes', 'Iluminación']
                },
                automatizacion: {
                    tipos: ['Domótica', 'Industrial', 'Comercial'],
                    sistemas: ['Control luces', 'Sensores', 'Cámaras', 'Alarmas'],
                    precio_base: 2500
                },
                mantenimiento: {
                    tipos: ['Preventivo', 'Correctivo', 'Predictivo'],
                    frecuencia: ['Mensual', 'Trimestral', 'Semestral'],
                    precio_mes: 300
                }
            }
        };

        // Flujo conversacional
        this.conversationFlow = {
            greeting: {
                triggers: ['hola', 'buenos', 'saludos', 'consulta'],
                responses: [
                    "¡Buenos días! Soy TeslaBot, su asistente virtual de Tesla Electricidad. Estoy aquí para brindarle información sobre nuestros servicios eléctricos profesionales.",
                    "¡Bienvenido a Tesla Electricidad! Estoy aquí para ayudarle con cualquier consulta sobre servicios eléctricos.",
                    "Hola, ¿en qué puedo ayudarle hoy? Soy TeslaBot, su asistente virtual de servicios eléctricos."
                ],
                nextStage: 'service_identification',
                quickReplies: [
                    { text: '📋 Certificado ITSE', value: 'itse' },
                    { text: '⚡ Instalaciones', value: 'instalacion' },
                    { text: '🏠 Automatización', value: 'automatizacion' },
                    { text: '🔧 Mantenimiento', value: 'mantenimiento' }
                ]
            },
            service_identification: {
                triggers: ['itse', 'instalacion', 'automatizacion', 'mantenimiento'],
                responses: {
                    itse: "¡Excelente elección! El certificado ITSE es esencial para garantizar la seguridad de su local. ¿Qué tipo de negocio tiene?",
                    instalacion: "Perfecto, ¿necesita instalación eléctrica para su hogar o negocio?",
                    automatizacion: "¡Bien! La automatización puede hacer su vida más fácil. ¿Qué le gustaría automatizar?",
                    mantenimiento: "El mantenimiento preventivo es clave para evitar fallas. ¿Qué tipo de mantenimiento necesita?"
                },
                nextStage: 'specification_gathering'
            },
            specification_gathering: {
                questions: {
                    itse: [
                        '¿Qué tipo de negocio tiene? (restaurante, comercio, industria, vivienda)',
                        '¿Cuántos metros cuadrados tiene el local?',
                        '¿Es un local nuevo o existente?'
                    ],
                    instalacion: [
                        '¿Cuántos puntos eléctricos necesita instalar?',
                        '¿Es para uso residencial o comercial?',
                        '¿Requiere instalación completa o ampliación?'
                    ],
                    automatizacion: [
                        '¿Qué sistemas le gustaría automatizar? (luces, persianas, seguridad, etc.)',
                        '¿Qué área desea automatizar? (hogar completo, sala, habitaciones, etc.)',
                        '¿Tiene algún sistema de automatización actualmente?'
                    ],
                    mantenimiento: [
                        '¿Qué tipo de mantenimiento necesita? (preventivo, correctivo, predictivo)',
                        '¿Con qué frecuencia desea el servicio? (mensual, trimestral, semestral)',
                        '¿Qué equipos o instalaciones requieren mantenimiento?'
                    ]
                },
                nextStage: 'quotation',
                responses: {
                    itse: "Gracias por la información. Para un local de {tipo} de {metros} m², el costo aproximado sería entre S/ {min} y S/ {max}.",
                    instalacion: "Para {puntos} puntos eléctricos de tipo {tipo}, el costo aproximado sería de S/ {total}.",
                    automatizacion: "Para la automatización de {sistema} en {area}, el costo aproximado sería de S/ {total}.",
                    mantenimiento: "El servicio de mantenimiento {tipo} con frecuencia {frecuencia} tiene un costo de S/ {total} mensuales."
                }
            },
            quotation: {
                responses: {
                    itse: "¿Desea agendar una visita técnica para una evaluación más precisa?",
                    instalacion: "¿Le gustaría que un técnico evalúe su instalación?",
                    automatizacion: "¿Desea que un asesor especializado lo contacte?",
                    mantenimiento: "¿Desea programar el mantenimiento ahora?"
                },
                quickReplies: [
                    { text: 'Sí, agendar visita', value: 'agendar_visita' },
                    { text: 'Más información', value: 'mas_informacion' },
                    { text: 'Contactar con un asesor', value: 'contactar_asesor' }
                ],
                nextStage: 'follow_up'
            },
            follow_up: {
                responses: {
                    agendar_visita: "Por favor, indíquenos un número de teléfono y disponibilidad para la visita.",
                    mas_informacion: "¿Sobre qué aspecto necesita más información?",
                    contactar_asesor: "Un asesor se pondrá en contacto con usted a la brevedad. ¿En qué horario prefiere que lo llamemos?"
                },
                nextStage: 'closing'
            },
            closing: {
                responses: {
                    default: "¡Gracias por contactar con Tesla Electricidad! ¿Hay algo más en lo que pueda ayudarle?"
                },
                nextStage: 'greeting'
            }
        };
    }
        // Base de conocimiento especializada
        this.knowledgeBase = {
            servicios: {
                itse: {
                    tipos: ['ITSE Básica', 'ITSE de Detalle', 'ITSE Ex-Post'],
                    sectores: ['restaurante', 'comercio', 'industria', 'vivienda'],
                    precios: {
                        restaurante: { min: 800, max: 1200, tiempo: '7-10 días' },
                        comercio: { min: 600, max: 1000, tiempo: '5-8 días' },
                        industria: { min: 1500, max: 3000, tiempo: '10-15 días' },
                        vivienda: { min: 400, max: 800, tiempo: '3-5 días' }
                    }
                },
                instalaciones: {
                    tipos: ['Residencial', 'Comercial', 'Industrial'],
                    precios_punto: { residencial: 85, comercial: 120, industrial: 150 },
                    servicios: ['Cableado', 'Tableros', 'Tomacorrientes', 'Iluminación']
                },
                automatizacion: {
                    tipos: ['Domótica', 'Industrial', 'Comercial'],
                    sistemas: ['Control luces', 'Sensores', 'Cámaras', 'Alarmas'],
                    precio_base: 2500
                },
                mantenimiento: {
                    tipos: ['Preventivo', 'Correctivo', 'Predictivo'],
                    frecuencia: ['Mensual', 'Trimestral', 'Semestral'],
                    precio_mes: 300
                }
            }
        };

        // Flujo conversacional
        this.conversationFlow = {
            greeting: {
                triggers: ['hola', 'buenos', 'saludos', 'consulta'],
                responses: [
                    "¡Buenos días! Soy TeslaBot, su asistente virtual de Tesla Electricidad. Estoy aquí para brindarle información sobre nuestros servicios eléctricos profesionales.",
                    "¡Bienvenido a Tesla Electricidad! Estoy aquí para ayudarle con cualquier consulta sobre servicios eléctricos.",
                    "Hola, ¿en qué puedo ayudarle hoy? Soy TeslaBot, su asistente virtual de servicios eléctricos."
                ],
                nextStage: 'service_identification',
                quickReplies: [
                    { text: '📋 Certificado ITSE', value: 'itse' },
                    { text: '⚡ Instalaciones', value: 'instalacion' },
                    { text: '🏠 Automatización', value: 'automatizacion' },
                    { text: '🔧 Mantenimiento', value: 'mantenimiento' }
                ]
            },
            service_identification: {
                triggers: ['itse', 'instalacion', 'automatizacion', 'mantenimiento'],
                responses: {
                    itse: "¡Excelente elección! El certificado ITSE es esencial para garantizar la seguridad de su local. ¿Qué tipo de negocio tiene?",
                    instalacion: "Perfecto, ¿necesita instalación eléctrica para su hogar o negocio?",
                    automatizacion: "¡Bien! La automatización puede hacer su vida más fácil. ¿Qué le gustaría automatizar?",
                    mantenimiento: "El mantenimiento preventivo es clave para evitar fallas. ¿Qué tipo de mantenimiento necesita?"
                },
                nextStage: 'specification_gathering'
            },
            specification_gathering: {
                questions: {
                    itse: [
                        '¿Qué tipo de negocio tiene? (restaurante, comercio, industria, vivienda)',
                        '¿Cuántos metros cuadrados tiene el local?',
                        '¿Es un local nuevo o existente?'
                    ],
                    instalacion: [
                        '¿Cuántos puntos eléctricos necesita instalar?',
                        '¿Es para uso residencial o comercial?',
                        '¿Requiere instalación completa o ampliación?'
                    ],
                    automatizacion: [
                        '¿Qué sistemas le gustaría automatizar? (luces, persianas, seguridad, etc.)',
                        '¿Qué área desea automatizar? (hogar completo, sala, habitaciones, etc.)',
                        '¿Tiene algún sistema de automatización actualmente?'
                    ],
                    mantenimiento: [
                        '¿Qué tipo de mantenimiento necesita? (preventivo, correctivo, predictivo)',
                        '¿Con qué frecuencia desea el servicio? (mensual, trimestral, semestral)',
                        '¿Qué equipos o instalaciones requieren mantenimiento?'
                    ]
                },
                nextStage: 'quotation',
                responses: {
                    itse: "Gracias por la información. Para un local de {tipo} de {metros} m², el costo aproximado sería entre S/ {min} y S/ {max}.",
                    instalacion: "Para {puntos} puntos eléctricos de tipo {tipo}, el costo aproximado sería de S/ {total}.",
                    automatizacion: "Para la automatización de {sistema} en {area}, el costo aproximado sería de S/ {total}.",
                    mantenimiento: "El servicio de mantenimiento {tipo} con frecuencia {frecuencia} tiene un costo de S/ {total} mensuales."
                }
            },
            quotation: {
                nextStage: 'data_collection',
                responses: {
                    default: "¿Le gustaría que un asesor se comunique con usted para brindarle una cotización personalizada?"
                },
                quickReplies: [
                    { text: 'Sí, por favor', value: 'si' },
                    { text: 'No, gracias', value: 'no' }
                ]
            },
            data_collection: {
                fields: [
                    { name: 'nombre', question: 'Por favor, ingrese su nombre completo:', type: 'text' },
                    { name: 'telefono', question: 'Ingrese su número de teléfono:', type: 'tel' },
                    { name: 'email', question: 'Ingrese su correo electrónico:', type: 'email' },
                    { name: 'direccion', question: '¿Cuál es su dirección para la cotización?', type: 'text' }
                ],
                nextStage: 'confirmation',
                response: "Gracias por la información. Un asesor se comunicará con usted a la brevedad."
            },
            confirmation: {
                response: "¡Listo! Hemos registrado su solicitud. ¿Hay algo más en lo que pueda ayudarle hoy?",
                nextStage: 'greeting',
                quickReplies: [
                    { text: 'Sí, tengo otra consulta', value: 'si' },
                    { text: 'No, gracias', value: 'no' }
                ]
            }
        };
    }

    // Inicializar chatbot
    init() {
        this.createChatInterface();
        this.bindEvents();
        this.sendWelcomeMessage();
        
        // Asegurar que el input esté enfocado al hacer clic en el chat
        const chatContainer = document.getElementById('chat-container');
        const chatInput = document.getElementById('chat-input');
        
        chatContainer.addEventListener('click', (e) => {
            if (e.target.closest('.chat-messages') || e.target.closest('.chat-header')) {
                chatInput.focus();
            }
        });
        
        // Enfocar el input cuando se muestra el chat
        const chatHeader = document.querySelector('.chat-header');
        if (chatHeader) {
            chatHeader.addEventListener('click', () => {
                setTimeout(() => {
                    chatInput.focus();
                }, 300);
            });
        }
    }

    // Enviar mensaje de bienvenida
    sendWelcomeMessage() {
        const hora = new Date().getHours();
        let saludo = 'Buenos días';
        
        if (hora >= 12 && hora < 19) {
            saludo = 'Buenas tardes';
        } else if (hora >= 19 || hora < 6) {
            saludo = 'Buenas noches';
        }
        
        const welcomeMsg = `${saludo} 👋\n\nSoy TeslaBot, su asistente virtual de Tesla Electricidad. Estoy aquí para brindarle información sobre nuestros servicios eléctricos profesionales.\n\n¿En qué puedo ayudarle hoy?`;
        
        this.addBotMessage(welcomeMsg);
        this.showQuickReplies(this.conversationFlow.greeting.quickReplies);
    }

    // Crear interfaz de chat
    createChatInterface() {
        const chatContainer = document.createElement('div');
        chatContainer.id = 'chat-container';
        chatContainer.className = 'chat-container';
        
        chatContainer.innerHTML = `
            <div class="chat-header">
                <div class="bot-avatar">
                    <i class="fas fa-bolt"></i>
                </div>
                <div class="bot-info">
                    <h4>TeslaBot</h4>
                    <span class="status online">En línea</span>
                </div>
                <button class="chat-minimize" onclick="toggleChat()">
                    <i class="fas fa-minus"></i>
                </button>
            </div>
            <div class="chat-messages" id="chat-messages"></div>
            <div class="chat-input-container">
                <input type="text" id="chat-input" placeholder="Escribe tu mensaje..." autocomplete="off">
                <button id="send-btn">
                    <i class="fas fa-paper-plane"></i>
                </button>
            </div>
            <div class="quick-actions" id="quick-actions"></div>
        `;
        
        document.body.appendChild(chatContainer);
        this.injectChatStyles();
    }

    // Inyectar estilos CSS
    injectChatStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .chat-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 380px;
                height: 600px;
                background: white;
                border-radius: 15px;
                box-shadow: 0 5px 25px rgba(0, 0, 0, 0.2);
                display: flex;
                flex-direction: column;
                overflow: hidden;
                z-index: 1000;
                font-family: 'Poppins', sans-serif;
            }
            
            .chat-header {
                background: linear-gradient(135deg, #0f3460, #16213e);
                color: white;
                padding: 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .bot-avatar {
                width: 40px;
                height: 40px;
                background: #e94560;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                margin-right: 10px;
            }
            
            .bot-info {
                flex: 1;
            }
            
            .bot-info h4 {
                margin: 0;
                font-size: 16px;
            }
            
            .status {
                font-size: 12px;
                opacity: 0.8;
            }
            
            .online {
                color: #4caf50;
            }
            
            .chat-messages {
                flex: 1;
                padding: 15px;
                overflow-y: auto;
                background: #f5f7fb;
            }
            
            .message {
                margin-bottom: 15px;
                max-width: 80%;
                padding: 10px 15px;
                border-radius: 18px;
                line-height: 1.4;
                position: relative;
                animation: fadeIn 0.3s ease;
            }
            
            .bot-message {
                background: white;
                color: #333;
                border-top-left-radius: 5px;
                align-self: flex-start;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .user-message {
                background: #0f3460;
                color: white;
                border-top-right-radius: 5px;
                margin-left: auto;
            }
            
            .chat-input-container {
                display: flex;
                padding: 15px;
                background: white;
                border-top: 1px solid #eee;
            }
            
            #chat-input {
                flex: 1;
                padding: 12px 15px;
                border: 1px solid #ddd;
                border-radius: 25px;
                outline: none;
                font-family: 'Poppins', sans-serif;
                font-size: 14px;
            }
            
            #send-btn {
                width: 45px;
                height: 45px;
                border-radius: 50%;
                background: #0f3460;
                color: white;
                border: none;
                margin-left: 10px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: all 0.3s ease;
            }
            
            #send-btn:hover {
                background: #16213e;
                transform: translateY(-2px);
            }
            
            .quick-actions {
                display: flex;
                flex-wrap: wrap;
                padding: 10px;
                gap: 8px;
                background: #f9f9f9;
                border-top: 1px solid #eee;
            }
            
            .quick-btn {
                background: white;
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 8px 15px;
                font-size: 13px;
                cursor: pointer;
                transition: all 0.2s ease;
                display: flex;
                align-items: center;
                gap: 5px;
            }
            
            .quick-btn:hover {
                background: #f0f0f0;
                transform: translateY(-2px);
            }
            
            .typing-indicator {
                display: flex;
                padding: 10px 15px;
                background: white;
                border-radius: 18px;
                width: fit-content;
                margin-bottom: 15px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1);
            }
            
            .typing-dot {
                width: 8px;
                height: 8px;
                background: #ccc;
                border-radius: 50%;
                margin: 0 2px;
                animation: typing 1.4s infinite ease-in-out;
            }
            
            .typing-dot:nth-child(1) { animation-delay: 0s; }
            .typing-dot:nth-child(2) { animation-delay: 0.2s; }
            .typing-dot:nth-child(3) { animation-delay: 0.4s; }
            
            @keyframes typing {
                0%, 60%, 100% { transform: translateY(0); }
                30% { transform: translateY(-5px); }
            }
            
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            
            .chat-container.minimized {
                height: 60px;
                overflow: hidden;
            }
            
            .chat-container.minimized .chat-messages,
            .chat-container.minimized .chat-input-container,
            .chat-container.minimized .quick-actions {
                display: none;
            }
            
            .chat-container.minimized .chat-header {
                cursor: pointer;
            }
            
            @media (max-width: 480px) {
                .chat-container {
                    width: 100%;
                    height: 100%;
                    bottom: 0;
                    right: 0;
                    border-radius: 0;
                }
                
                .message {
                    max-width: 90%;
                }
            }
        `;
        document.head.appendChild(style);
    }
    
    // Inicializar el chatbot
    init() {
        this.createChatInterface();
        this.bindEvents();
        this.sendWelcomeMessage();
        
        // Asegurar que el input esté enfocado al hacer clic en el chat
        const chatContainer = document.getElementById('chat-container');
        const chatInput = document.getElementById('chat-input');
        
        chatContainer.addEventListener('click', (e) => {
            if (e.target.closest('.chat-messages') || e.target.closest('.chat-header')) {
                chatInput.focus();
            }
        });
        
        // Enfocar el input cuando se muestra el chat
        const chatHeader = document.querySelector('.chat-header');
        if (chatHeader) {
            chatHeader.addEventListener('click', () => {
                setTimeout(() => {
                    chatInput.focus();
                }, 300);
            });
        }
    }

    // Crear la interfaz del chat
    createChatInterface() {
        const chatHTML = `
            <div class="chat-container" id="chat-container">
                <div class="chat-header" id="chat-header">
                    <h4>TeslaBot - Asistente Virtual</h4>
                    <button id="minimize-chat">_</button>
                </div>
                <div class="chat-messages" id="chat-messages"></div>
                <div class="quick-actions" id="quick-actions"></div>
                <div class="chat-input-container">
                    <input type="text" id="chat-input" placeholder="Escribe tu mensaje..." />
                    <button id="send-btn">
                        <i class="fas fa-paper-plane"></i>
                    </button>
                </div>
            </div>
        `;
        
        document.body.insertAdjacentHTML('beforeend', chatHTML);
        this.addStyles();
    }

    // Agregar estilos CSS
    addStyles() {
        const style = document.createElement('style');
        style.textContent = `
            .chat-container {
                position: fixed;
                bottom: 20px;
                right: 20px;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 10px;
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                display: flex;
                flex-direction: column;
                z-index: 1000;
                overflow: hidden;
                font-family: 'Poppins', sans-serif;
            }
            
            .chat-header {
                background: #0f3460;
                color: white;
                padding: 15px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                cursor: pointer;
            }
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid #ddd;
    }
    
    .chat-header h4 {
        margin: 0;
        font-size: 16px;
    }
    
    .chat-header button {
        background: none;
        border: none;
        color: white;
        cursor: pointer;
    }
    
    .chat-messages {
        flex: 1;
        padding: 15px;
        overflow-y: auto;
        background: #f5f7fb;
    }
    
    .message {
        margin-bottom: 15px;
        max-width: 80%;
        padding: 10px 15px;
        border-radius: 18px;
        line-height: 1.4;
        position: relative;
        animation: fadeIn 0.3s ease;
    }
    
    .bot-message {
        background: white;
        color: #333;
        border-top-left-radius: 5px;
        align-self: flex-start;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .user-message {
        background: #0f3460;
        color: white;
        border-top-right-radius: 5px;
        margin-left: auto;
    }
    
    .chat-input-container {
        display: flex;
        padding: 15px;
        background: white;
        border-top: 1px solid #eee;
    }
    
    #chat-input {
        flex: 1;
        padding: 12px 15px;
        border: 1px solid #ddd;
        border-radius: 25px;
        outline: none;
        font-family: 'Poppins', sans-serif;
        font-size: 14px;
    }
    
    #send-btn {
        width: 45px;
        height: 45px;
        border-radius: 50%;
        background: #0f3460;
        color: white;
        border: none;
        margin-left: 10px;
        cursor: pointer;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s ease;
    }
    
    #send-btn:hover {
        background: #16213e;
        transform: translateY(-2px);
    }
    
    .quick-actions {
        display: flex;
        flex-wrap: wrap;
        padding: 10px;
        gap: 8px;
        background: #f9f9f9;
        border-top: 1px solid #eee;
    }
    
    .quick-btn {
        background: white;
        border: 1px solid #ddd;
        border-radius: 20px;
        padding: 8px 15px;
        font-size: 13px;
        cursor: pointer;
        transition: all 0.2s ease;
        display: flex;
        align-items: center;
        gap: 5px;
    }
    
    .quick-btn:hover {
        background: #f0f0f0;
        transform: translateY(-2px);
    }
    
    .typing-indicator {
        display: flex;
        padding: 10px 15px;
        background: white;
        border-radius: 18px;
        width: fit-content;
        margin-bottom: 15px;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    .typing-dot {
        width: 8px;
        height: 8px;
        background: #ccc;
        border-radius: 50%;
        margin: 0 2px;
        animation: typing 1.4s infinite ease-in-out;
    }
    
    .typing-dot:nth-child(1) { animation-delay: 0s; }
    .typing-dot:nth-child(2) { animation-delay: 0.2s; }
    .typing-dot:nth-child(3) { animation-delay: 0.4s; }
    
    @keyframes typing {
        0%, 60%, 100% { transform: translateY(0); }
        30% { transform: translateY(-5px); }
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .chat-container.minimized {
        height: 60px;
        overflow: hidden;
    }
    
    .chat-container.minimized .chat-messages,
    .chat-container.minimized .chat-input-container,
    .chat-container.minimized .quick-actions {
        display: none;
    }
    
    .chat-container.minimized .chat-header {
        cursor: pointer;
    }
    
    @media (max-width: 480px) {
        .chat-container {
            width: 100%;
            height: 100%;
            bottom: 0;
            right: 0;
            border-radius: 0;
        }
        
        .message {
            max-width: 90%;
        }
    }
`;
document.head.appendChild(style);

// Clase para el chat
    // Enviar mensaje de bienvenida
    sendWelcomeMessage() {
        const hora = new Date().getHours();
        let saludo = 'Buenos días';
        
        if (hora >= 12 && hora < 19) {
            saludo = 'Buenas tardes';
        } else if (hora >= 19 || hora < 6) {
            saludo = 'Buenas noches';
        }

        const mensajeBienvenida = `${saludo}, soy TeslaBot, su asistente virtual de Tesla Electricidad. ¿En qué puedo ayudarle hoy?`;
        
        // Mostrar mensaje de bienvenida después de un pequeño retraso
        setTimeout(() => {
            this.addBotMessage(mensajeBienvenida);
            
            // Mostrar botones de acción rápida
            const quickActions = document.getElementById('quick-actions');
            if (quickActions) {
                quickActions.innerHTML = `
                    <button class="quick-btn" data-value="itse">📋 Certificado ITSE</button>
                    <button class="quick-btn" data-value="instalacion">⚡ Instalaciones</button>
                    <button class="quick-btn" data-value="automatizacion">🏠 Automatización</button>
                    <button class="quick-btn" data-value="mantenimiento">🔧 Mantenimiento</button>
                `;
                
                // Volver a vincular eventos para los nuevos botones
                document.querySelectorAll('.quick-btn').forEach(btn => {
                    btn.addEventListener('click', (e) => {
                        e.preventDefault();
                        const value = e.target.getAttribute('data-value');
                        this.handleQuickAction(value);
                    });
                });
            }
        }, 1000);
    }

    // Mostrar indicador de escritura
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        
        const typingDiv = document.createElement('div');
        typingDiv.className = 'typing-indicator';
        typingDiv.id = 'typing-indicator';
        typingDiv.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Eliminar indicador de escritura
    removeTypingIndicator() {
        const typingIndicator = document.getElementById('typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }

    // Agregar mensaje del usuario
    addUserMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message user-message';
        messageDiv.textContent = message;
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Agregar mensaje del bot
    addBotMessage(message) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        
        // Eliminar indicador de escritura si existe
        this.removeTypingIndicator();
        
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message bot-message';
        messageDiv.innerHTML = message.replace(/\n/g, '<br>');
        
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    // Procesar entrada del usuario
    async processUserInput(input) {
        if (!input || !input.trim()) return;
        
        // Agregar mensaje del usuario al historial
        this.conversationHistory.push({
            role: 'user',
            content: input
        });
        
        // Mostrar indicador de escritura
        this.showTypingIndicator();
        
        try {
            // Procesar el mensaje según la etapa actual
            let response = '';
            const currentStage = this.conversationFlow[this.currentStage];
            
            if (this.currentStage === 'greeting') {
                // Verificar si la entrada coincide con algún disparador de servicio
                const servicio = Object.keys(this.knowledgeBase.servicios).find(servicio => 
                    input.toLowerCase().includes(servicio)
                );
                
                if (servicio) {
                    this.serviceContext = servicio;
                    this.currentStage = 'service_identification';
                    response = currentStage.responses[servicio] || "Entendido, ¿en qué puedo ayudarte con este servicio?";
                } else {
                    response = "Por favor, seleccione un servicio para continuar:";
                }
            } 
            // Agregar más lógica para otras etapas...
            
            // Simular una respuesta del servidor
            await new Promise(resolve => setTimeout(resolve, 1000));
            
            // Agregar la respuesta al historial
            this.conversationHistory.push({
                role: 'assistant',
                content: response
            });
            
            // Mostrar la respuesta
            this.addBotMessage(response);
            
            // Mostrar botones de acción rápida si los hay
            if (currentStage.quickReplies) {
                this.showQuickReplies(currentStage.quickReplies);
            }
            
        } catch (error) {
            console.error('Error al procesar el mensaje:', error);
            this.addBotMessage("Lo siento, ha ocurrido un error. Por favor, inténtelo de nuevo más tarde.");
        } finally {
            this.removeTypingIndicator();
        }
    }

    // Mostrar botones de respuesta rápida
    showQuickReplies(quickReplies) {
        const quickActions = document.getElementById('quick-actions');
        if (!quickReplies || !quickActions) return;
        
        quickActions.innerHTML = quickReplies
            .map(reply => 
                `<button class="quick-btn" data-value="${reply.value}">${reply.text}</button>`
            )
            .join('');
        
        // Volver a vincular eventos para los nuevos botones
        document.querySelectorAll('.quick-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const value = e.target.getAttribute('data-value');
                this.handleQuickAction(value);
            });
        });
    }

    // Manejar acciones rápidas
    handleQuickAction(action) {
        switch(action) {
            case 'agendar_visita':
                this.addBotMessage("Por favor, indíquenos un número de teléfono y disponibilidad para la visita.");
                break;
            case 'mas_informacion':
                this.addBotMessage("¿Sobre qué aspecto necesita más información?");
                break;
            case 'contactar_asesor':
                this.addBotMessage("Un asesor se pondrá en contacto con usted a la brevedad. ¿En qué horario prefiere que lo llamemos?");
                break;
            default:
                this.processUserInput(action);
        }
    }

    // Vincular eventos
    bindEvents() {
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const quickBtns = document.querySelectorAll('.quick-btn');
        const minimizeBtn = document.getElementById('minimize-chat');
        const chatContainer = document.getElementById('chat-container');

        // Manejar el envío de mensajes con Enter
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Manejar clic en el botón de enviar
        sendBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Manejar botones rápidos
        quickBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const value = e.target.getAttribute('data-value');
                this.handleQuickAction(value);
            });
        });

        // Minimizar/expandir chat
        if (minimizeBtn) {
            minimizeBtn.addEventListener('click', (e) => {
                e.stopPropagation();
                chatContainer.classList.toggle('minimized');
                minimizeBtn.textContent = chatContainer.classList.contains('minimized') ? '+' : '_';
            });
        }

        // Asegurar que el input esté siempre enfocado cuando el chat está visible
        document.addEventListener('click', (e) => {
            if (e.target.closest('#chat-container') && !e.target.closest('.chat-input-container')) {
                chatInput.focus();
            }
        });
    }

    // Enviar mensaje
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();
        
        if (!message) return;

        // Deshabilitar temporalmente el input y el botón
        input.disabled = true;
        const sendBtn = document.getElementById('send-btn');
        sendBtn.disabled = true;
        
        this.addUserMessage(message);
        input.value = '';

        // Procesar el mensaje
        await this.processUserInput(message);
        
        // Re-habilitar el input y el botón
        input.disabled = false;
        sendBtn.disabled = false;
        input.focus();
    }
}

// Inicializar el chatbot cuando el DOM esté cargado
document.addEventListener('DOMContentLoaded', () => {
    const chatbot = new TeslaChatbot();
    chatbot.init();
});
        this.chatInput = document.getElementById('chat-input');
        this.sendBtn = document.getElementById('send-btn');
        this.quickActions = document.getElementById('quick-actions');
    }

    // Vincular eventos
    bindEvents() {
        const chatInput = document.getElementById('chat-input');
        const sendBtn = document.getElementById('send-btn');
        const quickBtns = document.querySelectorAll('.quick-btn');

        // Manejar el envío de mensajes con Enter
        chatInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                this.sendMessage();
            }
        });

        // Manejar clic en el botón de enviar
        sendBtn.addEventListener('click', (e) => {
            e.preventDefault();
            this.sendMessage();
        });

        // Manejar botones rápidos
        quickBtns.forEach(btn => {
            btn.addEventListener('click', (e) => {
                e.preventDefault();
                const service = e.target.getAttribute('data-service');
                this.handleQuickAction(service);
            });
        });

        // Asegurar que el input esté siempre enfocado cuando el chat está visible
        document.addEventListener('click', (e) => {
            if (e.target.closest('#chat-container') && !e.target.closest('.chat-input-container')) {
                chatInput.focus();
            }
        });
    }

    // Enviar mensaje usuario
    async sendMessage() {
        const input = document.getElementById('chat-input');
        const message = input.value.trim();

        if (!message) return;

        // Deshabilitar temporalmente el input y el botón
        input.disabled = true;
        const sendBtn = document.getElementById('send-btn');
        sendBtn.disabled = true;

        this.addUserMessage(message);
        input.value = '';

        // Mostrar indicador de escritura
        this.showTypingIndicator();

        try {
            const response = await this.processMessage(message);
            this.removeTypingIndicator();
            this.addBotMessage(response);
        } catch (error) {
            console.error('Error al procesar el mensaje:', error);
            this.removeTypingIndicator();
            const fallbackResponse = this.getFallbackResponse(message);
            this.addBotMessage(fallbackResponse);
        } finally {
            // Re-habilitar el input y el botón
            input.disabled = false;
            sendBtn.disabled = false;
            input.focus();
        }

        // Hacer scroll al final de los mensajes
        this.scrollToBottom();
    }

    // Procesar la entrada del usuario
    processUserInput(input) {
        // Aquí iría la lógica para procesar la entrada del usuario
        // y determinar la respuesta adecuada según el flujo de conversación

        // Por ahora, solo mostramos un mensaje de respuesta genérico
        setTimeout(() => {
            this.addBotMessage('Gracias por su mensaje. Un asesor se pondrá en contacto con usted pronto.');
        }, 1000);
    }

    // Mostrar botones de respuesta rápida
    showQuickReplies(quickReplies) {
        const quickActions = document.getElementById('quick-actions');
        if (!quickReplies || !quickActions) return;
        
        quickActions.innerHTML = quickReplies
            .map(reply => 
                `<button class="quick-btn" data-value="${reply.value}">${reply.text}</button>`
            )
            .join('');
    }
    
    // Agregar mensaje del bot
    addBotMessage(text) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = 'message bot-message';
        messageElement.innerHTML = text.replace(/\n/g, '<br>');
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Agregar mensaje del usuario
    addUserMessage(text) {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return;
        
        const messageElement = document.createElement('div');
        messageElement.className = 'message user-message';
        messageElement.textContent = text;
        
        messagesContainer.appendChild(messageElement);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    // Mostrar indicador de escritura
    showTypingIndicator() {
        const messagesContainer = document.getElementById('chat-messages');
        if (!messagesContainer) return null;
        
        const indicator = document.createElement('div');
        indicator.className = 'typing-indicator';
        indicator.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        messagesContainer.appendChild(indicator);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        return indicator;
    }
    
    // Ocultar indicador de escritura
    hideTypingIndicator(indicator) {
        if (indicator && indicator.parentNode) {
            indicator.parentNode.removeChild(indicator);
        }
    }
