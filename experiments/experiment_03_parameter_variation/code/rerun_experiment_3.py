#!/usr/bin/env python3
"""
Rerun Experiment 3 with 30 and 40 curves
Original parameters: Distance=8px, Segment=4px, Error=3.0
"""

import sys
import os

# Add shared utilities to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'experiment_02_iterative_segments', 'code'))

from canvas_config import *
from coordinate_utils import distance
from segment_creator import create_next_closed_curve
from PIL import Image, ImageDraw
import xml.etree.ElementTree as ET
import random

def create_labeled_image(curves, canvas_size, output_file, params, num_curves):
    """Create PNG with parameter labels and antialiasing."""
    # Create image with white background
    image = Image.new('RGB', (canvas_size, canvas_size), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image, 'RGBA')  # Use RGBA for transparency
    
    # Color mapping
    colors = ['black', 'blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink']
    
    # Draw curves with antialiasing
    for i, curve in enumerate(curves):
        if len(curve) < 2:
            continue
        
        color = colors[i % len(colors)]
        
        # Draw multiple thin lines with slight offsets for antialiasing
        for offset in range(-1, 2):
            for offset2 in range(-1, 2):
                alpha = 100 if offset == 0 and offset2 == 0 else 30
                points = [(p[0] + offset, p[1] + offset2) for p in curve]
                draw.line(points, fill=color, width=1)
    
    # Add parameter labels
    label_text = f"Distance: {params['dist']}px, Segment: {params['segment_length']}px, Error: {params['error']}"
    curve_count_text = f"Curves: {num_curves}"
    
    # Draw text background
    draw.rectangle([5, 5, 400, 50], fill='white', outline='black')
    
    # Draw text
    draw.text((10, 10), label_text, fill='black')
    draw.text((10, 30), curve_count_text, fill='black')
    
    # Save with high quality
    image.save(output_file, 'PNG', optimize=True, quality=95)
    print(f"Labeled image saved to: {output_file}")

def create_labeled_svg(curves, canvas_size, output_file, params, num_curves):
    """Create SVG with parameter labels."""
    # Check total points to estimate file size
    total_points = sum(len(curve) for curve in curves)
    estimated_size_mb = total_points * 0.01  # Rough estimate: ~10KB per 1000 points
    
    if estimated_size_mb > 2:  # Lower limit for large curves
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
        
        curve_count_text = f"Curves: {num_curves} (Simplified)"
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
    
    curve_count_text = f"Curves: {num_curves}"
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

def run_experiment_3_with_curves(num_curves):
    """Run experiment 3 with specified number of curves."""
    print(f"\n=== Experiment 3 with {num_curves} curves ===")
    print("Distance: 8px, Segment: 4px, Error: 3.0")
    
    # Load existing OUTER_CURVE
    outer_curve_file = os.path.join(os.path.dirname(__file__), '..', '..', 'experiment_01_outer_curve', 'output', 'outer_curve_coordinates.txt')
    if os.path.exists(outer_curve_file):
        print("Loading existing OUTER_CURVE...")
        with open(outer_curve_file, 'r') as f:
            lines = f.readlines()
            outer_curve = []
            for line in lines:
                if line.strip():
                    x, y = map(float, line.strip().split(','))
                    outer_curve.append((x, y))
    else:
        print("ERROR: OUTER_CURVE not found!")
        return None
    
    # Parameters for experiment 3
    params = {
        'dist': 8,
        'segment_length': 4,
        'error': 3.0
    }
    
    curves = [outer_curve]
    
    # Generate nested curves
    for curve_num in range(2, num_curves + 1):
        print(f"Generating curve {curve_num}...")
        
        new_curve = create_next_closed_curve(
            curves[-1],
            dist=params['dist'],
            error=params['error'],
            segment_length=params['segment_length']
        )
        
        if new_curve:
            curves.append(new_curve)
            print(f"  Generated curve {curve_num} with {len(new_curve)} points")
        else:
            print(f"  Failed to generate curve {curve_num}")
            break
    
    # Create output directory
    output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
    os.makedirs(output_dir, exist_ok=True)
    
    # Save PNG
    png_file = os.path.join(output_dir, f'experiment_3_dist8_seg4_err3.0_{num_curves}curves.png')
    create_labeled_image(curves, CANVAS_SIZE, png_file, params, num_curves)
    
    # Save SVG
    svg_file = os.path.join(output_dir, f'experiment_3_dist8_seg4_err3.0_{num_curves}curves.svg')
    create_labeled_svg(curves, CANVAS_SIZE, svg_file, params, num_curves)
    
    # Print summary
    total_points = sum(len(curve) for curve in curves)
    print(f"Generated {len(curves)} curves with {total_points} total points")
    
    return curves

def main():
    """Main function to run both experiments."""
    print("Rerunning Experiment 3 with 30 and 40 curves")
    print("=============================================")
    
    # Run with 30 curves
    curves_30 = run_experiment_3_with_curves(30)
    
    # Run with 40 curves
    curves_40 = run_experiment_3_with_curves(40)
    
    print("\n==================================================")
    print("EXPERIMENT SUMMARY")
    print("==================================================")
    if curves_30:
        total_points_30 = sum(len(curve) for curve in curves_30)
        print(f"30 curves: {total_points_30} total points")
    if curves_40:
        total_points_40 = sum(len(curve) for curve in curves_40)
        print(f"40 curves: {total_points_40} total points")

if __name__ == "__main__":
    main() 