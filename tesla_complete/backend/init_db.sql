-- Drop existing tables if they exist
DROP TABLE IF EXISTS conversaciones;
DROP TABLE IF EXISTS citas;
DROP TABLE IF EXISTS cotizaciones;
DROP TABLE IF EXISTS servicios;
DROP TABLE IF EXISTS leads;

-- Create leads table
CREATE TABLE leads (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    ruc TEXT UNIQUE,
    telefono TEXT NOT NULL,
    email TEXT,
    tipo_negocio TEXT, -- restaurante, comercio, industria, vivienda
    direccion TEXT,
    metraje REAL,
    tiene_licencia BOOLEAN DEFAULT FALSE,
    estado TEXT DEFAULT 'nuevo', -- nuevo, contactado, cotizado, visitado, cerrado
    servicio_interes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create citas table
CREATE TABLE citas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER REFERENCES leads(id),
    fecha_cita DATE,
    hora_cita TIME,
    especialista TEXT,
    tipo_visita TEXT, -- tecnica, comercial, seguimiento
    estado TEXT DEFAULT 'programada', -- programada, realizada, cancelada
    notas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create conversaciones table
CREATE TABLE conversaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER REFERENCES leads(id),
    mensaje TEXT NOT NULL,
    respuesta TEXT NOT NULL,
    contexto TEXT, -- servicio consultado
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create servicios table
CREATE TABLE servicios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    categoria TEXT, -- itse, pozo_tierra, mantenimiento, etc.
    precio_min REAL,
    precio_max REAL,
    descripcion TEXT,
    tiempo_entrega TEXT,
    foto1_url TEXT, -- ruta a foto local
    foto2_url TEXT,
    foto3_url TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create cotizaciones table
CREATE TABLE cotizaciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    lead_id INTEGER REFERENCES leads(id),
    servicio_id INTEGER REFERENCES servicios(id),
    monto_total REAL NOT NULL,
    detalles TEXT,
    estado TEXT DEFAULT 'pendiente', -- pendiente, aprobada, rechazada
    valido_hasta DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (lead_id) REFERENCES leads(id),
    FOREIGN KEY (servicio_id) REFERENCES servicios(id)
);

-- Insert initial services data
INSERT INTO servicios (nombre, categoria, precio_min, precio_max, descripcion, tiempo_entrega, foto1_url, foto2_url, foto3_url) VALUES
('Certificado ITSE', 'itse', 500.0, 2500.0, 'Gestión completa para la obtención del Certificado de Inspección Técnica de Seguridad en Edificaciones', '5-10 días hábiles', '/static/assets/servicios/itse/foto1.jpg', '/static/assets/servicios/itse/foto2.jpg', '/static/assets/servicios/itse/foto3.jpg'),

('Pozo a Tierra', 'pozo_tierra', 1200.0, 5000.0, 'Instalación de sistema de puesta a tierra para protección de equipos y personas', '1-2 días', '/static/assets/servicios/pozo_tierra/foto1.jpg', '/static/assets/servicios/pozo_tierra/foto2.jpg', '/static/assets/servicios/pozo_tierra/foto3.jpg'),

('Mantenimiento Eléctrico', 'mantenimiento', 300.0, 1500.0, 'Servicio de mantenimiento preventivo y correctivo para instalaciones eléctricas', '2-4 horas', '/static/assets/servicios/mantenimiento/foto1.jpg', '/static/assets/servicios/mantenimiento/foto2.jpg', '/static/assets/servicios/mantenimiento/foto3.jpg'),

('Sistema Contra Incendios', 'incendios', 2000.0, 10000.0, 'Diseño e instalación de sistemas de detección y extinción de incendios', '3-7 días', '/static/assets/servicios/incendios/foto1.jpg', '/static/assets/servicios/incendios/foto2.jpg', '/static/assets/servicios/incendios/foto3.jpg'),

('Diseño de Tableros', 'tableros', 1500.0, 8000.0, 'Diseño y fabricación de tableros eléctricos personalizados', '5-15 días', '/static/assets/servicios/tableros/foto1.jpg', '/static/assets/servicios/tableros/foto2.jpg', '/static/assets/servicios/tableros/foto3.jpg'),

('Suministros Eléctricos', 'suministros', 0.0, 0.0, 'Venta de materiales y equipos eléctricos de las mejores marcas', 'Inmediato', '/static/assets/servicios/suministros/foto1.jpg', '/static/assets/servicios/suministros/foto2.jpg', '/static/assets/servicios/suministros/foto3.jpg');

-- Create indexes for better performance
CREATE INDEX idx_leads_estado ON leads(estado);
CREATE INDEX idx_citas_lead_id ON citas(lead_id);
CREATE INDEX idx_citas_fecha ON citas(fecha_cita, hora_cita);
CREATE INDEX idx_conversaciones_lead_id ON conversaciones(lead_id);
CREATE INDEX idx_servicios_categoria ON servicios(categoria);
