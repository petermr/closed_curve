import streamlit as st
import math
import random
from PIL import Image, ImageDraw
import io

# Simple graphics bundle system
class SimpleGraphicsBundle:
    def __init__(self, name, color, width):
        self.name = name
        self.color = color
        self.width = width

def generate_initial_circle(center_x: float, center_y: float, radius: float, num_points: int = 50):
    """Generate initial circular curve with fewer points to prevent hanging."""
    points = []
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        points.append((x, y))
    return points

def generate_nested_curve_simple(outer_curve, distance: float, error: float):
    """Generate a nested curve by moving points inward with error."""
    if not outer_curve or len(outer_curve) < 3:
        return []
    
    # Calculate center of outer curve
    center_x = sum(p[0] for p in outer_curve) / len(outer_curve)
    center_y = sum(p[1] for p in outer_curve) / len(outer_curve)
    
    new_curve = []
    for i, point in enumerate(outer_curve):
        # Calculate direction from center to point
        dx = point[0] - center_x
        dy = point[1] - center_y
        
        # Normalize direction vector
        length = math.sqrt(dx*dx + dy*dy)
        if length > 0:
            dx /= length
            dy /= length
        
        # Move point inward by distance
        new_x = point[0] - dx * distance
        new_y = point[1] - dy * distance
        
        # Add random error (but less for first and last points to ensure closure)
        if i == 0 or i == len(outer_curve) - 1:
            error_x = random.uniform(-error * 0.3, error * 0.3)
            error_y = random.uniform(-error * 0.3, error * 0.3)
        else:
            error_x = random.uniform(-error, error)
            error_y = random.uniform(-error, error)
        
        new_curve.append((new_x + error_x, new_y + error_y))
    
    # Ensure the curve closes by making the last point very close to the first
    if len(new_curve) > 2:
        first_point = new_curve[0]
        last_point = new_curve[-1]
        # Average the first and last points to ensure closure
        avg_x = (first_point[0] + last_point[0]) / 2
        avg_y = (first_point[1] + last_point[1]) / 2
        new_curve[0] = (avg_x, avg_y)
        new_curve[-1] = (avg_x, avg_y)
    
    return new_curve

def draw_curves_simple(draw, curves, bundle):
    """Draw curves using the specified graphics bundle."""
    if not curves:
        return
    
    # Convert color string to RGB
    color_map = {
        'black': (0, 0, 0), 'red': (255, 0, 0), 'blue': (0, 0, 255),
        'green': (0, 128, 0), 'purple': (128, 0, 128), 'orange': (255, 165, 0),
        'brown': (139, 69, 19), 'pink': (255, 192, 203), 'cyan': (0, 255, 255),
        'gray': (128, 128, 128), 'magenta': (255, 0, 255), 'teal': (0, 128, 128),
        'gold': (255, 215, 0)
    }
    
    color = color_map.get(bundle.color.lower(), (0, 0, 0))
    
    # Draw each curve
    for curve in curves:
        if len(curve) < 2:
            continue
            
        # Draw line segments
        for i in range(len(curve) - 1):
            start_point = curve[i]
            end_point = curve[i + 1]
            draw.line([start_point, end_point], fill=color, width=bundle.width)

def main():
    st.set_page_config(page_title="AtPoE - Multi-Bundle Stable", page_icon="🎨", layout="wide")
    st.title("🎨 AtPoE - Multi-Bundle Interactive Curve Generator")
    st.markdown("Generate curves with different graphics bundles interactively")
    
    # Initialize session state
    if 'all_curves' not in st.session_state:
        st.session_state.all_curves = []
    if 'current_image' not in st.session_state:
        st.session_state.current_image = None
    if 'bundle_history' not in st.session_state:
        st.session_state.bundle_history = []
    
    # Simple bundle options
    bundle_options = [
        SimpleGraphicsBundle("Classic Black", "black", 2),
        SimpleGraphicsBundle("Classic Red", "red", 2),
        SimpleGraphicsBundle("Classic Blue", "blue", 2),
        SimpleGraphicsBundle("Bold Orange", "orange", 4),
        SimpleGraphicsBundle("Bold Brown", "brown", 4),
        SimpleGraphicsBundle("Thin Gray", "gray", 1),
        SimpleGraphicsBundle("Thin Magenta", "magenta", 1),
    ]
    
    # Sidebar for controls
    with st.sidebar:
        st.header("🎛️ Multi-Bundle Controls")
        
        # Bundle selection
        st.subheader("📦 Graphics Bundle")
        selected_bundle_name = st.selectbox(
            "Select Graphics Bundle:", 
            [bundle.name for bundle in bundle_options],
            key="bundle_selector"
        )
        selected_bundle = next((b for b in bundle_options if b.name == selected_bundle_name), bundle_options[0])
        
        # Display bundle info
        st.info(f"**{selected_bundle.name}**\n"
               f"Color: {selected_bundle.color}\n"
               f"Width: {selected_bundle.width}px")
        
        # Parameters for current bundle
        st.subheader("⚙️ Parameters")
        num_curves = st.slider("Number of Curves", 1, 8, 3, key="curves_slider")  # Reduced max to prevent hanging
        error_level = st.slider("Error Level", 0.0, 5.0, 1.5, 0.1, key="error_slider")
        curve_distance = st.slider("Curve Distance", 3, 20, 8, key="distance_slider")
        canvas_size = st.selectbox("Canvas Size", [800, 1000, 1200, 1500], index=1, key="canvas_slider")
        
        # Action buttons
        st.subheader("🎯 Actions")
        col1, col2 = st.columns(2)
        
        with col1:
            add_bundle_clicked = st.button("➕ Add Bundle", type="primary", key="add_bundle_btn")
        
        with col2:
            clear_all_clicked = st.button("🗑️ Clear All", key="clear_all_btn")
        
        # Bundle history
        if st.session_state.bundle_history:
            st.subheader("📚 Bundle History")
            for i, (bundle_name, curves_count) in enumerate(st.session_state.bundle_history):
                st.write(f"{i+1}. {bundle_name} ({curves_count} curves)")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🎨 Generated Curves")
        
        # Handle button clicks
        if add_bundle_clicked:
            try:
                # Generate curves for current bundle
                center_x = canvas_size / 2
                center_y = canvas_size / 2
                
                # Create new image or use existing
                if st.session_state.current_image is None:
                    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
                    draw = ImageDraw.Draw(image)
                    # Start with outer circle for first bundle
                    radius = min(canvas_size / 2 - 50, 300)
                    start_curve = generate_initial_circle(center_x, center_y, radius)
                else:
                    # Load existing image
                    image = st.session_state.current_image
                    draw = ImageDraw.Draw(image)
                    # Continue from the last curve of the previous bundle
                    if st.session_state.all_curves:
                        last_bundle_curves = st.session_state.all_curves[-1]
                        if last_bundle_curves:
                            start_curve = last_bundle_curves[-1]  # Use the innermost curve
                        else:
                            # Fallback to outer circle if no previous curves
                            radius = min(canvas_size / 2 - 50, 300)
                            start_curve = generate_initial_circle(center_x, center_y, radius)
                    else:
                        # Fallback to outer circle if no previous curves
                        radius = min(canvas_size / 2 - 50, 300)
                        start_curve = generate_initial_circle(center_x, center_y, radius)
                
                # Generate curves for this bundle, starting from the last curve
                bundle_curves = []
                
                for i in range(num_curves):
                    if i == 0:
                        # First curve: generate inward from the starting curve
                        # This ensures proper continuity and closure
                        curve = generate_nested_curve_simple(
                            start_curve, curve_distance, error_level
                        )
                    else:
                        # Nested curves continue inward from the previous curve in this bundle
                        curve = generate_nested_curve_simple(
                            bundle_curves[i-1], curve_distance, error_level
                        )
                    
                    if curve:
                        bundle_curves.append(curve)
                
                # Draw curves with current bundle
                draw_curves_simple(draw, bundle_curves, selected_bundle)
                
                # Update session state
                st.session_state.all_curves.append(bundle_curves)
                st.session_state.current_image = image
                st.session_state.bundle_history.append((selected_bundle.name, num_curves))
                
                st.success(f"✅ Added {num_curves} curves with '{selected_bundle.name}' bundle!")
                
            except Exception as e:
                st.error(f"❌ Error generating curves: {str(e)}")
        
        elif clear_all_clicked:
            st.session_state.all_curves = []
            st.session_state.current_image = None
            st.session_state.bundle_history = []
            st.info("🗑️ All curves cleared!")
        
        # Display current image
        if st.session_state.current_image:
            st.image(st.session_state.current_image, use_container_width=True)
            
            # Download buttons
            col_dl1, col_dl2 = st.columns(2)
            with col_dl1:
                # Convert PIL image to bytes for download
                img_buffer = io.BytesIO()
                st.session_state.current_image.save(img_buffer, format='PNG')
                img_buffer.seek(0)
                
                st.download_button(
                    label="📥 Download PNG",
                    data=img_buffer.getvalue(),
                    file_name=f"atpoe_multi_bundle_{len(st.session_state.bundle_history)}_bundles.png",
                    mime="image/png"
                )
        else:
            st.info("🎨 Click 'Add Bundle' to start generating curves!")
    
    with col2:
        st.subheader("📊 Status")
        
        # Current status
        total_bundles = len(st.session_state.bundle_history)
        total_curves = sum(curves_count for _, curves_count in st.session_state.bundle_history)
        
        st.metric("Total Bundles", total_bundles)
        st.metric("Total Curves", total_curves)
        
        if selected_bundle:
            st.metric("Selected Bundle", selected_bundle.name)
        
        # Current parameters
        st.subheader("⚙️ Current Parameters")
        st.write(f"**Curves:** {num_curves}")
        st.write(f"**Error Level:** {error_level}")
        st.write(f"**Curve Distance:** {curve_distance}")
        st.write(f"**Canvas Size:** {canvas_size}x{canvas_size}")
        
        # Instructions
        st.subheader("📖 Instructions")
        st.markdown("""
        1. **Select a graphics bundle** from the dropdown
        2. **Adjust parameters** as needed
        3. **Click 'Add Bundle'** to generate curves
        4. **Repeat** with different bundles
        5. **Download** your final composition
        
        **Tip:** Use thick curves as separators between different style groups!
        """)

if __name__ == "__main__":
    main()
