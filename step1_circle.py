"""Step 1: Draw a circle with antialiasing and save to PNG and SVG."""

from PIL import Image, ImageDraw
import os


def draw_circle_step1():
    """Draw a circle of radius 450 with line thickness 3 using antialiasing.
    
    Creates a 1000x1000 white canvas and draws a circle with antialiasing.
    Saves the result to both PNG and SVG formats.
    """
    # Canvas configuration
    canvas_size = 1000
    radius = 450
    thickness = 3
    center = canvas_size // 2
    
    # Create white canvas
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Calculate bounding box for circle
    bbox = (center - radius, center - radius, center + radius, center + radius)
    
    # Draw circle with antialiasing (PIL handles this automatically)
    draw.ellipse(bbox, outline='black', width=thickness)
    
    # Ensure output directory exists
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save as PNG
    png_path = os.path.join(output_dir, 'step1_circle.png')
    image.save(png_path, 'PNG')
    print(f"Saved PNG: {png_path}")
    
    # Save as SVG
    svg_path = os.path.join(output_dir, 'step1_circle.svg')
    save_as_svg(image, svg_path, canvas_size, center, radius, thickness)
    print(f"Saved SVG: {svg_path}")


def save_as_svg(image, path, canvas_size, center, radius, thickness):
    """Save the circle as an SVG file.
    
    Args:
        image: PIL Image object (for reference)
        path: Output file path
        canvas_size: Size of the canvas
        center: Center coordinate of the circle
        radius: Radius of the circle
        thickness: Line thickness
    """
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{canvas_size}" height="{canvas_size}" fill="white"/>
  <circle cx="{center}" cy="{center}" r="{radius}" 
          fill="none" stroke="black" stroke-width="{thickness}"/>
</svg>'''
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg_content)


if __name__ == "__main__":
    draw_circle_step1() 