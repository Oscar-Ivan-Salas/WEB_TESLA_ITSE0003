import os
import sqlite3
from pathlib import Path

def setup_database():
    # Create data directory if it doesn't exist
    data_dir = Path("e:/WEB_TESLA_ITSE0003/tesla_complete/backend/data")
    data_dir.mkdir(parents=True, exist_ok=True)
    
    db_path = data_dir / "tesla.db"
    
    # Remove existing database if it exists
    if db_path.exists():
        try:
            os.remove(db_path)
            print("ℹ️  Existing database removed.")
        except Exception as e:
            print(f"⚠️  Could not remove existing database: {e}")
    
    # SQL statements to create tables
    sql_commands = """
    -- Create leads table
    CREATE TABLE IF NOT EXISTS leads (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        ruc TEXT UNIQUE,
        telefono TEXT NOT NULL,
        email TEXT,
        tipo_negocio TEXT,
        direccion TEXT,
        metraje REAL,
        tiene_licencia BOOLEAN DEFAULT FALSE,
        estado TEXT DEFAULT 'nuevo',
        servicio_interes TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create citas table
    CREATE TABLE IF NOT EXISTS citas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER REFERENCES leads(id),
        fecha_cita DATE,
        hora_cita TIME,
        especialista TEXT,
        tipo_visita TEXT,
        estado TEXT DEFAULT 'programada',
        notas TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create conversaciones table
    CREATE TABLE IF NOT EXISTS conversaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER REFERENCES leads(id),
        mensaje TEXT NOT NULL,
        respuesta TEXT NOT NULL,
        contexto TEXT,
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create servicios table
    CREATE TABLE IF NOT EXISTS servicios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        categoria TEXT,
        precio_min REAL,
        precio_max REAL,
        descripcion TEXT,
        tiempo_entrega TEXT,
        foto1_url TEXT,
        foto2_url TEXT,
        foto3_url TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Create cotizaciones table
    CREATE TABLE IF NOT EXISTS cotizaciones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        lead_id INTEGER REFERENCES leads(id),
        servicio_id INTEGER REFERENCES servicios(id),
        monto_total REAL NOT NULL,
        detalles TEXT,
        estado TEXT DEFAULT 'pendiente',
        valido_hasta DATE,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );

    -- Insert services
    INSERT INTO servicios (nombre, categoria, precio_min, precio_max, descripcion, tiempo_entrega, foto1_url, foto2_url, foto3_url) VALUES
    ('Certificado ITSE', 'itse', 500.0, 2500.0, 'Gestión completa para la obtención del Certificado de Inspección Técnica de Seguridad en Edificaciones', '5-10 días hábiles', '/static/assets/servicios/itse/foto1.jpg', '/static/assets/servicios/itse/foto2.jpg', '/static/assets/servicios/itse/foto3.jpg'),
    ('Pozo a Tierra', 'pozo_tierra', 1200.0, 5000.0, 'Instalación de sistema de puesta a tierra para protección de equipos y personas', '1-2 días', '/static/assets/servicios/pozo_tierra/foto1.jpg', '/static/assets/servicios/pozo_tierra/foto2.jpg', '/static/assets/servicios/pozo_tierra/foto3.jpg'),
    ('Mantenimiento Eléctrico', 'mantenimiento', 300.0, 1500.0, 'Servicio de mantenimiento preventivo y correctivo para instalaciones eléctricas', '2-4 horas', '/static/assets/servicios/mantenimiento/foto1.jpg', '/static/assets/servicios/mantenimiento/foto2.jpg', '/static/assets/servicios/mantenimiento/foto3.jpg'),
    ('Sistema Contra Incendios', 'incendios', 2000.0, 10000.0, 'Diseño e instalación de sistemas de detección y extinción de incendios', '3-7 días', '/static/assets/servicios/incendios/foto1.jpg', '/static/assets/servicios/incendios/foto2.jpg', '/static/assets/servicios/incendios/foto3.jpg'),
    ('Diseño de Tableros', 'tableros', 1500.0, 8000.0, 'Diseño y fabricación de tableros eléctricos personalizados', '5-15 días', '/static/assets/servicios/tableros/foto1.jpg', '/static/assets/servicios/tableros/foto2.jpg', '/static/assets/servicios/tableros/foto3.jpg'),
    ('Suministros Eléctricos', 'suministros', 0.0, 0.0, 'Venta de materiales y equipos eléctricos de las mejores marcas', 'Inmediato', '/static/assets/servicios/suministros/foto1.jpg', '/static/assets/servicios/suministros/foto2.jpg', '/static/assets/servicios/suministros/foto3.jpg');

    -- Create indexes
    CREATE INDEX IF NOT EXISTS idx_leads_estado ON leads(estado);
    CREATE INDEX IF NOT EXISTS idx_citas_lead_id ON citas(lead_id);
    CREATE INDEX IF NOT EXISTS idx_citas_fecha ON citas(fecha_cita, hora_cita);
    CREATE INDEX IF NOT EXISTS idx_conversaciones_lead_id ON conversaciones(lead_id);
    CREATE INDEX IF NOT EXISTS idx_servicios_categoria ON servicios(categoria);
    """
    
    try:
        # Connect to SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Execute SQL commands
        cursor.executescript(sql_commands)
        conn.commit()
        
        # Verify
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        cursor.execute("SELECT COUNT(*) FROM servicios")
        service_count = cursor.fetchone()[0]
        
        print("✅ Database setup completed successfully!")
        print(f"📊 Tables created: {', '.join(tables)}")
        print(f"🛠️  {service_count} services inserted")
        
        return True
        
    except sqlite3.Error as e:
        print(f"❌ Error setting up database: {e}")
        return False
    finally:
        if 'conn' in locals():
            conn.close()

if __name__ == "__main__":
    setup_database()
