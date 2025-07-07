"""Step 3: Generate multiple nested curves iteratively."""

import streamlit as st
from PIL import Image, ImageDraw
import math
import random
import os
import io


def sample_circle_points(radius, num_points, canvas_size):
    """Sample points along a circle perimeter with constant arc length."""
    points = []
    circumference = 2 * math.pi * radius
    arc_length = circumference / num_points
    
    for i in range(num_points):
        angle = arc_length * i / radius  # Constant arc length
        x = radius * math.cos(angle) + canvas_size / 2
        y = radius * math.sin(angle) + canvas_size / 2
        points.append((x, y))
    return points


def do_lines_intersect(p1, p2, p3, p4):
    """Check if line segments (p1,p2) and (p3,p4) intersect."""
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)

def compute_offset_curve(points, offset, variation_amount, previous_curve=None):
    """Compute an offset curve with collision detection and correction."""
    n = len(points)
    offset_points = []
    min_separation = offset * 0.5  # Minimum separation is half the offset distance
    
    for i in range(n):
        p_prev = points[i - 1]
        p_curr = points[i]
        p_next = points[(i + 1) % n]
        # Tangent vector (from previous to next)
        dx = p_next[0] - p_prev[0]
        dy = p_next[1] - p_prev[1]
        length = math.hypot(dx, dy) or 1.0
        # Normal vector (perpendicular to tangent, inward)
        nx = -dy / length
        ny = dx / length
        # Move point inward by offset
        x_off = p_curr[0] + offset * nx
        y_off = p_curr[1] + offset * ny
        
        # Add human-like variation (adjustable amount)
        if variation_amount > 0:
            variation_x = random.uniform(-variation_amount, variation_amount)
            variation_y = random.uniform(-variation_amount, variation_amount)
            x_off += variation_x
            y_off += variation_y
        
        # Check for collision with previous curve
        if previous_curve is not None:
            # Check point-to-point distance
            min_distance = float('inf')
            for prev_point in previous_curve:
                dist = math.hypot(x_off - prev_point[0], y_off - prev_point[1])
                min_distance = min(min_distance, dist)
            
            # Check line segment intersections
            has_intersection = False
            if len(offset_points) > 0:
                new_segment = (offset_points[-1], (x_off, y_off))
                for j in range(len(previous_curve)):
                    prev_segment = (previous_curve[j], previous_curve[(j + 1) % len(previous_curve)])
                    if do_lines_intersect(new_segment[0], new_segment[1], prev_segment[0], prev_segment[1]):
                        has_intersection = True
                        break
            
            # If too close or intersecting, adjust position
            if min_distance < min_separation or has_intersection:
                # Move point further inward to maintain minimum separation
                adjustment_factor = max(1.5, (min_separation - min_distance) / min_separation) if min_distance < min_separation else 1.5
                x_off += nx * adjustment_factor * offset * 0.5
                y_off += ny * adjustment_factor * offset * 0.5
        
        offset_points.append((x_off, y_off))
    return offset_points


def draw_nested_curves(canvas_size, all_curves, thickness=3):
    """Draw all nested curves with different colors."""
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Color palette for curves
    colors = ['black', 'red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 
              'cyan', 'magenta', 'darkred', 'darkblue', 'darkgreen', 'darkorange',
              'navy', 'maroon', 'olive', 'teal', 'indigo', 'crimson']
    
    # Draw each curve
    for i, curve_points in enumerate(all_curves):
        color = colors[i % len(colors)]
        line_width = thickness if i == 0 else 2  # First curve (circle) is thicker
        
        for j in range(len(curve_points)):
            p1 = curve_points[j]
            p2 = curve_points[(j + 1) % len(curve_points)]
            draw.line([p1, p2], fill=color, width=line_width)
    
    return image


def generate_nested_curves(canvas_size, radius, num_curves, step_length, 
                          offset_distance, variation_amount):
    """Generate a series of nested curves."""
    # Calculate number of points based on step length
    circumference = 2 * math.pi * radius
    num_points = int(circumference / step_length)
    
    # Start with the outer circle
    current_points = sample_circle_points(radius, num_points, canvas_size)
    all_curves = [current_points]
    
    # Generate nested curves
    for i in range(num_curves - 1):
        current_points = compute_offset_curve(current_points, offset_distance, variation_amount, all_curves[-1])
        all_curves.append(current_points)
    
    return all_curves


def main():
    st.title("Nested Curves Generator - Step 3")
    st.write("Generate multiple nested curves iteratively")
    
    # Sidebar controls
    st.sidebar.header("Parameters")
    
    # Number of curves
    num_curves = st.sidebar.slider(
        "Number of Curves", 
        min_value=2, 
        max_value=50, 
        value=20, 
        step=1,
        help="Total number of nested curves to generate"
    )
    
    # Line step length control
    step_length = st.sidebar.slider(
        "Line Step Length (pixels)", 
        min_value=0.5, 
        max_value=10.0, 
        value=2.0, 
        step=0.5,
        help="Length of each line segment. Smaller = smoother curves"
    )
    
    # Random variation control
    variation_amount = st.sidebar.slider(
        "Random Variation (pixels)", 
        min_value=0.0, 
        max_value=5.0, 
        value=1.5, 
        step=0.1,
        help="Amount of random variation to simulate human hand"
    )
    
    # Offset distance control
    offset_distance = st.sidebar.slider(
        "Offset Distance (pixels)", 
        min_value=1, 
        max_value=20, 
        value=5, 
        step=1,
        help="Distance between consecutive curves"
    )
    
    # Canvas and circle parameters
    canvas_size = 1000
    radius = 450
    thickness = 3
    
    # Calculate number of points based on step length
    circumference = 2 * math.pi * radius
    num_points = int(circumference / step_length)
    
    # Display current settings
    st.sidebar.write("---")
    st.sidebar.write(f"**Number of points per curve:** {num_points}")
    st.sidebar.write(f"**Circumference:** {circumference:.1f} pixels")
    st.sidebar.write(f"**Total curves:** {num_curves}")
    
    # Generate curves
    if st.button("Generate Nested Curves"):
        # Set random seed for reproducible results
        random.seed(42)
        
        # Generate all nested curves
        all_curves = generate_nested_curves(
            canvas_size, radius, num_curves, step_length, 
            offset_distance, variation_amount
        )
        
        # Draw all curves
        image = draw_nested_curves(canvas_size, all_curves, thickness)
        
        # Display image
        st.image(image, caption=f"Generated {num_curves} Nested Curves", use_container_width=True)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # PNG download
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            st.download_button(
                label="Download PNG",
                data=buffer.getvalue(),
                file_name=f"nested_curves_{num_curves}_step{step_length}_var{variation_amount}.png",
                mime="image/png"
            )
        
        with col2:
            # SVG download
            svg_content = generate_svg_nested(all_curves, canvas_size, thickness)
            st.download_button(
                label="Download SVG",
                data=svg_content,
                file_name=f"nested_curves_{num_curves}_step{step_length}_var{variation_amount}.svg",
                mime="image/svg+xml"
            )


def generate_svg_nested(all_curves, canvas_size, thickness):
    """Generate SVG content for nested curves."""
    def points_to_svg_path(points):
        return 'M ' + ' L '.join(f'{x:.2f},{y:.2f}' for x, y in points) + ' Z'
    
    colors = ['black', 'red', 'blue', 'green', 'purple', 'orange', 'brown', 'pink', 
              'cyan', 'magenta', 'darkred', 'darkblue', 'darkgreen', 'darkorange',
              'navy', 'maroon', 'olive', 'teal', 'indigo', 'crimson']
    
    svg_paths = []
    for i, curve_points in enumerate(all_curves):
        color = colors[i % len(colors)]
        line_width = thickness if i == 0 else 2
        path_data = points_to_svg_path(curve_points)
        svg_paths.append(f'<path d="{path_data}" fill="none" stroke="{color}" stroke-width="{line_width}"/>')
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{canvas_size}" height="{canvas_size}" fill="white"/>
  {chr(10).join(svg_paths)}
</svg>'''
    
    return svg_content


if __name__ == "__main__":
    main() 