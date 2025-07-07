# Quick Reference Card

## 🚀 Get Started in 3 Steps

1. **Install Python** (if not already installed)
2. **Install packages**: `pip install streamlit pillow`
3. **Run app**: `streamlit run step6_final_version.py`

## 🎛️ Parameter Quick Guide

| Parameter | Range | Default | Effect |
|-----------|-------|---------|---------|
| **Number of Curves** | 2-100 | 10 | More = more complex |
| **Segment Length** | 5-30 | 15 | Shorter = smoother |
| **Human-like Error** | 0.0-5.0 | 1.5 | Higher = more organic |
| **Offset Distance** | 5-30 | 15 | Smaller = denser |

## 🎯 Quick Settings

### Simple Start
```
Curves: 8, Length: 20, Error: 0.5, Offset: 20
```

### Hand-drawn Feel
```
Curves: 15, Length: 12, Error: 2.5, Offset: 12
```

### Complex Detail
```
Curves: 30, Length: 8, Error: 1.0, Offset: 8
```

### Geometric Precision
```
Curves: 20, Length: 25, Error: 0.0, Offset: 15
```

## 📁 File Locations

- **Main App**: `step6_final_version.py`
- **Images**: `images/` folder
- **Documentation**: `README.md`, `USAGE_GUIDE.md`, `EXAMPLES.md`

## 🎨 What You'll See

- **Black circle** (starting point)
- **Colored nested curves** (each curve inside the previous)
- **No line crossings** (mathematically impossible)
- **Human-like variations** (simulated hand-drawing)

## 💾 Saving Images

- **PNG**: For digital use, web sharing
- **SVG**: For printing, scaling
- **Auto-save**: Images saved to `images/` folder
- **Naming**: `step6_final_curves_[curves]_len[length]_error[error].png`

## 🔧 Troubleshooting

| Problem | Solution |
|---------|----------|
| "Python not found" | Install Python from python.org |
| "Module not found" | Run `pip install streamlit pillow` |
| "Port in use" | Use `--server.port 8502` |
| "Can't save" | Check `images/` folder exists |

## 🎯 Tips

- **Start simple**: Use 5-10 curves first
- **Change one thing**: Adjust one parameter at a time
- **Experiment freely**: There are no wrong answers!
- **Save favorites**: Note down combinations you like

## 📞 Need Help?

1. Check [INSTALLATION.md](INSTALLATION.md) for setup
2. Read [USAGE_GUIDE.md](USAGE_GUIDE.md) for details
3. Try [EXAMPLES.md](EXAMPLES.md) for inspiration
4. Look at [PROJECT_OVERVIEW.md](PROJECT_OVERVIEW.md) for context

---

**Happy Creating!** 🎨✨ 