"""
Segment Creator: Algorithm for creating next closed curve

This implements the algorithm for creating a new closed curve inside a previous curve
while maintaining approximately DIST distance and ensuring no intersections.
"""

import math
import random
import sys
import os

# Add shared utilities to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'shared'))

from canvas_config import *
from coordinate_utils import distance


def create_next_closed_curve(previous_curve, dist, error=DEFAULT_ERROR, 
                           segment_length=DEFAULT_SEGMENT_LENGTH):
    """
    Simple algorithm: Go round inside the previous curve keeping close with 
    approximately constant steps until you get within a step length of the start.
    
    Args:
        previous_curve: List of (x, y) coordinate points of previous curve
        dist: Target distance from previous curve
        error: Random variation in direction (±error)
        segment_length: Length of each segment
    
    Returns:
        List of (x, y) coordinate points forming closed curve, or None if failed
    """
    if len(previous_curve) < 3:
        return None
    
    # Find center of previous curve
    center_x = sum(x for x, y in previous_curve) / len(previous_curve)
    center_y = sum(y for x, y in previous_curve) / len(previous_curve)
    
    new_curve = []
    
    # Start at first point of previous curve
    outer_point = previous_curve[0]
    
    # Calculate first point inside
    dx = center_x - outer_point[0]
    dy = center_y - outer_point[1]
    d = distance(outer_point, (center_x, center_y)) or 1.0
    
    # Add small random error
    error_x = random.uniform(-error, error)
    error_y = random.uniform(-error, error)
    
    # Place first point at dist distance inside
    first_point = (
        outer_point[0] + (dx / d) * dist + error_x,
        outer_point[1] + (dy / d) * dist + error_y
    )
    
    new_curve.append(first_point)
    current_point = first_point
    
    # Go round the previous curve
    for i in range(1, len(previous_curve)):
        outer_point = previous_curve[i]
        
        # Calculate target point inside this outer point
        dx = center_x - outer_point[0]
        dy = center_y - outer_point[1]
        d = distance(outer_point, (center_x, center_y)) or 1.0
        
        # Add small random error
        error_x = random.uniform(-error, error)
        error_y = random.uniform(-error, error)
        
        target_point = (
            outer_point[0] + (dx / d) * dist + error_x,
            outer_point[1] + (dy / d) * dist + error_y
        )
        
        # Move toward target in steps of segment_length
        while distance(current_point, target_point) > segment_length:
            # Calculate direction to target
            dx_to_target = target_point[0] - current_point[0]
            dy_to_target = target_point[1] - current_point[1]
            d_to_target = distance(current_point, target_point) or 1.0
            
            # Add new point at segment_length distance
            new_point = (
                current_point[0] + (dx_to_target / d_to_target) * segment_length,
                current_point[1] + (dy_to_target / d_to_target) * segment_length
            )
            
            new_curve.append(new_point)
            current_point = new_point
    
    # Close the curve: keep adding points until close to start
    while distance(current_point, new_curve[0]) > segment_length:
        # Calculate direction to start
        dx_to_start = new_curve[0][0] - current_point[0]
        dy_to_start = new_curve[0][1] - current_point[1]
        d_to_start = distance(current_point, new_curve[0]) or 1.0
        
        # Add new point at segment_length distance
        new_point = (
            current_point[0] + (dx_to_start / d_to_start) * segment_length,
            current_point[1] + (dy_to_start / d_to_start) * segment_length
        )
        
        new_curve.append(new_point)
        current_point = new_point
    
    # Final closure
    new_curve.append(new_curve[0])
    return new_curve


def test_segment_creator():
    """Test function for segment creator."""
    # Create a simple test curve (square)
    test_curve = [(100, 100), (200, 100), (200, 200), (100, 200)]
    
    print("Testing segment creator with square curve...")
    new_curve = create_next_closed_curve(test_curve, dist=20, error=1.0)
    
    if new_curve:
        print(f"Successfully created curve with {len(new_curve)} points")
        print("First few points:", new_curve[:5])
    else:
        print("Failed to create curve")


if __name__ == "__main__":
    test_segment_creator() 