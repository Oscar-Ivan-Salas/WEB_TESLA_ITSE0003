import os
from PIL import Image, ImageDraw, ImageFont
import textwrap

def create_placeholder_image(width, height, text, output_path):
    # Create a new image with a light gray background
    img = Image.new('RGB', (width, height), color='#f0f0f0')
    d = ImageDraw.Draw(img)
    
    # Add a border
    border_color = '#cccccc'
    d.rectangle([(0, 0), (width-1, height-1)], outline=border_color, width=2)
    
    # Add diagonal text
    try:
        font = ImageFont.truetype("arial.ttf", 20)
    except IOError:
        font = ImageFont.load_default()
    
    # Draw the text in the center
    text_color = '#999999'
    text_width, text_height = d.textsize(text, font=font)
    position = ((width - text_width) // 2, (height - text_height) // 2)
    d.text(position, text, fill=text_color, font=font)
    
    # Save the image
    img.save(output_path, 'PNG')

def create_placeholders():
    base_dir = os.path.join('app', 'static', 'assets')
    
    # Create logo placeholder
    logo_path = os.path.join(base_dir, 'logo', 'tesla-logo.png')
    create_placeholder_image(200, 100, 'Tesla Logo', logo_path)
    
    # Create service placeholders
    services = ['itse', 'pozo_tierra', 'mantenimiento', 'incendios', 'tableros', 'suministros']
    
    for service in services:
        service_dir = os.path.join(base_dir, 'servicios', service)
        os.makedirs(service_dir, exist_ok=True)
        
        # Create 3 placeholder images for each service
        for i in range(1, 4):
            filename = f'foto{i}.jpg'
            output_path = os.path.join(service_dir, filename)
            create_placeholder_image(400, 300, f'{service}\n{filename}', output_path)
    
    print("Placeholder images created successfully!")

if __name__ == "__main__":
    create_placeholders()
