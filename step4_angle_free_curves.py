"""Step 4: Angle-free nested curves using only line segments of constant length."""

import streamlit as st
from PIL import Image, ImageDraw
import math
import random
import os
import io


def generate_initial_curve(canvas_size, num_segments, segment_length):
    """Generate initial curve as a regular polygon with constant segment length."""
    # Calculate radius from segment length and number of segments
    # For a regular polygon: segment_length = 2 * radius * sin(π/n)
    # So: radius = segment_length / (2 * sin(π/n))
    radius = segment_length / (2 * math.sin(math.pi / num_segments))
    
    # Start at the top of the circle
    center_x = canvas_size // 2
    center_y = canvas_size // 2
    start_x = center_x
    start_y = center_y - radius
    
    points = [(start_x, start_y)]
    current_x, current_y = start_x, start_y
    
    # Generate points by rotating around center
    for i in range(1, num_segments):
        # Calculate next point using rotation matrix
        angle = 2 * math.pi * i / num_segments
        next_x = center_x + (current_x - center_x) * math.cos(angle) - (current_y - center_y) * math.sin(angle)
        next_y = center_y + (current_x - center_x) * math.sin(angle) + (current_y - center_y) * math.cos(angle)
        points.append((next_x, next_y))
        current_x, current_y = next_x, next_y
    
    return points


def do_lines_intersect(p1, p2, p3, p4):
    """Check if line segments (p1,p2) and (p3,p4) intersect."""
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def point_to_line_distance(point, line_start, line_end):
    """Calculate distance from point to line segment."""
    px, py = point
    x1, y1 = line_start
    x2, y2 = line_end
    
    # Vector from line_start to line_end
    dx = x2 - x1
    dy = y2 - y1
    
    # Vector from line_start to point
    px_vec = px - x1
    py_vec = py - y1
    
    # Projection parameter
    t = max(0, min(1, (px_vec * dx + py_vec * dy) / (dx * dx + dy * dy)))
    
    # Closest point on line segment
    closest_x = x1 + t * dx
    closest_y = y1 + t * dy
    
    # Distance
    return math.hypot(px - closest_x, py - closest_y)


def generate_nested_curve(previous_curve, num_segments, segment_length, offset_distance, variation_amount):
    """Generate a new curve inside the previous one, starting close to the previous start."""
    if not previous_curve:
        return generate_initial_curve(1000, num_segments, segment_length)
    
    # Start close to the previous curve's start point
    prev_start = previous_curve[0]
    center_x = sum(p[0] for p in previous_curve) / len(previous_curve)
    center_y = sum(p[1] for p in previous_curve) / len(previous_curve)
    
    # Calculate inward direction from center to start
    dx = prev_start[0] - center_x
    dy = prev_start[1] - center_y
    length = math.hypot(dx, dy) or 1.0
    dx, dy = dx / length, dy / length
    
    # Start point for new curve (inward from previous start)
    start_x = prev_start[0] + dx * offset_distance
    start_y = prev_start[1] + dy * offset_distance
    
    # Add variation to start point
    if variation_amount > 0:
        start_x += random.uniform(-variation_amount, variation_amount)
        start_y += random.uniform(-variation_amount, variation_amount)
    
    points = [(start_x, start_y)]
    current_x, current_y = start_x, start_y
    
    # Generate remaining points
    for i in range(1, num_segments):
        # Try different directions to find valid next point
        best_point = None
        best_score = float('inf')
        
        # Try multiple directions around the current point
        for attempt in range(8):
            # Calculate direction (inward bias)
            angle = 2 * math.pi * attempt / 8
            dir_x = math.cos(angle)
            dir_y = math.sin(angle)
            
            # Add inward bias
            to_center_x = center_x - current_x
            to_center_y = center_y - current_y
            center_dist = math.hypot(to_center_x, to_center_y) or 1.0
            to_center_x, to_center_y = to_center_x / center_dist, to_center_y / center_dist
            
            # Combine direction with inward bias
            final_dir_x = 0.7 * dir_x + 0.3 * to_center_x
            final_dir_y = 0.7 * dir_y + 0.3 * to_center_y
            final_length = math.hypot(final_dir_x, final_dir_y) or 1.0
            final_dir_x, final_dir_y = final_dir_x / final_length, final_dir_y / final_length
            
            # Calculate candidate next point
            next_x = current_x + final_dir_x * segment_length
            next_y = current_y + final_dir_y * segment_length
            
            # Add variation
            if variation_amount > 0:
                next_x += random.uniform(-variation_amount, variation_amount)
                next_y += random.uniform(-variation_amount, variation_amount)
            
            # Check if this point is valid (no intersections, inside previous curve)
            is_valid = True
            min_distance = float('inf')
            
            # Check distance to previous curve
            for j in range(len(previous_curve)):
                prev_start = previous_curve[j]
                prev_end = previous_curve[(j + 1) % len(previous_curve)]
                dist = point_to_line_distance((next_x, next_y), prev_start, prev_end)
                min_distance = min(min_distance, dist)
                
                # Check for line intersections
                if len(points) > 0:
                    new_segment = (points[-1], (next_x, next_y))
                    prev_segment = (prev_start, prev_end)
                    if do_lines_intersect(new_segment[0], new_segment[1], prev_segment[0], prev_segment[1]):
                        is_valid = False
                        break
            
            if is_valid and min_distance > offset_distance * 0.3:
                # Score based on distance to previous curve (prefer closer but not too close)
                score = abs(min_distance - offset_distance * 0.5)
                if score < best_score:
                    best_score = score
                    best_point = (next_x, next_y)
        
        if best_point is None:
            # If no valid point found, move further inward
            best_point = (current_x + dx * segment_length * 0.5, current_y + dy * segment_length * 0.5)
        
        points.append(best_point)
        current_x, current_y = best_point
    
    return points


def draw_curves(canvas_size, all_curves, thickness=3):
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
        line_width = thickness if i == 0 else 2
        
        for j in range(len(curve_points)):
            p1 = curve_points[j]
            p2 = curve_points[(j + 1) % len(curve_points)]
            draw.line([p1, p2], fill=color, width=line_width)
    
    return image


def main():
    st.title("Angle-Free Nested Curves Generator - Step 4")
    st.write("Generate curves using only line segments of constant length")
    
    # Sidebar controls
    st.sidebar.header("Parameters")
    
    # Number of curves
    num_curves = st.sidebar.slider(
        "Number of Curves", 
        min_value=2, 
        max_value=20, 
        value=10, 
        step=1,
        help="Total number of nested curves to generate"
    )
    
    # Number of segments per curve
    num_segments = st.sidebar.slider(
        "Segments per Curve", 
        min_value=6, 
        max_value=50, 
        value=20, 
        step=1,
        help="Number of line segments in each curve"
    )
    
    # Segment length
    segment_length = st.sidebar.slider(
        "Segment Length (pixels)", 
        min_value=10, 
        max_value=50, 
        value=20, 
        step=5,
        help="Length of each line segment"
    )
    
    # Random variation control
    variation_amount = st.sidebar.slider(
        "Random Variation (pixels)", 
        min_value=0.0, 
        max_value=5.0, 
        value=1.0, 
        step=0.1,
        help="Amount of random variation"
    )
    
    # Offset distance control
    offset_distance = st.sidebar.slider(
        "Offset Distance (pixels)", 
        min_value=5, 
        max_value=30, 
        value=15, 
        step=1,
        help="Distance between consecutive curves"
    )
    
    # Canvas parameters
    canvas_size = 1000
    thickness = 3
    
    # Display current settings
    st.sidebar.write("---")
    st.sidebar.write(f"**Segments per curve:** {num_segments}")
    st.sidebar.write(f"**Segment length:** {segment_length} pixels")
    st.sidebar.write(f"**Total curves:** {num_curves}")
    
    # Generate curves
    if st.button("Generate Angle-Free Curves"):
        # Set random seed for reproducible results
        random.seed(42)
        
        # Generate all nested curves
        all_curves = []
        for i in range(num_curves):
            if i == 0:
                curve = generate_initial_curve(canvas_size, num_segments, segment_length)
            else:
                curve = generate_nested_curve(all_curves[-1], num_segments, segment_length, 
                                           offset_distance, variation_amount)
            all_curves.append(curve)
        
        # Draw all curves
        image = draw_curves(canvas_size, all_curves, thickness)
        
        # Display image
        st.image(image, caption=f"Generated {num_curves} Angle-Free Curves", use_container_width=True)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # PNG download
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            st.download_button(
                label="Download PNG",
                data=buffer.getvalue(),
                file_name=f"angle_free_curves_{num_curves}_seg{num_segments}_len{segment_length}.png",
                mime="image/png"
            )
        
        with col2:
            # SVG download
            svg_content = generate_svg(all_curves, canvas_size, thickness)
            st.download_button(
                label="Download SVG",
                data=svg_content,
                file_name=f"angle_free_curves_{num_curves}_seg{num_segments}_len{segment_length}.svg",
                mime="image/svg+xml"
            )


def generate_svg(all_curves, canvas_size, thickness):
    """Generate SVG content for curves."""
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