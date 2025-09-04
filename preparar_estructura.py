import os

def crear_estructura():
    # Directorio base para los activos estáticos
    base_dir = os.path.join('app', 'static', 'assets')
    
    # Lista de servicios
    servicios = ['itse', 'pozo_tierra', 'mantenimiento', 'incendios', 'tableros', 'suministros']
    
    # Crear directorios necesarios
    directorios = [
        os.path.join(base_dir, 'css'),
        os.path.join(base_dir, 'js'),
        os.path.join(base_dir, 'logo')
    ]
    
    # Agregar directorios de servicios
    for servicio in servicios:
        directorios.append(os.path.join(base_dir, 'servicios', servicio))
    
    # Crear directorios si no existen
    for directorio in directorios:
        os.makedirs(directorio, exist_ok=True)
        print(f"Directorio creado: {directorio}")
    
    # Crear archivos README en cada directorio de servicio
    for servicio in servicios:
        ruta_readme = os.path.join(base_dir, 'servicios', servicio, 'LEEME.txt')
        with open(ruta_readme, 'w', encoding='utf-8') as f:
            f.write(f"Por favor, coloque aquí las imágenes para el servicio de {servicio.replace('_', ' ').title()}.\n")
            f.write("Nombres de archivo sugeridos: foto1.jpg, foto2.jpg, foto3.jpg")
        print(f"Archivo LEEME creado en: {ruta_readme}")
    
    print("\n¡Estructura de carpetas creada con éxito!")
    print("Ahora puede agregar sus imágenes en las carpetas correspondientes.")
    print("Ruta de los servicios: app/static/assets/servicios/")

if __name__ == "__main__":
    crear_estructura()
