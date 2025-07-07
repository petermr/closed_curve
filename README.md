# Closed Curve Generator

A Python application that generates visually appealing nested closed curves with human-like imperfections. This project explores the intersection of mathematics, art, and programming through algorithmic curve generation.

## 🎨 What It Does

This application creates beautiful nested geometric patterns that:
- Start with a perfect circle
- Generate inward-progressing curves with human-like imperfections
- Prevent any line crossings between curves
- Support up to 100 nested curves
- Use constant segment lengths with random variation

## 📁 Project Structure

```
closed_curve/
├── README.md                    # This file - main documentation
├── INSTALLATION.md              # Detailed installation instructions
├── USAGE_GUIDE.md               # How to use the application
├── EXAMPLES.md                  # Example parameters and results
├── step6_final_version.py       # Main application (latest version)
├── step6_summary.md             # Technical summary of Step 6
├── images/                      # Generated images
│   ├── step6_final_curves_*.png # PNG format images
│   └── step6_final_curves_*.svg # SVG format images
├── legacy/                      # Previous versions and experiments
└── docs/                        # Additional documentation
```

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation
1. **Clone or download** this project
2. **Install Python** (if not already installed):
   - macOS: `brew install python` or download from python.org
   - Windows: Download from python.org
   - Linux: `sudo apt-get install python3 python3-pip`

3. **Install required packages**:
   ```bash
   pip install streamlit pillow
   ```

### Running the Application
```bash
streamlit run step6_final_version.py
```

The application will open in your web browser at `http://localhost:8501`

## 🎯 Key Features

- **Interactive GUI**: Adjust parameters in real-time
- **Collision Detection**: Ensures no lines cross each other
- **Human-like Error**: Simulates hand-drawn imperfections
- **Multiple Outputs**: PNG and SVG formats
- **Color Coding**: Each curve has a distinct color
- **Scalable**: Up to 100 nested curves

## 📊 Parameters

- **Number of Curves**: 2-100 (how many nested curves to generate)
- **Segment Length**: 5-30 pixels (length of each line segment)
- **Human-like Error**: 0.0-5.0 pixels (random variation amount)
- **Offset Distance**: 5-30 pixels (space between curves)

## 🖼️ Example Results

The application generates images like:
- Concentric patterns with organic variations
- Color-coded nested curves
- Both PNG (raster) and SVG (vector) formats
- High-resolution output suitable for printing

## 📚 Documentation

- **[INSTALLATION.md](INSTALLATION.md)** - Detailed setup instructions
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - How to use the application
- **[EXAMPLES.md](EXAMPLES.md)** - Example parameters and results
- **[step6_summary.md](step6_summary.md)** - Technical implementation details

## 🎨 Artistic Value

This project creates algorithmic art that:
- Explores the relationship between order and chaos
- Creates meditative, mandala-like patterns
- Demonstrates mathematical beauty through code
- Generates unique, one-of-a-kind compositions

## 🔧 Technical Details

- **Language**: Python 3
- **Main Libraries**: Streamlit (GUI), Pillow (image generation)
- **Algorithm**: Collision detection with inward progression
- **Output**: PNG and SVG formats
- **Canvas**: 1000x1000 pixels

## 🤝 Contributing

Feel free to experiment with the code! You can:
- Modify the color schemes
- Adjust the collision detection algorithms
- Add new geometric patterns
- Create animations or variations

## 📄 License

This project is open source. Feel free to use, modify, and distribute.

---

**Created by**: Closed Curve Generator Project  
**Latest Version**: Step 6  
**Last Updated**: July 2024
