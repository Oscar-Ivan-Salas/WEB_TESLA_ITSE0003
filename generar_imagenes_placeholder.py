from PIL import Image, ImageDraw, ImageFont
import os

def crear_imagen_placeholder(texto, ancho=400, alto=300):
    # Crear una imagen con fondo gris claro
    img = Image.new('RGB', (ancho, alto), color=(240, 240, 240))
    d = ImageDraw.Draw(img)
    
    # Dibujar un borde gris
    d.rectangle([0, 0, ancho-1, alto-1], outline=(200, 200, 200), width=2)
    
    # Dibujar un icono de cámara en el centro
    d.ellipse([ancho//2-40, alto//2-60, ancho//2+40, alto//2+20], outline=(180, 180, 180), width=2)
    d.ellipse([ancho//2-20, alto//2-40, ancho//2+20, alto//2], fill=(200, 200, 200))
    d.polygon([(ancho//2, alto//2-30), (ancho//2+15, alto//2-15), (ancho//2, alto//2-5), 
                (ancho//2-15, alto//2-15)], fill=(150, 150, 150))
    
    # Agregar texto descriptivo
    try:
        # Intentar cargar una fuente, si no está disponible, usar la predeterminada
        try:
            fuente = ImageFont.truetype("arial.ttf", 16)
        except IOError:
            fuente = ImageFont.load_default()
        
        # Asegurarse de que el texto no sea demasiado ancho
        if len(texto) > 30:
            texto = texto[:27] + "..."
            
        # Calcular el ancho del texto
        ancho_texto = d.textlength(texto, font=fuente)
        
        # Dibujar el texto centrado en la parte inferior
        d.text(((ancho - ancho_texto) / 2, alto - 40), 
               texto, fill=(100, 100, 100), font=fuente)
    except Exception as e:
        print(f"Error al agregar texto: {e}")
    
    return img

def generar_imagenes_servicios():
    # Directorio base para los activos estáticos
    base_dir = os.path.join('app', 'static', 'assets', 'servicios')
    
    # Servicios y sus descripciones
    servicios = {
        'itse': 'Certificado ITSE',
        'pozo_tierra': 'Pozo de Tierra',
        'mantenimiento': 'Mantenimiento Eléctrico',
        'incendios': 'Sistema Contra Incendios',
        'tableros': 'Diseño de Tableros',
        'suministros': 'Suministros Eléctricos'
    }
    
    # Generar imágenes para cada servicio
    for servicio, nombre in servicios.items():
        # Crear directorio si no existe
        servicio_dir = os.path.join(base_dir, servicio)
        os.makedirs(servicio_dir, exist_ok=True)
        
        # Generar 3 imágenes de ejemplo para cada servicio
        for i in range(1, 4):
            # Crear imagen de placeholder
            img = crear_imagen_placeholder(f"{nombre} - Ejemplo {i}")
            
            # Guardar la imagen
            ruta_imagen = os.path.join(servicio_dir, f'foto{i}.jpg')
            img.save(ruta_imagen, 'JPEG', quality=85)
            print(f"Imagen generada: {ruta_imagen}")
            
            # Crear un archivo LEEME en cada directorio
            with open(os.path.join(servicio_dir, 'LEEME.txt'), 'w', encoding='utf-8') as f:
                f.write(f"Por favor, reemplace estas imágenes de ejemplo con imágenes reales del servicio de {nombre}.\n")
                f.write("Los nombres de archivo deben ser: foto1.jpg, foto2.jpg, foto3.jpg")
    
    print("\n¡Proceso completado!")
    print("Se han generado imágenes de marcador de posición para todos los servicios.")
    print("Por favor, reemplácelas con imágenes reales cuando estén disponibles.")

if __name__ == "__main__":
    generar_imagenes_servicios()
