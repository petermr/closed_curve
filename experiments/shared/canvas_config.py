"""
Shared canvas configuration for experiments.
"""

# Canvas settings
CANVAS_SIZE = 1200  # Large enough for radius 500 circle centered at (500, 500)
BACKGROUND_COLOR = 'white'
CURVE_COLORS = ['black', 'blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink']
LINE_WIDTH = 2

# Default parameters
DEFAULT_RADIUS = 500
DEFAULT_CENTER_X = 500
DEFAULT_CENTER_Y = 500
DEFAULT_DIST = 6  # Distance between curves (increased by 50%)
DEFAULT_ERROR = 2.0  # Random variation in segment direction
DEFAULT_SEGMENT_LENGTH = 3  # Length of each segment

# Safety limits
MAX_SEGMENTS = 1000
MAX_RETRY_ATTEMPTS = 10
CLOSURE_THRESHOLD = 5.0  # Distance threshold for curve closure 