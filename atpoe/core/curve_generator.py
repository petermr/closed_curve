"""
atpoe/core/curve_generator.py - Working curve generation functions

This module provides the core functions for generating nested curves:
- generate_initial_circle: Creates the starting circle
- generate_nested_curve: Creates inward-progressing curves with error
- do_lines_intersect: Collision detection using CCW algorithm
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
    
    # Safety limit to prevent infinite loops
    max_iterations = int(2 * math.pi * radius / segment_length) + 100
    iteration_count = 0
    
    while iteration_count < max_iterations:
        iteration_count += 1
        
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
    
    if iteration_count >= max_iterations:
        print(f"Warning: Circle generation reached maximum iterations ({max_iterations})")
    
    return points

def generate_nested_curve(outer_curve, length, error, segment_length=3):
    """Generate a nested curve inside the outer curve with fixed segment length."""
    if len(outer_curve) < 3:
        return None
    
    # Calculate center of outer curve
    center_x = sum(x for x, y in outer_curve) / len(outer_curve)
    center_y = sum(y for x, y in outer_curve) / len(outer_curve)
    
    new_curve = []
    
    # Start at first point of previous curve
    outer_point = outer_curve[0]
    
    # Calculate first point inside
    dx = center_x - outer_point[0]
    dy = center_y - outer_point[1]
    d = math.hypot(dx, dy) or 1.0
    
    # Add small random error
    error_x = random.uniform(-error, error)
    error_y = random.uniform(-error, error)
    
    # Place first point at length distance inside
    first_point = (
        outer_point[0] + (dx / d) * length + error_x,
        outer_point[1] + (dy / d) * length + error_y
    )
    
    new_curve.append(first_point)
    current_point = first_point
    
    # Go round the previous curve systematically
    for i in range(1, len(outer_curve)):
        outer_point = outer_curve[i]
        
        # Calculate target point inside this outer point
        dx = center_x - outer_point[0]
        dy = center_y - outer_point[1]
        d = math.hypot(dx, dy) or 1.0
        
        # Add small random error
        error_x = random.uniform(-error, error)
        error_y = random.uniform(-error, error)
        
        target_point = (
            outer_point[0] + (dx / d) * length + error_x,
            outer_point[1] + (dy / d) * length + error_y
        )
        
        # Move toward target in steps of segment_length
        while math.hypot(current_point[0] - target_point[0], current_point[1] - target_point[1]) > segment_length:
            # Calculate direction to target
            dx_to_target = target_point[0] - current_point[0]
            dy_to_target = target_point[1] - current_point[1]
            d_to_target = math.hypot(dx_to_target, dy_to_target) or 1.0
            
            # Add new point at segment_length distance
            new_point = (
                current_point[0] + (dx_to_target / d_to_target) * segment_length,
                current_point[1] + (dy_to_target / d_to_target) * segment_length
            )
            
            new_curve.append(new_point)
            current_point = new_point
    
    # Close the curve: keep adding points until close to start
    while math.hypot(current_point[0] - new_curve[0][0], current_point[1] - new_curve[0][1]) > segment_length:
        # Calculate direction to start
        dx_to_start = new_curve[0][0] - current_point[0]
        dy_to_start = new_curve[0][1] - current_point[1]
        d_to_start = math.hypot(dx_to_start, dy_to_start) or 1.0
        
        # Add new point at segment_length distance
        new_point = (
            current_point[0] + (dx_to_start / d_to_start) * segment_length,
            current_point[1] + (dy_to_start / d_to_start) * segment_length
        )
        
        new_curve.append(new_point)
        current_point = new_point
    
    # Final closure
    new_curve.append(new_curve[0])
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
