"""Step 2 GUI: Adjustable line step length and random variation for offset curves."""

import streamlit as st
from PIL import Image, ImageDraw
import math
import random
import os
import io
import base64


def sample_circle_points(radius, num_points, canvas_size):
    """Sample points along a circle perimeter."""
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = radius * math.cos(angle) + canvas_size / 2
        y = radius * math.sin(angle) + canvas_size / 2
        points.append((x, y))
    return points


def compute_offset_curve(points, offset, variation_amount):
    """Compute an offset curve with adjustable random variation."""
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
        
        # Add human-like variation (adjustable amount)
        if variation_amount > 0:
            variation_x = random.uniform(-variation_amount, variation_amount)
            variation_y = random.uniform(-variation_amount, variation_amount)
            x_off += variation_x
            y_off += variation_y
        
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


def image_to_base64(image):
    """Convert PIL image to base64 for display in Streamlit."""
    buffer = io.BytesIO()
    image.save(buffer, format='PNG')
    img_str = base64.b64encode(buffer.getvalue()).decode()
    return img_str


def main():
    st.title("Closed Curve Generator - Step 2")
    st.write("Adjust line step length and random variation for human-like curves")
    
    # Sidebar controls
    st.sidebar.header("Parameters")
    
    # Line step length control
    step_length = st.sidebar.slider(
        "Line Step Length (pixels)", 
        min_value=0.5, 
        max_value=10.0, 
        value=2.0, 
        step=0.5,
        help="Length of each line segment. Smaller = smoother curve"
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
        help="Distance of red curve from black circle"
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
    st.sidebar.write(f"**Number of points:** {num_points}")
    st.sidebar.write(f"**Circumference:** {circumference:.1f} pixels")
    
    # Generate curves
    if st.button("Generate Curves"):
        # Set random seed for reproducible results
        random.seed(42)
        
        # Generate points
        enclosing_points = sample_circle_points(radius, num_points, canvas_size)
        offset_points = compute_offset_curve(enclosing_points, offset_distance, variation_amount)
        
        # Draw curves
        image = draw_curves(canvas_size, enclosing_points, offset_points, thickness)
        
        # Display image
        st.image(image, caption="Generated Curves", use_container_width=True)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # PNG download
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            st.download_button(
                label="Download PNG",
                data=buffer.getvalue(),
                file_name=f"curves_step{step_length}_var{variation_amount}.png",
                mime="image/png"
            )
        
        with col2:
            # SVG download
            svg_content = generate_svg(enclosing_points, offset_points, canvas_size, thickness)
            st.download_button(
                label="Download SVG",
                data=svg_content,
                file_name=f"curves_step{step_length}_var{variation_amount}.svg",
                mime="image/svg+xml"
            )


def generate_svg(enclosing_points, offset_points, canvas_size, thickness):
    """Generate SVG content for download."""
    def points_to_svg_path(points):
        return 'M ' + ' L '.join(f'{x:.2f},{y:.2f}' for x, y in points) + ' Z'
    
    svg_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{canvas_size}" height="{canvas_size}" fill="white"/>
  <path d="{points_to_svg_path(enclosing_points)}" fill="none" stroke="black" stroke-width="{thickness}"/>
  <path d="{points_to_svg_path(offset_points)}" fill="none" stroke="red" stroke-width="2"/>
</svg>'''
    
    return svg_content


if __name__ == "__main__":
    main() 