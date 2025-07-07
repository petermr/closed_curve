"""Step 2: Generate and display an offset curve using only the enclosing curve's geometry."""

from PIL import Image, ImageDraw
import math
import random
import os

def sample_circle_points(radius, num_points, canvas_size):
    """Sample points along a circle perimeter."""
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = radius * math.cos(angle) + canvas_size / 2
        y = radius * math.sin(angle) + canvas_size / 2
        points.append((x, y))
    return points

def compute_offset_curve(points, offset):
    """Compute an offset curve by moving each point inward along its local normal."""
    n = len(points)
    offset_points = []
    for i in range(n):
        p_prev = points[i - 1]
        p_curr = points[i]
        p_next = points[(i + 1) % n]
        # Tangent vector (from previous to next)
        dx = p_next[0] - p_prev[0]
        dy = p_next[1] - p_prev[1]
        length = math.hypot(dx, dy) or 1.0
        # Normal vector (perpendicular to tangent, inward for a circle)
        nx = -dy / length
        ny = dx / length
        # Move point inward by offset
        x_off = p_curr[0] + offset * nx
        y_off = p_curr[1] + offset * ny
        
        # Add human-like variation (small random perturbation)
        variation = random.uniform(-1.5, 1.5)  # ±1.5 pixel variation
        x_off += variation
        y_off += variation
        
        offset_points.append((x_off, y_off))
    return offset_points

def draw_curves(canvas_size, enclosing_points, offset_points, thickness=3):
    """Draw both the enclosing and offset curves."""
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    # Draw enclosing curve (black)
    for i in range(len(enclosing_points)):
        p1 = enclosing_points[i]
        p2 = enclosing_points[(i + 1) % len(enclosing_points)]
        draw.line([p1, p2], fill='black', width=thickness)
    # Draw offset curve (red) with line width 2
    for i in range(len(offset_points)):
        p1 = offset_points[i]
        p2 = offset_points[(i + 1) % len(offset_points)]
        draw.line([p1, p2], fill='red', width=2)
    return image

def save_svg(enclosing_points, offset_points, canvas_size, thickness, path):
    """Save both curves as SVG."""
    def points_to_svg_path(points):
        return 'M ' + ' L '.join(f'{x:.2f},{y:.2f}' for x, y in points) + ' Z'
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{canvas_size}" height="{canvas_size}" fill="white"/>
  <path d="{points_to_svg_path(enclosing_points)}" fill="none" stroke="black" stroke-width="{thickness}"/>
  <path d="{points_to_svg_path(offset_points)}" fill="none" stroke="red" stroke-width="2"/>
</svg>'''
    with open(path, 'w', encoding='utf-8') as f:
        f.write(svg_content)

def main():
    canvas_size = 1000
    radius = 450
    offset = 5  # Positive for inward (corrected direction)
    # Calculate points for 2-pixel line increments
    circumference = 2 * math.pi * radius
    num_points = int(circumference / 2)  # 2-pixel increments
    thickness = 3
    enclosing_points = sample_circle_points(radius, num_points, canvas_size)
    offset_points = compute_offset_curve(enclosing_points, offset)
    image = draw_curves(canvas_size, enclosing_points, offset_points, thickness)
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    png_path = os.path.join(output_dir, 'step2_offset_curve.png')
    image.save(png_path, 'PNG')
    print(f"Saved PNG: {png_path}")
    svg_path = os.path.join(output_dir, 'step2_offset_curve.svg')
    save_svg(enclosing_points, offset_points, canvas_size, thickness, svg_path)
    print(f"Saved SVG: {svg_path}")

if __name__ == "__main__":
    main() 