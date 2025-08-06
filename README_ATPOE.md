# AtPoE - Admitting the Possibilities of Error

🎨 A closed curve generation and visualization system that embraces human-like variation and imperfection in mathematical art.

## Overview

AtPoE generates beautiful nested, non-crossing curves with controlled levels of "error" or irregularity, simulating the natural variation found in hand-drawn curves.

## Quick Start

### Installation

```bash
# Fast installation (assumes dependencies are available)
python install_atpoe_fast.py

# Or manual installation
pip install -r requirements.txt
pip install -e .
```

### Basic Usage

#### Command Line
```bash
# Generate 10 curves with default settings
atpoe --curves 10 --length 15 --error 1.5

# Generate 20 curves with custom parameters
atpoe --curves 20 --length 10 --error 2.4 --output my_curves.png
```

#### Python API
```python
from atpoe.core.curve_generator import generate_initial_circle, generate_nested_curve

# Generate initial circle
curve = generate_initial_circle(1000, 450)

# Generate nested curve
nested_curve = generate_nested_curve(curve, 15, 15, 1.5)
```

## Parameters

### Core Parameters
- **`num_curves`**: Number of nested curves to generate (1-100)
- **`length`**: Length of curve segments (5-30 pixels)
- **`error`**: Error level for human-like variation (0.1-5.0)
- **`canvas_size`**: Canvas size in pixels (500-2000)

### Error Level Guide
- **0.1-0.5**: Very smooth, almost perfect circles
- **0.5-1.0**: Slight human-like variation
- **1.0-2.0**: Moderate irregularity, natural hand-drawn effect
- **2.0-3.0**: Noticeable irregularity, organic appearance
- **3.0+**: Highly irregular, very rough curves

## Examples

### Basic Curve Generation
```python
from atpoe.core.curve_generator import generate_initial_circle
from PIL import Image, ImageDraw

# Generate curve
curve = generate_initial_circle(1000, 450)

# Create image
image = Image.new('RGB', (1000, 1000), 'white')
draw = ImageDraw.Draw(image)

# Draw curve
for j in range(len(curve)):
    p1 = curve[j]
    p2 = curve[(j + 1) % len(curve)]
    draw.line([p1, p2], fill='black', width=3)

# Save
image.save('my_curves.png')
```

## Testing

### Quick Test
```bash
python test_atpoe_quick.py
```

### Manual Test
```bash
# Test command line
atpoe --curves 5 --length 15 --error 1.5 --output test.png

# Test Python import
python -c "from atpoe.core.curve_generator import generate_initial_circle; print('AtPoE works!')"
```

## Dependencies

### Core Dependencies
- **Pillow>=9.0.0**: Image processing and drawing
- **numpy>=1.21.0**: Numerical computations
- **matplotlib>=3.5.0**: Plotting and visualization

### Optional Dependencies
- **streamlit>=1.20.0**: For GUI features
- **psutil>=5.8.0**: For performance monitoring

## Project Structure

```
atpoe/
├── __init__.py                    # Main package
├── cli.py                        # Command-line interface
├── core/                         # Core functionality
│   ├── __init__.py
│   └── curve_generator.py       # Main curve generation
├── graphics/                     # Visual styling
│   └── __init__.py
├── interactive/                  # Interactive mode
│   └── __init__.py
└── utils/                        # Utilities
    └── __init__.py
```

## Performance

AtPoE is optimized for performance:
- **Fast Generation**: Efficient curve generation algorithms
- **Memory Efficient**: Minimal overhead for large curve sets
- **Scalable**: Handles 100+ curves with 1000+ segments each

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

- **Documentation**: See this README
- **Issues**: Report on GitHub
- **Examples**: Check the test scripts

---

**AtPoE** - Where mathematical precision meets human creativity 🎨 