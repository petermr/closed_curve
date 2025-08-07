#!/usr/bin/env python3
"""
Streamlit GUI for AtPoE (Admitting the Possibilities of Error).
Interactive curve generation with graphics bundle selection.
"""

import streamlit as st
import math
import random
from PIL import Image, ImageDraw
import io
import os
from typing import List, Tuple, Optional

# Import our graphics bundle system
from graphics_bundle import BundleLibrary, GraphicsBundle, StrokeStyle
from collision_detector import IncrementalCollisionDetector


def generate_initial_circle(canvas_size: int, radius: int, segment_length: int = 3) -> List[Tuple[float, float]]:
    """Generate initial circle centered at canvas center with fixed segment length."""
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


def generate_nested_curve(outer_curve: List[Tuple[float, float]], 
                         length: int, error: float, segment_length: int = 3) -> Optional[List[Tuple[float, float]]]:
    """Generate a nested curve inside the outer curve."""
    if len(outer_curve) < 3:
        return None
    
    center_x = sum(x for x, y in outer_curve) / len(outer_curve)
    center_y = sum(y for x, y in outer_curve) / len(outer_curve)
    
    new_curve = []
    
    # Find starting point
    max_dist = 0
    start_outer_point = None
    for ox, oy in outer_curve:
        dist = math.hypot(ox - center_x, oy - center_y)
        if dist > max_dist:
            max_dist = dist
            start_outer_point = (ox, oy)
    
    if not start_outer_point:
        return None
    
    # Calculate first point
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


def draw_curves_with_bundle(curves: List[List[Tuple[float, float]]], 
                          bundle: GraphicsBundle, 
                          canvas_size: int = 1000) -> Image.Image:
    """Draw curves using the specified graphics bundle."""
    img = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(img)
    
    for curve in curves:
        if len(curve) < 2:
            continue
        
        for j in range(len(curve)):
            p1 = curve[j]
            p2 = curve[(j + 1) % len(curve)]
            
            if bundle.stroke_style == StrokeStyle.DASHED and j % 2 == 0:
                draw.line([p1, p2], fill=bundle.color, width=bundle.width)
            elif bundle.stroke_style == StrokeStyle.DOTTED and j % 3 == 0:
                draw.line([p1, p2], fill=bundle.color, width=bundle.width)
            elif bundle.stroke_style == StrokeStyle.DASH_DOT and j % 4 < 2:
                draw.line([p1, p2], fill=bundle.color, width=bundle.width)
            elif bundle.stroke_style == StrokeStyle.SOLID:
                draw.line([p1, p2], fill=bundle.color, width=bundle.width)
    
    return img


def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="AtPoE - Interactive Curve Generator",
        page_icon="🎨",
        layout="wide"
    )
    
    st.title("🎨 AtPoE - Admitting the Possibilities of Error")
    st.markdown("Interactive curve generation with graphics bundle selection")
    
    # Initialize session state
    if 'curves' not in st.session_state:
        st.session_state.curves = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Controls")
        
        # Graphics Bundle Selection
        st.subheader("Graphics Bundle")
        bundle_library = BundleLibrary()
        bundle_names = bundle_library.get_bundle_names()
        
        selected_bundle_name = st.selectbox(
            "Select Graphics Bundle:",
            bundle_names,
            index=0
        )
        
        selected_bundle = bundle_library.get_bundle(selected_bundle_name)
        
        if selected_bundle:
            st.info(f"""
            **Selected Bundle: {selected_bundle.name}**
            - Color: {selected_bundle.color}
            - Width: {selected_bundle.width}px
            - Style: {selected_bundle.stroke_style.value}
            - {selected_bundle.description}
            """)
        
        # Parameter Controls
        st.subheader("Parameters")
        
        col1, col2 = st.columns(2)
        
        with col1:
            num_curves = st.slider("Number of Curves", 1, 50, 10)
            segment_length = st.slider("Segment Length", 3, 30, 12)
        
        with col2:
            error_level = st.slider("Error Level", 0.0, 5.0, 1.5, 0.1)
            curve_distance = st.slider("Curve Distance", 3, 20, 8)
        
        canvas_size = st.selectbox("Canvas Size", [800, 1000, 1200, 1500], index=1)
        
        # Action Buttons
        st.subheader("Actions")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("🔄 Generate Curves", type="primary"):
                generate_curves(num_curves, segment_length, error_level, curve_distance, canvas_size, selected_bundle)
        
        with col2:
            if st.button("🗑️ Clear All"):
                st.session_state.curves = []
                st.session_state.current_image = None
                st.rerun()
        
        # Batch Generation
        st.subheader("Batch Generation")
        batch_size = st.slider("Curves per Batch", 1, 10, 3)
        
        if st.button("➕ Add Batch"):
            add_batch(batch_size, segment_length, error_level, curve_distance, canvas_size, selected_bundle)
    
    # Main area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎨 Generated Curves")
        
        if st.session_state.current_image:
            st.image(st.session_state.current_image, use_column_width=True)
            
            # Download buttons
            col1, col2 = st.columns(2)
            
            with col1:
                img_byte_arr = io.BytesIO()
                st.session_state.current_image.save(img_byte_arr, format='PNG')
                img_byte_arr = img_byte_arr.getvalue()
                
                st.download_button(
                    label="📥 Download PNG",
                    data=img_byte_arr,
                    file_name=f"atpoe_curves_{len(st.session_state.curves)}.png",
                    mime="image/png"
                )
            
            with col2:
                svg_content = create_svg(st.session_state.curves, selected_bundle, canvas_size)
                st.download_button(
                    label="📥 Download SVG",
                    data=svg_content,
                    file_name=f"atpoe_curves_{len(st.session_state.curves)}.svg",
                    mime="image/svg+xml"
                )
        else:
            st.info("Click 'Generate Curves' to create your first curve!")
    
    with col2:
        st.subheader("📊 Status")
        
        st.metric("Total Curves", len(st.session_state.curves))
        
        if st.session_state.curves:
            st.metric("Canvas Size", f"{canvas_size}x{canvas_size}")
            st.metric("Segment Length", f"{segment_length}px")
            st.metric("Error Level", f"{error_level}px")
            st.metric("Curve Distance", f"{curve_distance}px")
        
        # Bundle Info
        if selected_bundle:
            st.subheader("🎨 Bundle Info")
            st.write(f"**Name:** {selected_bundle.name}")
            st.write(f"**Color:** {selected_bundle.color}")
            st.write(f"**Width:** {selected_bundle.width}px")
            st.write(f"**Style:** {selected_bundle.stroke_style.value}")
            st.write(f"**Description:** {selected_bundle.description}")


def generate_curves(num_curves: int, segment_length: int, error_level: float, 
                   curve_distance: int, canvas_size: int, bundle: GraphicsBundle):
    """Generate curves with the specified parameters."""
    with st.spinner("Generating curves..."):
        curves = []
        
        # Generate initial circle
        initial_curve = generate_initial_circle(canvas_size, 450, segment_length)
        curves.append(initial_curve)
        
        # Generate nested curves
        for i in range(num_curves - 1):
            new_curve = generate_nested_curve(curves[-1], curve_distance, error_level, segment_length)
            if new_curve:
                curves.append(new_curve)
            else:
                st.warning(f"Failed to generate curve {i + 2}")
                break
        
        # Store in session state
        st.session_state.curves = curves
        
        # Draw and store image
        st.session_state.current_image = draw_curves_with_bundle(curves, bundle, canvas_size)
        
        st.success(f"Generated {len(curves)} curves successfully!")
        st.rerun()


def add_batch(batch_size: int, segment_length: int, error_level: float, 
              curve_distance: int, canvas_size: int, bundle: GraphicsBundle):
    """Add a batch of curves to existing curves."""
    if not st.session_state.curves:
        st.error("No existing curves to add to. Please generate curves first.")
        return
    
    with st.spinner(f"Adding {batch_size} curves..."):
        curves = st.session_state.curves.copy()
        
        # Generate additional curves
        for i in range(batch_size):
            new_curve = generate_nested_curve(curves[-1], curve_distance, error_level, segment_length)
            if new_curve:
                curves.append(new_curve)
            else:
                st.warning(f"Failed to generate additional curve {i + 1}")
                break
        
        # Update session state
        st.session_state.curves = curves
        st.session_state.current_image = draw_curves_with_bundle(curves, bundle, canvas_size)
        
        st.success(f"Added {len(curves) - len(st.session_state.curves) + batch_size} curves!")
        st.rerun()


def create_svg(curves: List[List[Tuple[float, float]]], bundle: GraphicsBundle, canvas_size: int) -> str:
    """Create SVG content for the curves."""
    svg_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<svg width="{canvas_size}" height="{canvas_size}" xmlns="http://www.w3.org/2000/svg">
  <rect width="{canvas_size}" height="{canvas_size}" fill="white"/>
"""
    
    for curve in curves:
        if len(curve) < 2:
            continue
        
        path_data = f"M {curve[0][0]} {curve[0][1]}"
        for point in curve[1:]:
            path_data += f" L {point[0]} {point[1]}"
        path_data += " Z"
        
        stroke_dasharray = ""
        if bundle.stroke_style == StrokeStyle.DASHED:
            stroke_dasharray = f'stroke-dasharray="{bundle.width * 2},{bundle.width}"'
        elif bundle.stroke_style == StrokeStyle.DOTTED:
            stroke_dasharray = f'stroke-dasharray="{bundle.width},{bundle.width}"'
        elif bundle.stroke_style == StrokeStyle.DASH_DOT:
            stroke_dasharray = f'stroke-dasharray="{bundle.width * 3},{bundle.width},{bundle.width},{bundle.width}"'
        
        svg_content += f'  <path d="{path_data}" stroke="{bundle.color}" stroke-width="{bundle.width}" fill="none" {stroke_dasharray}/>\n'
    
    svg_content += "</svg>"
    return svg_content


if __name__ == "__main__":
    main()
