# Experiment 02: Iterative Segment Generation

## Rules Implemented

### RULE 2
The algorithm adds segments iteratively.
- Create and draw OUTER_CURVE
- Set previous_curve = OUTER_CURVE
- Create new_closed_curve of segments inside previous_curve by keeping approximately DIST away

## Algorithm

### Main Process (`iterative_curve_generator.py`)
1. **Initialize**:
   - Load or create OUTER_CURVE from Experiment 01
   - Set previous_curve = OUTER_CURVE
   - Create canvas for combined visualization

2. **Iterative Generation**:
   - For each curve (1 to num_curves):
     - Call `create_next_closed_curve(previous_curve, dist)`
     - Draw new curve with different color
     - Save coordinates to individual file
     - Set previous_curve = new_curve for next iteration

3. **Output**:
   - `curves_sequence.png`: All curves drawn together
   - `curve_N_coordinates.txt`: Individual curve data files

### Segment Creation Algorithm (`segment_creator.py`)

**Input**: previous_curve, dist, error, segment_length

**Process**:
1. **Initialize**:
   - Calculate center of previous curve
   - Start with first point of previous curve
   - Calculate inward direction with random variation
   - Place first point at dist distance inward

2. **Iterative Segment Creation**:
   - For each point in previous curve:
     - Calculate inward direction from outer point
     - Add random variation (±error)
     - Calculate target point at dist distance
     - Place new segment point at segment_length toward target
     - Check for intersections with existing segments
     - If intersection found, retry with adjusted direction
     - Check if curve is closed (distance to start < threshold)

3. **Intersection Prevention**:
   - Check new segment against all existing segments in new curve
   - Check new segment against all segments in previous curve
   - Use CCW algorithm for intersection detection
   - Limit retry attempts to prevent infinite loops

4. **Termination Conditions**:
   - Curve successfully closes (distance to start < closure_threshold)
   - Maximum segments reached (safety limit)
   - Maximum retry attempts exceeded

**Output**: List of (x, y) coordinates forming closed curve

## Key Features

- **Non-intersecting**: All segments checked for intersections
- **Approximately dist away**: Target distance with small variations
- **Closed**: Always returns complete closed curve
- **Robust**: Handles edge cases and prevents infinite loops
- **Human-like error**: Random variations in segment direction

## Parameters

- `dist`: Target distance between curves (default: 50)
- `error`: Random variation in direction (default: 2.0)
- `segment_length`: Length of each segment (default: 3)
- `num_curves`: Number of curves to generate (default: 5)

## Files

- `code/iterative_curve_generator.py`: Main iterative process
- `code/segment_creator.py`: Segment creation algorithm
- `output/curves_sequence.png`: Combined visualization
- `output/curve_N_coordinates.txt`: Individual curve data

## Usage

```bash
cd experiments/experiment_02_iterative_segments/code
python iterative_curve_generator.py
```

## Dependencies

- PIL (Pillow) for image generation
- Shared utilities from `../shared/`
- Experiment 01 output for OUTER_CURVE 