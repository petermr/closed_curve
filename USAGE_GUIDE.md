# Usage Guide

This guide will teach you how to use the Closed Curve Generator application effectively.

## 🚀 Starting the Application

1. **Open Terminal/Command Prompt**
2. **Navigate to the project folder**:
   ```bash
   cd /path/to/closed_curve
   ```
3. **Start the application**:
   ```bash
   streamlit run step6_final_version.py
   ```
4. **Open your web browser** to `http://localhost:8501`

## 🎛️ Understanding the Interface

The application has a **sidebar** on the left with controls and a **main area** on the right for the image.

### Sidebar Controls

#### 1. Number of Curves (2-100)
- **What it does**: Controls how many nested curves to generate
- **Default**: 10
- **Effect**: More curves = more complex, detailed patterns
- **Tip**: Start with 10-20 for quick results, use 50+ for detailed patterns

#### 2. Segment Length (5-30 pixels)
- **What it does**: Length of each straight line segment
- **Default**: 15 pixels
- **Effect**: 
  - Shorter segments = smoother, more detailed curves
  - Longer segments = more angular, geometric appearance
- **Tip**: 10-15 pixels gives a good balance

#### 3. Human-like Error (0.0-5.0 pixels)
- **What it does**: Amount of random variation to simulate hand-drawing
- **Default**: 1.5 pixels
- **Effect**:
  - 0.0 = perfect geometric curves
  - 1.0-2.0 = subtle human-like imperfections
  - 3.0+ = more organic, hand-drawn appearance
- **Tip**: 1.0-2.0 gives realistic hand-drawn feel

#### 4. Offset Distance (5-30 pixels)
- **What it does**: Space between consecutive curves
- **Default**: 15 pixels
- **Effect**:
  - Smaller values = curves closer together (dense patterns)
  - Larger values = curves further apart (sparse patterns)
- **Tip**: 10-20 pixels works well for most cases

### Main Area
- **Current Settings**: Shows your current parameter values
- **Generate Button**: Click to create new curves
- **Image Display**: Shows the generated pattern
- **Download Buttons**: Save PNG and SVG versions

## 🎨 How to Use the Application

### Step 1: Start with Default Settings
1. Open the application
2. Click "Generate Final Nested Curves"
3. Observe the result - you should see a black circle with colored nested curves

### Step 2: Experiment with Parameters
1. **Adjust Number of Curves**:
   - Try 5 curves for a simple pattern
   - Try 20 curves for more detail
   - Try 50+ curves for complex patterns

2. **Play with Segment Length**:
   - Set to 10 for smoother curves
   - Set to 25 for more angular appearance

3. **Experiment with Human-like Error**:
   - Set to 0.0 for perfect geometric curves
   - Set to 2.0 for realistic hand-drawn feel
   - Set to 4.0 for very organic appearance

4. **Adjust Offset Distance**:
   - Set to 10 for tight, dense patterns
   - Set to 25 for loose, spacious patterns

### Step 3: Generate and Observe
- Click "Generate Final Nested Curves" after each parameter change
- Notice how each parameter affects the final result
- Take time to appreciate the mathematical beauty!

### Step 4: Save Your Creations
- Use the "Download PNG" button for raster images
- Use the "Download SVG" button for vector images (scalable)
- Images are automatically saved to the `images/` folder

## 🎯 Parameter Combinations to Try

### Simple and Clean
- Number of Curves: 8
- Segment Length: 20
- Human-like Error: 0.5
- Offset Distance: 20

### Organic and Natural
- Number of Curves: 15
- Segment Length: 12
- Human-like Error: 2.5
- Offset Distance: 12

### Complex and Detailed
- Number of Curves: 30
- Segment Length: 8
- Human-like Error: 1.0
- Offset Distance: 8

### Geometric and Precise
- Number of Curves: 20
- Segment Length: 25
- Human-like Error: 0.0
- Offset Distance: 15

### Hand-drawn Feel
- Number of Curves: 12
- Segment Length: 15
- Human-like Error: 3.0
- Offset Distance: 18

## 🔍 Understanding the Results

### What You're Seeing
1. **Black Circle**: The starting point (perfect circle, radius 450)
2. **Colored Curves**: Each subsequent curve has a different color
3. **Nested Pattern**: Each curve is inside the previous one
4. **No Crossings**: Lines never intersect (thanks to collision detection)

### Color Progression
- Curve 1: Black (starting circle)
- Curve 2: Red
- Curve 3: Blue
- Curve 4: Green
- And so on through a predefined color palette

### File Naming
Generated files are named like:
```
step6_final_curves_15_len12_error2.5.png
```
This means:
- 15 curves
- 12-pixel segment length
- 2.5-pixel human-like error

## 💡 Tips and Tricks

### For Beginners
1. **Start Simple**: Use 5-10 curves with default settings
2. **Change One Thing at a Time**: This helps you understand each parameter
3. **Take Notes**: Write down combinations you like
4. **Experiment Freely**: There are no wrong answers!

### For Advanced Users
1. **Fine-tune Parameters**: Small changes can have big effects
2. **Create Series**: Generate multiple images with slight variations
3. **Use SVG for Printing**: Vector format scales perfectly
4. **Combine Parameters**: Try unusual combinations for unique results

### Performance Tips
1. **Fewer Curves = Faster**: 10-20 curves generate quickly
2. **More Curves = Slower**: 50+ curves may take a few seconds
3. **Close Other Apps**: Free up memory for complex patterns
4. **Be Patient**: Complex patterns are worth the wait!

## 🎨 Artistic Considerations

### Composition
- The patterns naturally draw the eye inward
- Each curve adds depth and complexity
- The color progression creates visual flow

### Use Cases
- **Wall Art**: Print large versions for decoration
- **Digital Art**: Use in graphic design projects
- **Meditation**: The patterns can be calming and meditative
- **Mathematical Education**: Demonstrates geometric concepts

### Customization Ideas
- Print multiple versions with different parameters
- Frame your favorites
- Use as backgrounds for other artwork
- Create a series exploring different parameter ranges

## 🔧 Troubleshooting

### Common Issues

**"Generate" button doesn't work**
- Make sure all parameters are set to valid values
- Try refreshing the page
- Check that Python and packages are installed correctly

**Images look wrong**
- Try different parameter combinations
- Make sure human-like error isn't too high
- Check that offset distance isn't too small

**Application is slow**
- Reduce the number of curves
- Close other applications
- Try simpler parameter combinations

**Can't download images**
- Check that the `images/` folder exists
- Make sure you have write permissions
- Try refreshing the page

## 📚 Next Steps

Once you're comfortable with the basics:
1. Read [EXAMPLES.md](EXAMPLES.md) for more parameter combinations
2. Experiment with creating your own parameter sets
3. Try generating a series of related images
4. Share your favorite creations!

Remember: The goal is to have fun and create beautiful patterns. There are no rules - just explore and enjoy the mathematical art you're creating! 