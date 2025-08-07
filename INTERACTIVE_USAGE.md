# Interactive AtPoE Usage Guide

## Overview

The Interactive AtPoE (Admitting the Possibilities of Error) allows you to generate curves in batches, see the results after each batch, and adjust parameters before continuing. This is perfect for iterative design and experimentation.

## Quick Start

### 1. Run the Interactive Session
```bash
python atpoe_interactive.py
```

### 2. Default Parameters
The session starts with these default parameters:
- **Curves per batch**: 3
- **Segment length**: 12px
- **Error level**: 1.5px
- **Distance between curves**: 8px
- **Target total curves**: 15
- **Canvas size**: 1000x1000px

## How It Works

### Batch Generation
1. **Generate**: Creates a small batch of curves (default: 3 curves)
2. **Display**: Shows the current image and status
3. **Save**: Automatically saves the image to `interactive_atpoe_output/`
4. **Choose**: You decide what to do next

### After Each Batch, You Can:
1. **Continue** with current parameters
2. **Adjust parameters** for the next batch
3. **Save and exit** to finish

## Parameter Adjustment

When you choose to adjust parameters, you can modify:

### Curves per Batch
- **Range**: 1-10 recommended
- **Effect**: More curves per batch = faster progress, less control
- **Tip**: Start with 3-5 for good control

### Segment Length
- **Range**: 5-30px
- **Effect**: 
  - Shorter = smoother, more detailed curves
  - Longer = more angular, geometric appearance
- **Tip**: 10-15px gives a good balance

### Error Level
- **Range**: 0.0-5.0px
- **Effect**:
  - 0.0 = perfect geometric curves
  - 1.0-2.0 = subtle human-like imperfections
  - 3.0+ = more organic, hand-drawn appearance
- **Tip**: 1.0-2.0 gives realistic hand-drawn feel

### Distance Between Curves
- **Range**: 5-30px
- **Effect**:
  - Smaller values = curves closer together (dense patterns)
  - Larger values = curves further apart (sparse patterns)
- **Tip**: 8-15px works well for most cases

### Target Total Curves
- **Range**: 5-100
- **Effect**: Total number of curves to generate
- **Tip**: Start with 15-20 for experimentation

## Example Workflow

### Session 1: Simple Start
```
Batch 1: 3 curves (default parameters)
→ Continue with current parameters

Batch 2: 3 more curves
→ Adjust: Increase error to 2.0, decrease distance to 6

Batch 3: 3 curves with new parameters
→ Continue with current parameters

Batch 4: 3 curves
→ Adjust: Increase segment length to 15

Batch 5: 3 curves with longer segments
→ Save and exit
```

### Session 2: Complex Design
```
Batch 1: 5 curves (increase batch size)
→ Continue

Batch 2: 5 curves
→ Adjust: Decrease error to 0.8, increase distance to 12

Batch 3: 5 curves with precise parameters
→ Continue

Batch 4: 5 curves
→ Save and exit (20 curves total)
```

## File Output

### Automatic Saving
- **Location**: `interactive_atpoe_output/` directory
- **Naming**: `atpoe_interactive_[number]_curves.png`
- **Format**: PNG with color-coded curves

### Example Files
```
interactive_atpoe_output/
├── atpoe_interactive_3_curves.png
├── atpoe_interactive_6_curves.png
├── atpoe_interactive_9_curves.png
└── atpoe_interactive_12_curves.png
```

## Tips for Best Results

### 1. Start Simple
- Begin with default parameters
- Generate 2-3 batches to see the pattern
- Then start adjusting

### 2. Change One Thing at a Time
- Adjust only one parameter per batch
- See how it affects the result
- Build up complexity gradually

### 3. Use Small Batches
- 3-5 curves per batch gives good control
- You can see changes more clearly
- Easier to experiment

### 4. Save Often
- Images are automatically saved
- You can always go back to previous results
- Compare different parameter combinations

### 5. Experiment with Extremes
- Try very high error (4.0+) for organic feel
- Try very low error (0.1) for precision
- Try very small distance (3-4) for dense patterns
- Try very large distance (20+) for sparse patterns

## Advanced Usage

### Custom Canvas Size
```bash
python atpoe_interactive.py --canvas-size 1200
```

### Demo Mode
To see how it works without interaction:
```bash
python atpoe_interactive_demo.py
```

### Parameter Ranges to Try

#### Geometric Precision
- Error: 0.1-0.5
- Segment length: 20-30
- Distance: 10-15

#### Hand-drawn Feel
- Error: 2.0-3.0
- Segment length: 8-12
- Distance: 6-10

#### Organic Complexity
- Error: 3.0-4.0
- Segment length: 5-8
- Distance: 4-6

#### Simple Clean
- Error: 0.5-1.0
- Segment length: 15-20
- Distance: 12-18

## Troubleshooting

### Common Issues

**"Module not found" errors**
- Make sure you're in the project directory
- Install required packages: `pip install pillow`

**"Canvas too small"**
- Use `--canvas-size 1200` for larger canvas
- Reduce target total curves

**"Curves too dense"**
- Increase distance between curves
- Reduce number of curves per batch

**"Curves too sparse"**
- Decrease distance between curves
- Increase number of curves per batch

### Keyboard Interrupt
- Press `Ctrl+C` to exit at any time
- Current image will be saved automatically

## Next Steps

After mastering the interactive version:

1. **Try the regular CLI**: `python -m atpoe.cli --help`
2. **Explore the Streamlit app**: `streamlit run step6_final_version.py`
3. **Experiment with different algorithms** in the experiments directory
4. **Create your own parameter combinations** and share them

Happy curve generating! 🎨
