"""
Experiment 03: Parameter Variation

This experiment tests different combinations of:
- Separation distance (≥ 3)
- Segment length
- Error function (≤ 4)

All diagrams are labeled with the parameters used.
"""

import sys
import os
from pathlib import Path

# Add shared utilities to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'experiment_01_outer_curve', 'code'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'experiment_02_iterative_segments', 'code'))

from canvas_config import *
from coordinate_utils import load_coordinates
from draw_outer_curve import draw_outer_curve
from segment_creator import create_next_closed_curve
from PIL import Image, ImageDraw, ImageFont
import xml.etree.ElementTree as ET


def create_labeled_image(curves, canvas_size, output_file, params):
    """Create image with parameter labels and antialiasing."""
    # Create image with antialiasing
    image = Image.new('RGB', (canvas_size, canvas_size), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image, 'RGBA')  # Use RGBA for antialiasing
    
    # Try to use a font, fallback to default if not available
    try:
        font = ImageFont.truetype("Arial.ttf", 16)
    except:
        font = ImageFont.load_default()
    
    # Draw curves with antialiasing
    colors = ['black', 'blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink']
    
    for i, curve in enumerate(curves):
        if len(curve) < 2:
            continue
        
        color = colors[i % len(colors)]
        
        # Convert color to RGBA for antialiasing
        if color == 'black':
            rgba_color = (0, 0, 0, 255)
        elif color == 'blue':
            rgba_color = (0, 0, 255, 255)
        elif color == 'red':
            rgba_color = (255, 0, 0, 255)
        elif color == 'green':
            rgba_color = (0, 128, 0, 255)
        elif color == 'purple':
            rgba_color = (128, 0, 128, 255)
        elif color == 'orange':
            rgba_color = (255, 165, 0, 255)
        elif color == 'brown':
            rgba_color = (139, 69, 19, 255)
        elif color == 'pink':
            rgba_color = (255, 192, 203, 255)
        else:
            rgba_color = (0, 0, 0, 255)
        
        # Draw the curve with antialiasing
        for j in range(len(curve)):
            p1 = curve[j]
            p2 = curve[(j + 1) % len(curve)]
            # Draw multiple thin lines for antialiasing effect
            for offset in range(-1, 2):
                for offset2 in range(-1, 2):
                    if offset == 0 and offset2 == 0:
                        # Main line
                        draw.line([p1, p2], fill=rgba_color, width=LINE_WIDTH)
                    else:
                        # Subtle offset lines for antialiasing
                        p1_offset = (p1[0] + offset, p1[1] + offset2)
                        p2_offset = (p2[0] + offset, p2[1] + offset2)
                        draw.line([p1_offset, p2_offset], fill=(rgba_color[0], rgba_color[1], rgba_color[2], 50), width=1)
    
    # Add parameter labels
    label_text = f"Distance: {params['dist']}px, Segment: {params['segment_length']}px, Error: {params['error']}"
    draw.text((10, 10), label_text, fill='black', font=font)
    
    # Add curve count
    curve_count_text = f"Curves: {len(curves)}"
    draw.text((10, 30), curve_count_text, fill='black', font=font)
    
    # Save image with high quality
    image.save(output_file, 'PNG', optimize=True, quality=95)
    print(f"Labeled image saved to: {output_file}")


def create_labeled_svg(curves, canvas_size, output_file, params):
    """Create SVG with parameter labels."""
    # Check total points to estimate file size
    total_points = sum(len(curve) for curve in curves)
    estimated_size_mb = total_points * 0.01  # Rough estimate: ~10KB per 1000 points
    
    if estimated_size_mb > 2:  # Lower limit for 5 curves
        print(f"WARNING: Estimated SVG size would be ~{estimated_size_mb:.1f}MB (>2MB limit)")
        print(f"Creating simplified SVG with reduced points...")
        
        # Create simplified SVG with fewer points
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
        
        # Add curves as simplified path elements (every 10th point)
        for i, curve in enumerate(curves):
            if len(curve) < 2:
                continue
            
            color = colors[i % len(colors)]
            
            # Sample every 10th point to reduce file size
            sampled_curve = curve[::10]
            if len(sampled_curve) < 2:
                sampled_curve = curve[::5]  # If still too few, sample every 5th
            if len(sampled_curve) < 2:
                sampled_curve = curve  # Use all points if necessary
            
            # Create path data
            path_data = f"M {sampled_curve[0][0]:.1f} {sampled_curve[0][1]:.1f}"
            for point in sampled_curve[1:]:
                path_data += f" L {point[0]:.1f} {point[1]:.1f}"
            
            # Add path element
            path = ET.SubElement(svg, 'path', {
                'd': path_data,
                'stroke': color,
                'stroke-width': '2',
                'fill': 'none'
            })
        
        # Add parameter labels as text elements
        label_text = f"Distance: {params['dist']}px, Segment: {params['segment_length']}px, Error: {params['error']} (Simplified)"
        text = ET.SubElement(svg, 'text', {
            'x': '10',
            'y': '25',
            'font-family': 'Arial',
            'font-size': '16',
            'fill': 'black'
        })
        text.text = label_text
        
        curve_count_text = f"Curves: {len(curves)} (Simplified)"
        text2 = ET.SubElement(svg, 'text', {
            'x': '10',
            'y': '45',
            'font-family': 'Arial',
            'font-size': '16',
            'fill': 'black'
        })
        text2.text = curve_count_text
        
        # Write SVG file
        tree = ET.ElementTree(svg)
        tree.write(output_file, encoding='utf-8', xml_declaration=True)
        print(f"Simplified SVG saved to: {output_file}")
        return True
    
    # Create full SVG for smaller files
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
    
    # Add parameter labels as text elements
    label_text = f"Distance: {params['dist']}px, Segment: {params['segment_length']}px, Error: {params['error']}"
    text = ET.SubElement(svg, 'text', {
        'x': '10',
        'y': '25',
        'font-family': 'Arial',
        'font-size': '16',
        'fill': 'black'
    })
    text.text = label_text
    
    curve_count_text = f"Curves: {len(curves)}"
    text2 = ET.SubElement(svg, 'text', {
        'x': '10',
        'y': '45',
        'font-family': 'Arial',
        'font-size': '16',
        'fill': 'black'
    })
    text2.text = curve_count_text
    
    # Write SVG file
    tree = ET.ElementTree(svg)
    tree.write(output_file, encoding='utf-8', xml_declaration=True)
    print(f"Labeled SVG saved to: {output_file}")
    return True


def run_parameter_experiment(experiment_num, dist, segment_length, error, num_curves=10):
    """Run a single parameter experiment."""
    print(f"\n=== Experiment {experiment_num} ===")
    print(f"Distance: {dist}px, Segment: {segment_length}px, Error: {error}")
    
    # Load or create OUTER_CURVE
    outer_curve_file = Path(__file__).parent.parent.parent / 'experiment_01_outer_curve' / 'output' / 'outer_curve_coordinates.txt'
    if outer_curve_file.exists():
        print("Loading existing OUTER_CURVE...")
        outer_curve = load_coordinates(outer_curve_file)
    else:
        print("Creating OUTER_CURVE...")
        outer_curve = draw_outer_curve()
    
    # Generate curves
    curves = [outer_curve]
    previous_curve = outer_curve
    
    for curve_num in range(1, num_curves + 1):
        print(f"Generating curve {curve_num + 1}...")
        
        new_curve = create_next_closed_curve(previous_curve, dist, error, segment_length)
        
        if new_curve:
            curves.append(new_curve)
            previous_curve = new_curve
            print(f"  Generated curve {curve_num + 1} with {len(new_curve)} points")
        else:
            print(f"  Failed to generate curve {curve_num + 1}")
            break
    
    # Create output files
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    params = {
        'dist': dist,
        'segment_length': segment_length,
        'error': error
    }
    
    # Save labeled images
    png_file = output_dir / f'experiment_{experiment_num}_dist{dist}_seg{segment_length}_err{error}.png'
    svg_file = output_dir / f'experiment_{experiment_num}_dist{dist}_seg{segment_length}_err{error}.svg'
    
    create_labeled_image(curves, 1200, str(png_file), params)
    svg_created = create_labeled_svg(curves, 1200, str(svg_file), params)
    
    if not svg_created:
        # Remove the SVG file if it was created but too large
        if svg_file.exists():
            svg_file.unlink()
    
    return curves


def main():
    """Run all parameter experiments."""
    print("Starting Parameter Variation Experiments")
    print("=======================================")
    
    # Define 5 different parameter sets with reasonable error values
    experiments = [
        # Experiment 1: Small distance, small segments, low error
        {'dist': 3, 'segment_length': 2, 'error': 0.5},
        
        # Experiment 2: Medium distance, medium segments, medium error
        {'dist': 5, 'segment_length': 3, 'error': 1.0},
        
        # Experiment 3: Large distance, large segments, moderate error
        {'dist': 8, 'segment_length': 4, 'error': 1.5},
        
        # Experiment 4: Small distance, large segments, low error
        {'dist': 4, 'segment_length': 5, 'error': 0.3},
        
        # Experiment 5: Large distance, small segments, moderate error
        {'dist': 10, 'segment_length': 2, 'error': 2.0}
    ]
    
    all_results = []
    
    for i, params in enumerate(experiments, 1):
        curves = run_parameter_experiment(
            experiment_num=i,
            dist=params['dist'],
            segment_length=params['segment_length'],
            error=params['error'],
            num_curves=5  # Reduced to 5 curves for smaller SVG files
        )
        all_results.append({
            'experiment': i,
            'params': params,
            'curves': len(curves),
            'total_points': sum(len(curve) for curve in curves)
        })
    
    # Print summary
    print("\n" + "="*50)
    print("EXPERIMENT SUMMARY")
    print("="*50)
    for result in all_results:
        print(f"Experiment {result['experiment']}: "
              f"Distance={result['params']['dist']}px, "
              f"Segment={result['params']['segment_length']}px, "
              f"Error={result['params']['error']} → "
              f"{result['curves']} curves, {result['total_points']} total points")


if __name__ == "__main__":
    main() 