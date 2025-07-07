"""Step 2: Draw a human-like parallel curve inside the circle."""

from PIL import Image, ImageDraw
import math
import random
import os


def draw_parallel_curve_step2():
    """Draw a human-like parallel curve inside the circle with 5-pixel separation.
    
    Creates a curve that tries to be parallel to the circle but with human-like
    imperfections and variations.
    """
    # Canvas configuration
    canvas_size = 1000
    radius = 450
    thickness = 3
    separation = 5
    center = canvas_size // 2
    
    # Create white canvas
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw the original circle
    bbox = (center - radius, center - radius, center + radius, center + radius)
    draw.ellipse(bbox, outline='black', width=thickness)
    
    # Generate parallel curve points
    curve_points = generate_parallel_curve(center, radius, separation)
    
    # Draw the parallel curve
    draw_curve_sequential(draw, curve_points, 'red', thickness=2)
    
    # Ensure output directory exists
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Save as PNG
    png_path = os.path.join(output_dir, 'step2_parallel_curve.png')
    image.save(png_path, 'PNG')
    print(f"Saved PNG: {png_path}")
    
    # Save as SVG
    svg_path = os.path.join(output_dir, 'step2_parallel_curve.svg')
    save_as_svg_with_curves(image, svg_path, canvas_size, center, radius, 
                           thickness, curve_points)
    print(f"Saved SVG: {svg_path}")


def generate_parallel_curve(center, radius, separation):
    """Generate points for a human-like parallel curve.
    
    Args:
        center: Center coordinate (single value for x and y)
        radius: Radius of the original circle
        separation: Distance inward from the circle
        
    Returns:
        List of (x, y) points for the parallel curve
    """
    points = []
    cx = cy = center  # Center is the same for x and y
    inner_radius = radius - separation
    
    # Number of points to sample (more points = smoother curve)
    num_points = 200
    
    # Hand steadiness parameters
    max_variation = 2.0  # Maximum pixel variation
    variation_frequency = 0.3  # How often variations occur
    
    for i in range(num_points):
        # Calculate angle around the circle
        angle = 2 * math.pi * i / num_points
        
        # Base point on inner circle
        base_x = cx + inner_radius * math.cos(angle)
        base_y = cy + inner_radius * math.sin(angle)
        
        # Add human-like variation
        if random.random() < variation_frequency:
            # Add small random perturbation
            variation_x = random.uniform(-max_variation, max_variation)
            variation_y = random.uniform(-max_variation, max_variation)
            base_x += variation_x
            base_y += variation_y
        
        points.append((int(base_x), int(base_y)))
    
    # Close the curve by adding the first point at the end
    points.append(points[0])
    
    return points


def draw_curve_sequential(draw, points, color, thickness=2):
    """Draw curve by connecting points sequentially.
    
    Args:
        draw: PIL ImageDraw object
        points: List of (x, y) points
        color: Color of the curve
        thickness: Line thickness
    """
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        draw.line([p1, p2], fill=color, width=thickness)


def save_as_svg_with_curves(image, path, canvas_size, center, radius, 
                           thickness, curve_points):
    """Save the image with both circle and parallel curve as SVG.
    
    Args:
        image: PIL Image object (for reference)
        path: Output file path
        canvas_size: Size of the canvas
        center: Center coordinate
        radius: Circle radius
        thickness: Line thickness
        curve_points: Points for the parallel curve
    """
    cx = cy = center
    
    # Create SVG path for the parallel curve
    curve_path = "M"
    for x, y in curve_points:
        curve_path += f" {x},{y}"
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{canvas_size}" height="{canvas_size}" fill="white"/>
  <circle cx="{cx}" cy="{cy}" r="{radius}" 
          fill="none" stroke="black" stroke-width="{thickness}"/>
  <path d="{curve_path}" fill="none" stroke="red" stroke-width="2"/>
</svg>'''
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg_content)


if __name__ == "__main__":
    draw_parallel_curve_step2() 