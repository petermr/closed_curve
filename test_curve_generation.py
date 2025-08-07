#!/usr/bin/env python3
import math
import random
from PIL import Image, ImageDraw

def generate_initial_circle(canvas_size, radius, segment_length=3):
    center_x = canvas_size // 2
    center_y = canvas_size // 2
    points = []
    start_point = (center_x + radius, center_y)
    current_point = start_point
    points.append(current_point)
    
    while True:
        dx = current_point[0] - center_x
        dy = current_point[1] - center_y
        angle_step = segment_length / radius
        cos_step = math.cos(angle_step)
        sin_step = math.sin(angle_step)
        new_x = center_x + dx * cos_step - dy * sin_step
        new_y = center_y + dx * sin_step + dy * cos_step
        new_point = (new_x, new_y)
        points.append(new_point)
        distance_to_start = math.hypot(new_x - start_point[0], new_y - start_point[1])
        if distance_to_start <= segment_length and len(points) > 10:
            break
        current_point = new_point
    return points

def generate_nested_curve(outer_curve, length, error, segment_length=3):
    if len(outer_curve) < 3:
        return None
    center_x = sum(x for x, y in outer_curve) / len(outer_curve)
    center_y = sum(y for x, y in outer_curve) / len(outer_curve)
    new_curve = []
    max_dist = 0
    start_outer_point = None
    for ox, oy in outer_curve:
        dist = math.hypot(ox - center_x, oy - center_y)
        if dist > max_dist:
            max_dist = dist
            start_outer_point = (ox, oy)
    if not start_outer_point:
        return None
    ox, oy = start_outer_point
    dx = center_x - ox
    dy = center_y - oy
    dist = math.hypot(dx, dy) or 1.0
    dx = dx / dist * length
    dy = dy / dist * length
    error_x = random.uniform(-error, error)
    error_y = random.uniform(-error, error)
    start_point = (ox + dx + error_x, oy + dy + error_y)
    current_point = start_point
    new_curve.append(current_point)
    
    while True:
        min_dist = float('inf')
        closest_outer_point = None
        for ox, oy in outer_curve:
            dist = math.hypot(current_point[0] - ox, current_point[1] - oy)
            if dist < min_dist:
                min_dist = dist
                closest_outer_point = (ox, oy)
        if not closest_outer_point:
            break
        ox, oy = closest_outer_point
        dx = center_x - ox
        dy = center_y - oy
        dist = math.hypot(dx, dy) or 1.0
        dx = dx / dist * length
        dy = dy / dist * length
        error_x = random.uniform(-error, error)
        error_y = random.uniform(-error, error)
        total_dx = dx + error_x
        total_dy = dy + error_y
        total_dist = math.hypot(total_dx, total_dy) or 1.0
        new_x = current_point[0] + (total_dx / total_dist) * segment_length
        new_y = current_point[1] + (total_dy / total_dist) * segment_length
        new_point = (new_x, new_y)
        new_curve.append(new_point)
        distance_to_start = math.hypot(new_x - start_point[0], new_y - start_point[1])
        if distance_to_start <= segment_length:
            break
        current_point = new_point
    return new_curve

def draw_curves(curves, canvas_size=1000):
    img = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(img)
    colors = ['black', 'red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink']
    for i, curve in enumerate(curves):
        if len(curve) < 2:
            continue
        color = colors[i % len(colors)]
        for j in range(len(curve)):
            p1 = curve[j]
            p2 = curve[(j + 1) % len(curve)]
            draw.line([p1, p2], fill=color, width=2)
    return img

print("Testing curve generation...")
canvas_size = 1000
num_curves = 5
segment_length = 12
error_level = 1.5
curve_distance = 8
curves = []

print(f"Generating initial circle...")
initial_curve = generate_initial_circle(canvas_size, 450, segment_length)
curves.append(initial_curve)
print(f"Generated curve 1 with {len(initial_curve)} points")

for i in range(num_curves - 1):
    print(f"Generating curve {i + 2}...")
    new_curve = generate_nested_curve(curves[-1], curve_distance, error_level, segment_length)
    if new_curve:
        curves.append(new_curve)
        print(f"Generated curve {i + 2} with {len(new_curve)} points")
    else:
        print(f"Failed to generate curve {i + 2}")
        break

print(f"\nTotal curves generated: {len(curves)}")
img = draw_curves(curves, canvas_size)
img.save("test_curves.png")
print("Saved test image to test_curves.png")
