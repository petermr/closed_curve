#!/usr/bin/env python3
"""
Command-line interface for AtPoE (Admitting the Possibilities of Error).
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional

from atpoe.core.curve_generator import generate_nested_curve, generate_initial_circle
from PIL import Image, ImageDraw


def create_curves(
    num_curves: int, 
    segment_length: int, 
    error: float, 
    inter_curve_distance: int, 
    canvas_size: int = 1000, 
    output_file: Optional[str] = None
) -> List[List[Tuple[float, float]]]:
    """Generate and save curves using command line parameters."""
    
    # Initialize
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Generate curves
    curves = []
    colors = ['black', 'blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan']
    
    for i in range(num_curves):
        if i == 0:
            curve = generate_initial_circle(canvas_size, 450, segment_length)
        else:
            curve = generate_nested_curve(curves[-1], inter_curve_distance, error, segment_length)
        
        curves.append(curve)
        print(f"Generated curve {i+1} ({len(curve)} segments)")
        
        # Debug: print first few points of each curve
        if len(curve) > 0:
            print(f"  Curve {i+1} starts at: {curve[0]}")
            print(f"  Curve {i+1} ends at: {curve[-1]}")
    
    # Draw curves with different colors
    for i, curve in enumerate(curves):
        color = colors[i % len(colors)]
        for j in range(len(curve)):
            p1 = curve[j]
            p2 = curve[(j + 1) % len(curve)]
            draw.line([p1, p2], fill=color, width=2)
    
    # Save or display
    if output_file:
        image.save(output_file)
        print(f"Saved curves to: {output_file}")
    else:
        image.show()
    
    return curves


def main() -> None:
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="AtPoE - Admitting the Possibilities of Error",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  atpoe --curves 10 --segment-length 15 --error 1.5 --distance 6
  atpoe --curves 20 --segment-length 10 --error 2.4 --distance 8 --output my_curves.png
        """
    )
    
    parser.add_argument(
        '--curves', '-c',
        type=int,
        default=10,
        help='Number of curves to generate (default: 10)'
    )
    
    parser.add_argument(
        '--segment-length', '-l',
        type=int,
        default=3,
        help='Length of each line segment in pixels (default: 3)'
    )
    
    parser.add_argument(
        '--error', '-e',
        type=float,
        default=1.5,
        help='Error level for human-like variation in pixels (default: 1.5)'
    )
    
    parser.add_argument(
        '--distance', '-d',
        type=int,
        default=6,
        help='Distance between curves in pixels (default: 6)'
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
            args.segment_length,
            args.error,
            args.distance,
            args.canvas_size,
            args.output
        )
        print(f"Successfully generated {len(curves)} curves!")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main() 