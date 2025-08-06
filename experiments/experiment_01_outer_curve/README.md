# Experiment 01: Draw OUTER_CURVE

## Rules Implemented

### RULE 0
There is a universe with an outer closed curve OUTER_CURVE. The user will tell you what the curve is and where it is located (USER_INPUT).

### RULE 1
You will draw OUTER_CURVE and remember its coordinates. You will forget its form and its centre.

## User Input
Currently it is a circle with radius R=500. The user will set the centre at (R, R). You will draw this curve and then forget that it is a circle or where the center is. This will be called OUTER_CURVE.

## Algorithm

1. **Input Parameters**:
   - Radius: 500 pixels
   - Center: (500, 500)
   - Canvas size: 1200x1200 pixels
   - Segment length: 3 pixels

2. **Process**:
   - Generate circle points using parametric equations
   - Calculate number of points: `2π × radius / segment_length`
   - Draw line segments between consecutive points
   - Save coordinates to text file
   - Save visual output as PNG

3. **Output**:
   - `outer_curve.png`: Visual representation
   - `outer_curve_coordinates.txt`: List of (x, y) coordinates
   - Return coordinate list as OUTER_CURVE

4. **Memory State**:
   - After drawing, forget that it was a circle
   - Forget where the center was located
   - Remember only the coordinate list

## Files

- `code/draw_outer_curve.py`: Main implementation
- `output/outer_curve.png`: Visual output
- `output/outer_curve_coordinates.txt`: Coordinate data

## Usage

```bash
cd experiments/experiment_01_outer_curve/code
python draw_outer_curve.py
```

## Dependencies

- PIL (Pillow) for image generation
- Shared utilities from `../shared/` 