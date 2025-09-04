from PIL import Image, ImageDraw, ImageFont
import os

def crear_logo_temporal(ruta_salida, ancho=300, alto=150):
    # Crear una imagen con fondo azul oscuro
    img = Image.new('RGB', (ancho, alto), color=(0, 51, 102))
    d = ImageDraw.Draw(img)
    
    # Dibujar un borde blanco
    d.rectangle([0, 0, ancho-1, alto-1], outline='white', width=2)
    
    # Intentar cargar una fuente, si no está disponible, usar la predeterminada
    try:
        # Intentar con Arial, si no está disponible, usar la fuente por defecto
        fuente = ImageFont.truetype("arial.ttf", 40)
    except IOError:
        fuente = ImageFont.load_default()
    
    # Texto del logo
    texto = "TESLA"
    texto2 = "ELECTRICIDAD"
    
    # Calcular el ancho y alto del texto
    ancho_texto, alto_texto = d.textsize(texto, font=fuente)
    ancho_texto2, alto_texto2 = d.textsize(texto2, font=fuente)
    
    # Calcular posición para centrar el texto
    x = (ancho - ancho_texto) / 2
    y = (alto - alto_texto - alto_texto2 - 10) / 2
    
    # Dibujar el texto
    d.text((x, y), texto, fill=(255, 255, 255), font=fuente)
    d.text(((ancho - ancho_texto2) / 2, y + alto_texto + 5), texto2, fill=(255, 255, 255), font=fuente)
    
    # Guardar la imagen
    img.save(ruta_salida, 'PNG')
    print(f"Logo temporal generado en: {ruta_salida}")

def verificar_estructura_archivos():
    # Directorio base para los activos estáticos
    base_dir = os.path.join('app', 'static', 'assets')
    
    # Lista de servicios
    servicios = ['itse', 'pozo_tierra', 'mantenimiento', 'incendios', 'tableros', 'suministros']
    
    # Verificar y crear directorios si no existen
    if not os.path.exists(os.path.join(base_dir, 'logo')):
        os.makedirs(os.path.join(base_dir, 'logo'))
    
    for servicio in servicios:
        servicio_dir = os.path.join(base_dir, 'servicios', servicio)
        if not os.path.exists(servicio_dir):
            os.makedirs(servicio_dir)
    
    print("Estructura de directorios verificada.")

if __name__ == "__main__":
    # Verificar la estructura de directorios
    verificar_estructura_archivos()
    
    # Generar el logo temporal
    ruta_logo = os.path.join('app', 'static', 'assets', 'logo', 'tesla-logo.png')
    crear_logo_temporal(ruta_logo)
    
    print("\n¡Proceso completado!")
    print("Por favor, reemplaza el logo temporal con tu logo oficial cuando lo tengas listo.")
