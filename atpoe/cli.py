#!/usr/bin/env python3
"""
Command-line interface for AtPoE (Admitting the Possibilities of Error).
"""

import argparse
import sys
import os
import math
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from atpoe.core.curve_generator import generate_circle_polygon, perturb_polygon
from PIL import Image, ImageDraw


def create_curves(num_curves, length, error, canvas_size=1000, output_file=None):
    """Generate and save curves using command line parameters."""
    
    # Initialize
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Generate curves
    curves = []
    center_x = canvas_size // 2
    center_y = canvas_size // 2
    
    for i in range(num_curves):
        if i == 0:
            # Generate initial circle
            radius = 450
            n_points = int(2 * math.pi * radius / length)
            curve = generate_circle_polygon(n_points, radius)
            curve = [(x + center_x, y + center_y) for x, y in curve]
        else:
            # Generate nested curve
            curve = perturb_polygon(curves[-1], length, error)
        
        curves.append(curve)
        print(f"Generated curve {i+1} ({len(curve)} segments)")
    
    # Draw curves
    for curve in curves:
        for j in range(len(curve)):
            p1 = curve[j]
            p2 = curve[(j + 1) % len(curve)]
            draw.line([p1, p2], fill='black', width=3)
    
    # Save or display
    if output_file:
        image.save(output_file)
        print(f"Saved curves to: {output_file}")
    else:
        image.show()
    
    return curves


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="AtPoE - Admitting the Possibilities of Error",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  atpoe --curves 10 --length 15 --error 1.5
  atpoe --curves 20 --length 10 --error 2.4 --output my_curves.png
        """
    )
    
    parser.add_argument(
        '--curves', '-c',
        type=int,
        default=10,
        help='Number of curves to generate (default: 10)'
    )
    
    parser.add_argument(
        '--length', '-l',
        type=int,
        default=15,
        help='Length of curve segments (default: 15)'
    )
    
    parser.add_argument(
        '--error', '-e',
        type=float,
        default=1.5,
        help='Error level for human-like variation (default: 1.5)'
    )
    
    parser.add_argument(
        '--canvas-size', '-s',
        type=int,
        default=1000,
        help='Canvas size in pixels (default: 1000)'
    )
    
    parser.add_argument(
        '--output', '-o',
        type=str,
        help='Output file path (PNG format)'
    )
    
    parser.add_argument(
        '--version', '-v',
        action='version',
        version='AtPoE 1.0.0'
    )
    
    args = parser.parse_args()
    
    # Generate curves with CLI parameters
    try:
        curves = create_curves(
            args.curves,
            args.length,
            args.error,
            args.canvas_size,
            args.output
        )
        print(f"Successfully generated {len(curves)} curves!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 