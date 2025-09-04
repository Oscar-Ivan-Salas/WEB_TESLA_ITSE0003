// Sistema de Automatización de Comunicación y Formularios para Tesla Electricidad

class TeslaAutomation {
    constructor() {
        this.apiUrl = 'http://localhost:8000/api';
        this.whatsappNumber = '51987654321';
        this.telegramBot = '@tesla_electricidad_bot';
        this.emailService = true;
        this.notifications = {
            browser: true,
            sound: true,
            vibration: true
        };
    }

    // Inicializar sistema de automatización
    init() {
        this.setupFormAutomation();
        this.setupNotifications();
        this.setupRealTimeUpdates();
        this.initServiceWorker();
    }

    // Configurar automatización de formularios
    setupFormAutomation() {
        // Formulario principal de contacto
        const contactForm = document.getElementById('contact-form');
        if (contactForm) {
            contactForm.addEventListener('submit', (e) => this.handleContactSubmit(e));
        }

        // Formularios de servicios específicos
        const serviceButtons = document.querySelectorAll('[data-service-request]');
        serviceButtons.forEach(button => {
            button.addEventListener('click', (e) => this.handleServiceRequest(e));
        });

        // Auto-completado inteligente
        this.setupSmartAutocomplete();

        // Validación en tiempo real
        this.setupRealTimeValidation();
    }

    // Manejar envío de formulario principal
    async handleContactSubmit(event) {
        event.preventDefault();
        
        const formData = new FormData(event.target);
        const contactData = {
            nombre: formData.get('nombre'),
            telefono: formData.get('telefono'),
            email: formData.get('email'),
            servicio: formData.get('servicio'),
            mensaje: formData.get('mensaje')
        };

        // Validar datos
        if (!this.validateContactData(contactData)) {
            return;
        }

        // Mostrar loading
        this.showFormLoading(event.target);

        try {
            // Enviar al backend
            const response = await fetch(`${this.apiUrl}/contact`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(contactData)
            });

            const result = await response.json();

            if (result.success) {
                // Automatización inmediata post-envío
                await this.triggerAutomations(contactData, result.lead_id);
                
                // Mostrar éxito
                this.showSuccessMessage(contactData);
                
                // Resetear formulario
                event.target.reset();
            } else {
                throw new Error(result.message || 'Error procesando solicitud');
            }

        } catch (error) {
            console.error('Error enviando formulario:', error);
            this.showErrorMessage('Error enviando solicitud. Intenta por WhatsApp directo.');
            
            // Fallback: abrir WhatsApp
            this.openWhatsAppFallback(contactData);
        } finally {
            this.hideFormLoading(event.target);
        }
    }

    // Disparar automatizaciones post-contacto
    async triggerAutomations(contactData, leadId) {
        const promises = [];

        // 1. WhatsApp automático inmediato
        promises.push(this.sendAutoWhatsApp(contactData, leadId));

        // 2. Email de confirmación
        if (this.emailService && contactData.email) {
            promises.push(this.sendConfirmationEmail(contactData));
        }

        // 3. Notificación a especialistas
        promises.push(this.notifySpecialists(contactData, leadId));

        // 4. Agendar seguimiento automático
        promises.push(this.scheduleFollowUp(contactData, leadId));

        // 5. Actualizar analytics
        promises.push(this.updateAnalytics(contactData.servicio));

        // Ejecutar todas las automatizaciones
        try {
            await Promise.allSettled(promises);
        } catch (error) {
            console.error('Error en automatizaciones:', error);
        }
    }

    // Envío automático de WhatsApp
    async sendAutoWhatsApp(contactData, leadId) {
        const message = this.generateWhatsAppMessage(contactData, leadId);
        
        try {
            // Intentar envío via API
            const response = await fetch(`${this.apiUrl}/whatsapp/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    to: contactData.telefono,
                    message: message
                })
            });
            
            const result = await response.json();
            return result.success;
            
        } catch (error) {
            console.error('Error enviando WhatsApp automático:', error);
            return false;
        }
    }

    // Generar mensaje de WhatsApp personalizado
    generateWhatsAppMessage(contactData, leadId) {
        return `¡Hola ${contactData.nombre}! 👋\n\n` +
               `Gracias por contactar a Tesla Electricidad.\n` +
               `Tu solicitud #${leadId} ha sido recibida.\n\n` +
               `📋 *Servicio solicitado:* ${contactData.servicio}\n` +
               `📞 *Contacto:* ${contactData.telefono}\n` +
               `📧 *Email:* ${contactData.email || 'No especificado'}\n\n` +
               `Un asesor se pondrá en contacto contigo en los próximos minutos.\n\n` +
               `*Tesla Electricidad - Energía Inteligente*`;
    }

    // Enviar email de confirmación
    async sendConfirmationEmail(contactData) {
        if (!contactData.email) return false;
        
        try {
            const response = await fetch(`${this.apiUrl}/email/send`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    to: contactData.email,
                    subject: 'Confirmación de contacto - Tesla Electricidad',
                    template: 'confirmation',
                    data: contactData
                })
            });
            
            return await response.json();
            
        } catch (error) {
            console.error('Error enviando email de confirmación:', error);
            return false;
        }
    }

    // Notificar a especialistas
    async notifySpecialists(contactData, leadId) {
        try {
            const response = await fetch(`${this.apiUrl}/notifications/specialists`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lead_id: leadId,
                    service: contactData.servicio,
                    priority: 'high'
                })
            });
            
            return await response.json();
            
        } catch (error) {
            console.error('Error notificando a especialistas:', error);
            return false;
        }
    }

    // Programar seguimiento automático
    async scheduleFollowUp(contactData, leadId) {
        try {
            const response = await fetch(`${this.apiUrl}/followups/schedule`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    lead_id: leadId,
                    contact_method: 'whatsapp',
                    delay_hours: 24,
                    message: `Hola ${contactData.nombre}, soy ${contactData.servicio} de Tesla Electricidad. ¿En qué te puedo ayudar hoy?`
                })
            });
            
            return await response.json();
            
        } catch (error) {
            console.error('Error programando seguimiento:', error);
            return false;
        }
    }

    // Actualizar analytics
    async updateAnalytics(service) {
        try {
            const response = await fetch(`${this.apiUrl}/analytics/track`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    event: 'service_request',
                    service: service,
                    timestamp: new Date().toISOString()
                })
            });
            
            return await response.json();
            
        } catch (error) {
            console.error('Error actualizando analytics:', error);
            return false;
        }
    }

    // Validar datos del formulario
    validateContactData(data) {
        if (!data.nombre || data.nombre.trim().length < 3) {
            this.showFieldError('nombre', 'Por favor ingresa tu nombre completo');
            return false;
        }

        if (!data.telefono || !/^[0-9]{9,15}$/.test(data.telefono)) {
            this.showFieldError('telefono', 'Ingresa un número de teléfono válido');
            return false;
        }

        if (data.email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(data.email)) {
            this.showFieldError('email', 'Ingresa un correo electrónico válido');
            return false;
        }

        if (!data.servicio) {
            this.showFieldError('servicio', 'Por favor selecciona un servicio');
            return false;
        }

        return true;
    }

    // Mostrar error en campo específico
    showFieldError(fieldId, message) {
        const field = document.getElementById(fieldId);
        if (!field) return;

        // Remover errores previos
        const existingError = field.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Agregar clase de error
        field.classList.add('error');

        // Crear y mostrar mensaje de error
        const errorElement = document.createElement('div');
        errorElement.className = 'error-message';
        errorElement.textContent = message;
        
        field.parentNode.insertBefore(errorElement, field.nextSibling);
        
        // Enfocar el campo con error
        field.focus();
        
        // Scroll al campo con error
        field.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }

    // Configurar auto-completado inteligente
    setupSmartAutocomplete() {
        // Implementar lógica de autocompletado
        // (puede integrarse con API de Google Places u otra fuente de datos)
    }

    // Configurar validación en tiempo real
    setupRealTimeValidation() {
        const validateField = (field, validator) => {
            field.addEventListener('input', () => {
                const value = field.value.trim();
                const isValid = validator(value);
                
                if (!isValid) {
                    field.classList.add('error');
                } else {
                    field.classList.remove('error');
                    const errorElement = field.parentElement.querySelector('.error-message');
                    if (errorElement) {
                        errorElement.remove();
                    }
                }
            });
        };

        // Validar nombre
        const nameField = document.getElementById('nombre');
        if (nameField) {
            validateField(nameField, value => value.length >= 3);
        }

        // Validar teléfono
        const phoneField = document.getElementById('telefono');
        if (phoneField) {
            validateField(phoneField, value => /^[0-9]{9,15}$/.test(value));
        }

        // Validar email
        const emailField = document.getElementById('email');
        if (emailField) {
            validateField(emailField, value => {
                if (!value) return true; // Opcional
                return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
            });
        }
    }

    // Mostrar loading en formulario
    showFormLoading(form) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = true;
            submitButton.innerHTML = '<span class="spinner"></span> Enviando...';
        }
    }

    // Ocultar loading del formulario
    hideFormLoading(form) {
        const submitButton = form.querySelector('button[type="submit"]');
        if (submitButton) {
            submitButton.disabled = false;
            submitButton.textContent = 'Enviar mensaje';
        }
    }

    // Mostrar mensaje de éxito
    showSuccessMessage(contactData) {
        // Mostrar notificación
        if (this.notifications.browser && 'Notification' in window) {
            const notification = new Notification('¡Mensaje enviado!', {
                body: `Gracias ${contactData.nombre}, te contactaremos pronto.`,
                icon: '/assets/images/logo.png'
            });
        }

        // Mostrar mensaje en la interfaz
        const successMessage = document.createElement('div');
        successMessage.className = 'success-message';
        successMessage.innerHTML = `
            <div class="success-icon">✓</div>
            <h3>¡Mensaje enviado con éxito!</h3>
            <p>Gracias ${contactData.nombre}, hemos recibido tu solicitud de <strong>${contactData.servicio}</strong>.</p>
            <p>Te contactaremos en breve al número <strong>${contactData.telefono}</strong>.</p>
            <button class="btn-close-message">Aceptar</button>
        `;

        document.body.appendChild(successMessage);

        // Cerrar mensaje al hacer clic
        const closeButton = successMessage.querySelector('.btn-close-message');
        closeButton.addEventListener('click', () => {
            successMessage.remove();
        });

        // Reproducir sonido de éxito
        if (this.notifications.sound) {
            const audio = new Audio('/assets/sounds/success.mp3');
            audio.play().catch(e => console.log('No se pudo reproducir el sonido:', e));
        }
    }

    // Mostrar mensaje de error
    showErrorMessage(message) {
        const errorMessage = document.createElement('div');
        errorMessage.className = 'error-message-global';
        errorMessage.innerHTML = `
            <div class="error-icon">!</div>
            <p>${message}</p>
            <button class="btn-close-message">×</button>
        `;

        document.body.appendChild(errorMessage);

        // Cerrar mensaje al hacer clic
        const closeButton = errorMessage.querySelector('.btn-close-message');
        closeButton.addEventListener('click', () => {
            errorMessage.remove();
        });

        // Ocultar automáticamente después de 5 segundos
        setTimeout(() => {
            errorMessage.remove();
        }, 5000);
    }

    // Abrir WhatsApp como fallback
    openWhatsAppFallback(contactData) {
        const message = `Hola, soy ${contactData.nombre}. Estoy interesado en: ${contactData.servicio}. ${contactData.mensaje || ''}`.substring(0, 200);
        const whatsappUrl = `https://wa.me/${this.whatsappNumber}?text=${encodeURIComponent(message)}`;
        window.open(whatsappUrl, '_blank');
    }

    // Configurar notificaciones del navegador
    setupNotifications() {
        if ('Notification' in window) {
            if (Notification.permission === 'granted') {
                // Ya tiene permisos
                this.notifications.browser = true;
            } else if (Notification.permission !== 'denied') {
                // Solicitar permiso
                Notification.requestPermission().then(permission => {
                    this.notifications.browser = permission === 'granted';
                });
            }
        }

        // Configurar vibración si está disponible
        if ('vibrate' in navigator) {
            this.notifications.vibration = true;
        }
    }

    // Configurar actualizaciones en tiempo real
    setupRealTimeUpdates() {
        // Implementar actualizaciones en tiempo real con WebSockets o Server-Sent Events
        // (requiere configuración adicional en el backend)
    }

    // Inicializar Service Worker para notificaciones push
    initServiceWorker() {
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('ServiceWorker registrado con éxito:', registration.scope);
                    })
                    .catch(error => {
                        console.log('Error al registrar el ServiceWorker:', error);
                    });
            });
        }
    }

    // Manejar solicitud de servicio específico
    handleServiceRequest(event) {
        event.preventDefault();
        
        const service = event.target.getAttribute('data-service-request');
        const serviceName = event.target.getAttribute('data-service-name') || service;
        
        // Desplazarse al formulario
        const contactSection = document.getElementById('contact');
        if (contactSection) {
            contactSection.scrollIntoView({ behavior: 'smooth' });
        }
        
        // Establecer el servicio seleccionado
        const serviceSelect = document.getElementById('servicio');
        if (serviceSelect) {
            serviceSelect.value = service;
            
            // Disparar evento de cambio para actualizar validaciones
            const event = new Event('change');
            serviceSelect.dispatchEvent(event);
        }
        
        // Mostrar mensaje de confirmación
        this.showSuccessMessage({
            nombre: '',
            telefono: '',
            servicio: serviceName
        });
    }
}

// Inicializar cuando el DOM esté listo
document.addEventListener('DOMContentLoaded', () => {
    const teslaAutomation = new TeslaAutomation();
    teslaAutomation.init();
});
