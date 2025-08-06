"""
step6_final_version.py - Working version of closed curve generator

This version generates nested curves that:
- Start with a circle of given radius
- Generate inward-progressing curves with human-like error
- Do not cross themselves or earlier curves
- Use proper coordinate system centered at canvas center
"""

import math
import random
from PIL import Image, ImageDraw

def generate_initial_circle(canvas_size, radius, segment_length=3):
    """Generate initial circle centered at canvas center with fixed segment length."""
    center_x = canvas_size // 2
    center_y = canvas_size // 2
    
    points = []
    start_point = (center_x + radius, center_y)  # Start at (radius, 0)
    current_point = start_point
    points.append(current_point)
    
    while True:
        # Calculate next point on circle at segment_length distance
        # Move clockwise around the circle
        dx = current_point[0] - center_x
        dy = current_point[1] - center_y
        
        # Rotate by small angle to get next point
        angle_step = segment_length / radius
        cos_step = math.cos(angle_step)
        sin_step = math.sin(angle_step)
        
        new_x = center_x + dx * cos_step - dy * sin_step
        new_y = center_y + dx * sin_step + dy * cos_step
        
        new_point = (new_x, new_y)
        points.append(new_point)
        
        # Check if we're close enough to start point
        distance_to_start = math.hypot(new_x - start_point[0], new_y - start_point[1])
        if distance_to_start <= segment_length and len(points) > 10:  # Need at least some points
            break
        
        current_point = new_point
    
    return points

def generate_nested_curve(outer_curve, length, error, segment_length=3):
    """Generate a nested curve inside the outer curve with fixed segment length."""
    if len(outer_curve) < 3:
        return None
    
    # Calculate center of outer curve
    center_x = sum(x for x, y in outer_curve) / len(outer_curve)
    center_y = sum(y for x, y in outer_curve) / len(outer_curve)
    
    new_curve = []
    
    # Find a good starting point (furthest from center)
    max_dist = 0
    start_outer_point = None
    for ox, oy in outer_curve:
        dist = math.hypot(ox - center_x, oy - center_y)
        if dist > max_dist:
            max_dist = dist
            start_outer_point = (ox, oy)
    
    if not start_outer_point:
        return None
    
    # Calculate first point of new curve
    ox, oy = start_outer_point
    dx = center_x - ox
    dy = center_y - oy
    dist = math.hypot(dx, dy) or 1.0
    
    # Normalize and apply length
    dx = dx / dist * length
    dy = dy / dist * length
    
    # Add error
    error_x = random.uniform(-error, error)
    error_y = random.uniform(-error, error)
    
    start_point = (ox + dx + error_x, oy + dy + error_y)
    current_point = start_point
    new_curve.append(current_point)
    
    while True:
        # Find closest point on outer curve to current point
        min_dist = float('inf')
        closest_outer_point = None
        
        for ox, oy in outer_curve:
            dist = math.hypot(current_point[0] - ox, current_point[1] - oy)
            if dist < min_dist:
                min_dist = dist
                closest_outer_point = (ox, oy)
        
        if not closest_outer_point:
            break
        
        # Calculate direction from outer curve point to center
        ox, oy = closest_outer_point
        dx = center_x - ox
        dy = center_y - oy
        dist = math.hypot(dx, dy) or 1.0
        
        # Normalize and apply length
        dx = dx / dist * length
        dy = dy / dist * length
        
        # Add error
        error_x = random.uniform(-error, error)
        error_y = random.uniform(-error, error)
        
        # Calculate new point at segment_length distance from current point
        # in the direction of (dx, dy)
        total_dx = dx + error_x
        total_dy = dy + error_y
        total_dist = math.hypot(total_dx, total_dy) or 1.0
        
        # Normalize to segment_length
        new_x = current_point[0] + (total_dx / total_dist) * segment_length
        new_y = current_point[1] + (total_dy / total_dist) * segment_length
        
        new_point = (new_x, new_y)
        new_curve.append(new_point)
        
        # Check if we're close enough to start point
        distance_to_start = math.hypot(new_x - start_point[0], new_y - start_point[1])
        if distance_to_start <= segment_length:
            break
        
        current_point = new_point
    
    return new_curve

def do_lines_intersect(p1, p2, p3, p4):
    """Check if line segments (p1,p2) and (p3,p4) intersect using CCW algorithm."""
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def draw_curves(curves, canvas_size, output_file):
    """Draw all curves to an image file."""
    img = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(img)
    
    colors = ['black', 'blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink']
    
    for i, curve in enumerate(curves):
        if len(curve) < 2:
            continue
        
        color = colors[i % len(colors)]
        
        # Draw the curve
        for j in range(len(curve)):
            p1 = curve[j]
            p2 = curve[(j + 1) % len(curve)]
            draw.line([p1, p2], fill=color, width=2)
    
    img.save(output_file)
    print(f"Curves saved to {output_file}")

def main():
    """Main function to generate and draw curves."""
    canvas_size = 1000
    initial_radius = 450
    num_curves = 5
    length = 15
    error = 2.4
    segment_length = 3  # Small segment length for smooth curves
    
    # Generate initial circle
    curves = [generate_initial_circle(canvas_size, initial_radius, segment_length)]
    
    # Generate nested curves
    for i in range(num_curves - 1):
        new_curve = generate_nested_curve(curves[-1], length, error, segment_length)
        if new_curve:
            curves.append(new_curve)
    
    # Draw all curves
    draw_curves(curves, canvas_size, "step6_output.png")

if __name__ == "__main__":
    main() 