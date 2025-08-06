"""
Experiment 02: Iterative Segment Generation

RULE 2: The algorithm adds segments iteratively.
- Create and draw OUTER_CURVE
- Set previous_curve = OUTER_CURVE
- Create new_closed_curve of segments inside previous_curve by keeping approximately DIST away
"""

import sys
import os
from pathlib import Path

# Add shared utilities to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'experiment_01_outer_curve', 'code'))

from canvas_config import *
from coordinate_utils import save_coordinates, load_coordinates
from draw_outer_curve import draw_outer_curve
from segment_creator import create_next_closed_curve
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET


def generate_iterative_curves(outer_curve, dist=DEFAULT_DIST, num_curves=5, 
                            canvas_size=CANVAS_SIZE, output_file=None):
    """
    Generate iterative curves according to RULE 2.
    
    Args:
        outer_curve: The OUTER_CURVE coordinates
        dist: Target distance between curves
        num_curves: Number of curves to generate (including outer curve)
        canvas_size: Canvas size in pixels
        output_file: Output file path for combined image
    
    Returns:
        List of all generated curves
    """
    curves = [outer_curve]  # Start with OUTER_CURVE
    previous_curve = outer_curve
    
    # Create canvas for combined image
    image = Image.new('RGB', (canvas_size, canvas_size), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    
    # Draw OUTER_CURVE
    for i in range(len(outer_curve)):
        p1 = outer_curve[i]
        p2 = outer_curve[(i + 1) % len(outer_curve)]
        draw.line([p1, p2], fill=CURVE_COLORS[0], width=LINE_WIDTH)
    
    # Generate iterative curves
    for curve_num in range(1, num_curves):
        print(f"Generating curve {curve_num + 1}...")
        
        # Create new closed curve inside previous curve
        new_curve = create_next_closed_curve(previous_curve, dist)
        
        if new_curve:
            curves.append(new_curve)
            
            # Draw new curve
            color = CURVE_COLORS[curve_num % len(CURVE_COLORS)]
            for i in range(len(new_curve)):
                p1 = new_curve[i]
                p2 = new_curve[(i + 1) % len(new_curve)]
                draw.line([p1, p2], fill=color, width=LINE_WIDTH)
            
            # Save individual curve coordinates
            output_dir = Path(__file__).parent.parent / 'output'
            coords_file = output_dir / f'curve_{curve_num + 1}_coordinates.txt'
            save_coordinates(new_curve, coords_file)
            
            # Update previous curve for next iteration
            previous_curve = new_curve
            
            print(f"  Generated curve {curve_num + 1} with {len(new_curve)} points")
        else:
            print(f"  Failed to generate curve {curve_num + 1}")
            break
    
    # Save combined image
    if output_file:
        image.save(output_file)
        print(f"All curves saved to: {output_file}")
        
        # Also save as SVG
        svg_file = output_file.replace('.png', '.svg')
        save_as_svg(curves, canvas_size, svg_file)
        print(f"SVG version saved to: {svg_file}")
    
    return curves


def save_as_svg(curves, canvas_size, output_file):
    """Save curves as SVG file for vector examination."""
    # Create SVG root element
    svg = ET.Element('svg', {
        'width': str(canvas_size),
        'height': str(canvas_size),
        'xmlns': 'http://www.w3.org/2000/svg',
        'version': '1.1'
    })
    
    # Add background rectangle
    background = ET.SubElement(svg, 'rect', {
        'width': str(canvas_size),
        'height': str(canvas_size),
        'fill': 'white'
    })
    
    # Color mapping
    colors = ['black', 'blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink']
    
    # Add curves as path elements
    for i, curve in enumerate(curves):
        if len(curve) < 2:
            continue
        
        color = colors[i % len(colors)]
        
        # Create path data
        path_data = f"M {curve[0][0]} {curve[0][1]}"
        for point in curve[1:]:
            path_data += f" L {point[0]} {point[1]}"
        
        # Add path element
        path = ET.SubElement(svg, 'path', {
            'd': path_data,
            'stroke': color,
            'stroke-width': '2',
            'fill': 'none'
        })
    
    # Write SVG file
    tree = ET.ElementTree(svg)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)


def main():
    """Main function for experiment 02."""
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    # First, create OUTER_CURVE if it doesn't exist
    outer_curve_file = output_dir / 'outer_curve_coordinates.txt'
    if not outer_curve_file.exists():
        print("Creating OUTER_CURVE...")
        from draw_outer_curve import main as create_outer_curve
        outer_curve = create_outer_curve()
    else:
        print("Loading existing OUTER_CURVE...")
        outer_curve = load_coordinates(outer_curve_file)
    
    # Generate iterative curves with experiment versioning
    experiment_count = 1
    while (output_dir / f'curves_sequence_v{experiment_count}.png').exists():
        experiment_count += 1
    
    output_file = output_dir / f'curves_sequence_v{experiment_count}.png'
    curves = generate_iterative_curves(
        outer_curve=outer_curve,
        dist=6,  # Increased by 50%
        num_curves=30,  # Generate 30 curves
        canvas_size=1200,
        output_file=str(output_file)
    )
    
    print(f"Generated {len(curves)} curves total")
    return curves


if __name__ == "__main__":
    main() 