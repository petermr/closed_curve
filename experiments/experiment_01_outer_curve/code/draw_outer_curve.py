"""
Experiment 01: Draw OUTER_CURVE

RULE 0: There is a universe with an outer closed curve OUTER_CURVE.
        The user will tell you what the curve is and where it is located (USER_INPUT).

RULE 1: You will draw OUTER_CURVE and remember its coordinates. 
        You will forget its form and its centre.

USER INPUT: Currently it is a circle with radius R=500. 
           The user will set the centre at (R, R). 
           You will draw this curve and then forget that it is a circle or where the center is.
           This will be called OUTER_CURVE.
"""

import math
import sys
import os
from pathlib import Path

# Add shared utilities to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from canvas_config import *
from coordinate_utils import save_coordinates
from PIL import Image, ImageDraw


def draw_outer_curve(radius=DEFAULT_RADIUS, center_x=DEFAULT_CENTER_X, 
                    center_y=DEFAULT_CENTER_Y, canvas_size=CANVAS_SIZE, 
                    output_file=None):
    """
    Draw OUTER_CURVE and return its coordinates.
    
    Args:
        radius: Circle radius (default: 500)
        center_x: Center X coordinate (default: 500)
        center_y: Center Y coordinate (default: 500)
        canvas_size: Canvas size in pixels
        output_file: Output file path for image
    
    Returns:
        List of (x, y) coordinate tuples representing OUTER_CURVE
    """
    # Create canvas
    image = Image.new('RGB', (canvas_size, canvas_size), BACKGROUND_COLOR)
    draw = ImageDraw.Draw(image)
    
    # Generate circle points
    outer_curve = []
    num_points = int(2 * math.pi * radius / DEFAULT_SEGMENT_LENGTH)
    
    for i in range(num_points):
        angle = 2 * math.pi * i / num_points
        x = center_x + radius * math.cos(angle)
        y = center_y + radius * math.sin(angle)
        outer_curve.append((x, y))
    
    # Draw the curve
    for i in range(len(outer_curve)):
        p1 = outer_curve[i]
        p2 = outer_curve[(i + 1) % len(outer_curve)]
        draw.line([p1, p2], fill=CURVE_COLORS[0], width=LINE_WIDTH)
    
    # Save image
    if output_file:
        image.save(output_file)
        print(f"OUTER_CURVE saved to: {output_file}")
    
    # Save coordinates
    coords_file = output_file.replace('.png', '_coordinates.txt') if output_file else 'outer_curve_coordinates.txt'
    save_coordinates(outer_curve, coords_file)
    print(f"OUTER_CURVE coordinates saved to: {coords_file}")
    
    print(f"Generated OUTER_CURVE with {len(outer_curve)} points")
    print("RULE 1: Forgetting that this was a circle and where the center was.")
    
    return outer_curve


def main():
    """Main function for experiment 01."""
    output_dir = Path(__file__).parent.parent / 'output'
    output_dir.mkdir(exist_ok=True)
    
    output_file = output_dir / 'outer_curve.png'
    
    # Create OUTER_CURVE according to USER INPUT
    outer_curve = draw_outer_curve(
        radius=500,
        center_x=500,
        center_y=500,
        canvas_size=1200,
        output_file=str(output_file)
    )
    
    return outer_curve


if __name__ == "__main__":
    main() 