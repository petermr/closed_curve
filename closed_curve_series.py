"""
Closed Curve Series Generator

This script generates a comprehensive series of closed curves using different algorithms:
1. Bézier curves with varying control points
2. Nested polygons with error transmission
3. Cellular deposition patterns
4. Parametric curves (circles, ellipses, cardioids, etc.)
5. Fractal-like curves

Author: AI Assistant
Date: [Current Date]
"""

import matplotlib.pyplot as plt
import numpy as np
import math
import random
from PIL import Image, ImageDraw
import os

# Configuration
CANVAS_SIZE = 800
OUTPUT_DIR = "curve_series"
BACKGROUND_COLOR = (255, 255, 255)
CURVE_COLORS = [
    (0, 0, 0),      # Black
    (255, 0, 0),    # Red
    (0, 0, 255),    # Blue
    (0, 128, 0),    # Green
    (128, 0, 128),  # Purple
    (255, 165, 0),  # Orange
]

def ensure_output_dir():
    """Ensure output directory exists"""
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

def draw_bezier_curve(draw, points, color, width=2):
    """Draw a Bézier curve through given points"""
    if len(points) < 3:
        return
    
    # Create control points for smooth curve
    control_points = []
    for i in range(len(points)):
        if i == 0:
            # First point: control point is between first and second
            cp = ((points[0][0] + points[1][0]) // 2, 
                  (points[0][1] + points[1][1]) // 2)
        elif i == len(points) - 1:
            # Last point: control point is between last and second-to-last
            cp = ((points[-1][0] + points[-2][0]) // 2,
                  (points[-1][1] + points[-2][1]) // 2)
        else:
            # Middle points: average of adjacent points
            cp = ((points[i-1][0] + points[i+1][0]) // 2,
                  (points[i-1][1] + points[i+1][1]) // 2)
        control_points.append(cp)
    
    # Draw curve segments
    for i in range(len(points) - 1):
        p1 = points[i]
        p2 = points[i + 1]
        cp1 = control_points[i]
        cp2 = control_points[i + 1]
        
        # Draw cubic Bézier segment
        draw.line([p1, cp1, cp2, p2], fill=color, width=width)

def generate_parametric_curve(center, radius, curve_type="circle", params=None):
    """Generate parametric curve points"""
    t = np.linspace(0, 2*np.pi, 100)
    cx, cy = center
    
    if curve_type == "circle":
        x = cx + radius * np.cos(t)
        y = cy + radius * np.sin(t)
    elif curve_type == "ellipse":
        a, b = params.get('a', radius), params.get('b', radius * 0.7)
        x = cx + a * np.cos(t)
        y = cy + b * np.sin(t)
    elif curve_type == "cardioid":
        x = cx + radius * (2 * np.cos(t) - np.cos(2*t))
        y = cy + radius * (2 * np.sin(t) - np.sin(2*t))
    elif curve_type == "limacon":
        a, b = params.get('a', radius), params.get('b', radius * 0.5)
        x = cx + (a + b * np.cos(t)) * np.cos(t)
        y = cy + (a + b * np.cos(t)) * np.sin(t)
    elif curve_type == "rose":
        n = params.get('n', 3)
        x = cx + radius * np.cos(n * t) * np.cos(t)
        y = cy + radius * np.sin(n * t) * np.sin(t)
    else:
        # Default to circle
        x = cx + radius * np.cos(t)
        y = cy + radius * np.sin(t)
    
    return list(zip(x, y))

def generate_fractal_curve(center, radius, depth=3, angle_offset=0):
    """Generate fractal-like curve using recursive subdivision"""
    if depth == 0:
        return [center]
    
    points = []
    cx, cy = center
    
    # Generate base polygon
    n_sides = 6
    for i in range(n_sides):
        angle = 2 * np.pi * i / n_sides + angle_offset
        x = cx + radius * np.cos(angle)
        y = cy + radius * np.sin(angle)
        points.append((x, y))
    
    # Recursively add detail
    if depth > 1:
        new_points = []
        for i in range(len(points)):
            p1 = points[i]
            p2 = points[(i + 1) % len(points)]
            
            # Add midpoint with perturbation
            mx = (p1[0] + p2[0]) / 2
            my = (p1[1] + p2[1]) / 2
            
            # Perturb inward
            dx = mx - cx
            dy = my - cy
            dist = math.sqrt(dx*dx + dy*dy)
            if dist > 0:
                perturbation = radius * 0.1 * (depth - 1)
                mx += (dx / dist) * perturbation
                my += (dy / dist) * perturbation
            
            new_points.extend([p1, (mx, my)])
        points = new_points
    
    return points

def create_curve_image(curve_type, params, filename):
    """Create and save a curve image"""
    img = Image.new("RGB", (CANVAS_SIZE, CANVAS_SIZE), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(img)
    
    center = (CANVAS_SIZE // 2, CANVAS_SIZE // 2)
    radius = 200
    
    if curve_type == "bezier":
        # Generate random control points for Bézier curve
        points = []
        for i in range(8):
            angle = 2 * np.pi * i / 8
            r = radius * (0.5 + 0.5 * random.random())
            x = center[0] + r * math.cos(angle)
            y = center[1] + r * math.sin(angle)
            points.append((int(x), int(y)))
        
        draw_bezier_curve(draw, points, CURVE_COLORS[0], width=3)
        
    elif curve_type == "parametric":
        curve_subtype = params.get('subtype', 'circle')
        curve_params = params.get('params', {})
        points = generate_parametric_curve(center, radius, curve_subtype, curve_params)
        
        # Draw the curve
        for i in range(len(points) - 1):
            p1 = (int(points[i][0]), int(points[i][1]))
            p2 = (int(points[i+1][0]), int(points[i+1][1]))
            draw.line([p1, p2], fill=CURVE_COLORS[1], width=2)
        
    elif curve_type == "fractal":
        depth = params.get('depth', 3)
        angle_offset = params.get('angle_offset', 0)
        points = generate_fractal_curve(center, radius, depth, angle_offset)
        
        # Draw the fractal curve
        for i in range(len(points) - 1):
            p1 = (int(points[i][0]), int(points[i][1]))
            p2 = (int(points[i+1][0]), int(points[i+1][1]))
            draw.line([p1, p2], fill=CURVE_COLORS[2], width=1)
    
    # Save the image
    img.save(os.path.join(OUTPUT_DIR, filename))
    print(f"Generated: {filename}")

def generate_curve_series():
    """Generate the complete series of closed curves"""
    ensure_output_dir()
    
    # 1. Bézier Curves Series
    print("Generating Bézier curves...")
    for i in range(5):
        create_curve_image("bezier", {}, f"bezier_curve_{i+1}.png")
    
    # 2. Parametric Curves Series
    print("Generating parametric curves...")
    parametric_types = [
        ("circle", {}),
        ("ellipse", {"params": {"a": 200, "b": 150}}),
        ("cardioid", {}),
        ("limacon", {"params": {"a": 150, "b": 100}}),
        ("rose", {"params": {"n": 3}}),
        ("rose", {"params": {"n": 4}}),
        ("rose", {"params": {"n": 5}}),
    ]
    
    for i, (subtype, params) in enumerate(parametric_types):
        create_curve_image("parametric", {"subtype": subtype, "params": params}, 
                          f"parametric_{subtype}_{i+1}.png")
    
    # 3. Fractal Curves Series
    print("Generating fractal curves...")
    for depth in [2, 3, 4, 5]:
        for angle_offset in [0, np.pi/6, np.pi/4]:
            params = {"depth": depth, "angle_offset": angle_offset}
            create_curve_image("fractal", params, 
                              f"fractal_depth_{depth}_angle_{int(angle_offset*180/np.pi)}.png")

if __name__ == "__main__":
    print("Starting Closed Curve Series Generation...")
    generate_curve_series()
    print(f"All curves generated in '{OUTPUT_DIR}' directory!") 