"""
Shared coordinate utilities for experiments.
"""

import math
import json
from pathlib import Path


def distance(p1, p2):
    """Calculate Euclidean distance between two points."""
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])


def calculate_center(curve):
    """Calculate the center point of a curve."""
    if not curve:
        return None
    center_x = sum(x for x, y in curve) / len(curve)
    center_y = sum(y for x, y in curve) / len(curve)
    return (center_x, center_y)


def inward_direction(point, center):
    """Calculate direction vector from point toward center."""
    dx = center[0] - point[0]
    dy = center[1] - point[1]
    dist = math.hypot(dx, dy) or 1.0
    return (dx / dist, dy / dist)


def segments_intersect(p1, p2, p3, p4):
    """Check if line segments (p1,p2) and (p3,p4) intersect using CCW algorithm."""
    def ccw(A, B, C):
        return (C[1] - A[1]) * (B[0] - A[0]) > (B[1] - A[1]) * (C[0] - A[0])
    
    return ccw(p1, p3, p4) != ccw(p2, p3, p4) and ccw(p1, p2, p3) != ccw(p1, p2, p4)


def save_coordinates(curve, filename):
    """Save curve coordinates to text file."""
    with open(filename, 'w') as f:
        for x, y in curve:
            f.write(f"{x},{y}\n")


def load_coordinates(filename):
    """Load curve coordinates from text file."""
    curve = []
    with open(filename, 'r') as f:
        for line in f:
            x, y = map(float, line.strip().split(','))
            curve.append((x, y))
    return curve


def is_curve_closed(curve, threshold=5.0):
    """Check if a curve is closed (start point close to end point)."""
    if len(curve) < 3:
        return False
    return distance(curve[0], curve[-1]) <= threshold 