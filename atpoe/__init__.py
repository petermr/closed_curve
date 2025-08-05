"""
AtPoE - Admitting the Possibilities of Error

A closed curve generation and visualization system that embraces human-like
variation and imperfection in mathematical art.

This package provides tools for generating nested, non-crossing curves with
controlled levels of "error" or irregularity, simulating the natural variation
found in hand-drawn curves.
"""

__version__ = "1.0.0"
__author__ = "Closed Curve Team"
__email__ = "team@atpoe.org"

# Package metadata only - no executable code
__all__ = [
    "generate_nested_curve",
    "generate_initial_circle", 
    "IncrementalCollisionDetector",
    "GraphicsBundle",
    "BundleLibrary", 
    "StrokeStyle",
    "InteractiveCurveDrawer",
] 