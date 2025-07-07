"""Step 4: Truly angle-free nested curves using only line segments of constant length."""

import streamlit as st
from PIL import Image, ImageDraw
import math
import random
import os
import io


def generate_initial_circle(canvas_size, radius=450):
    """Generate initial circle with radius 450, width 3, color black."""
    center_x = canvas_size // 2
    center_y = canvas_size // 2
    
    # Calculate number of segments needed for smooth circle
    # Use segment length of approximately 2 pixels for smooth appearance
    segment_length = 2.0
    circumference = 2 * math.pi * radius
    num_segments = int(circumference / segment_length)
    
    points = []
    for i in range(num_segments):
        angle = 2 * math.pi * i / num_segments
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    
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


def generate_nested_curve_angle_free(previous_curve, segment_length, offset_distance, variation_amount):
    """Generate a new curve inside the previous one with variable number of segments."""
    if not previous_curve:
        return generate_initial_circle(1000, 450)
    
    # Start close to the previous curve's start point
    prev_start = previous_curve[0]
    
    # Calculate center of previous curve
    center_x = sum(p[0] for p in previous_curve) / len(previous_curve)
    center_y = sum(p[1] for p in previous_curve) / len(previous_curve)
    
    # Calculate inward direction from center to start (no angles)
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
    
    # Calculate approximate perimeter of the new curve
    # Estimate based on previous curve's perimeter minus offset
    prev_perimeter = sum(math.hypot(previous_curve[i][0] - previous_curve[(i+1) % len(previous_curve)][0],
                                   previous_curve[i][1] - previous_curve[(i+1) % len(previous_curve)][1])
                        for i in range(len(previous_curve)))
    
    # New curve will have smaller perimeter
    estimated_perimeter = prev_perimeter * 0.8  # Rough estimate
    num_segments = max(6, int(estimated_perimeter / segment_length))
    
    # Generate remaining points using only geometric operations
    for i in range(1, num_segments):
        # Try different directions to find valid next point
        best_point = None
        best_score = float('inf')
        
        # Try multiple directions around the current point (no angles)
        for attempt in range(8):
            # Use predefined direction vectors (no trig)
            directions = [
                (1, 0), (0.7, 0.7), (0, 1), (-0.7, 0.7),
                (-1, 0), (-0.7, -0.7), (0, -1), (0.7, -0.7)
            ]
            dir_x, dir_y = directions[attempt]
            
            # Add inward bias (toward center)
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
        if i == 0:
            # Starting circle: black, width 3
            color = 'black'
            line_width = 3
        else:
            # Subsequent curves: different colors, width 2
            color = colors[(i-1) % len(colors)]
            line_width = 2
        
        for j in range(len(curve_points)):
            p1 = curve_points[j]
            p2 = curve_points[(j + 1) % len(curve_points)]
            draw.line([p1, p2], fill=color, width=line_width)
    
    return image


def main():
    st.title("Truly Angle-Free Nested Curves Generator - Step 4")
    st.write("Generate curves using only line segments of constant length (no angles)")
    
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
    
    # Number of segments per curve (for display only - will be calculated dynamically)
    st.sidebar.write("**Note:** Number of segments is calculated dynamically based on available space")
    
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
    st.sidebar.write(f"**Starting circle:** Radius 450, width 3, black")
    st.sidebar.write(f"**Segment length:** {segment_length} pixels")
    st.sidebar.write(f"**Total curves:** {num_curves}")
    
    # Generate curves
    if st.button("Generate Truly Angle-Free Curves"):
        # Set random seed for reproducible results
        random.seed(42)
        
        # Generate all nested curves
        all_curves = []
        for i in range(num_curves):
            if i == 0:
                curve = generate_initial_circle(canvas_size, 450)
            else:
                curve = generate_nested_curve_angle_free(all_curves[-1], segment_length, 
                                                       offset_distance, variation_amount)
            all_curves.append(curve)
        
        # Draw all curves
        image = draw_curves(canvas_size, all_curves, thickness)
        
        # Display image
        st.image(image, caption=f"Generated {num_curves} Truly Angle-Free Curves", use_container_width=True)
        
        # Download buttons
        col1, col2 = st.columns(2)
        
        with col1:
            # PNG download
            buffer = io.BytesIO()
            image.save(buffer, format='PNG')
            
            # Ensure images directory exists
            images_dir = "images"
            if not os.path.exists(images_dir):
                os.makedirs(images_dir)
            
            # Save to images directory
            png_filename = f"truly_angle_free_curves_{num_curves}_len{segment_length}.png"
            png_path = os.path.join(images_dir, png_filename)
            image.save(png_path, format='PNG')
            
            st.download_button(
                label="Download PNG",
                data=buffer.getvalue(),
                file_name=png_filename,
                mime="image/png"
            )
            st.write(f"Saved to: {png_path}")
        
        with col2:
            # SVG download
            svg_content = generate_svg(all_curves, canvas_size, thickness)
            
            # Save SVG to images directory
            svg_filename = f"truly_angle_free_curves_{num_curves}_len{segment_length}.svg"
            svg_path = os.path.join(images_dir, svg_filename)
            
            with open(svg_path, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            st.download_button(
                label="Download SVG",
                data=svg_content,
                file_name=svg_filename,
                mime="image/svg+xml"
            )
            st.write(f"Saved to: {svg_path}")


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