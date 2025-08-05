#!/usr/bin/env python3
"""
Fast installation script for AtPoE (Admitting the Possibilities of Error).
Assumes dependencies are already available.
"""

import sys
import os
import subprocess
from pathlib import Path


def check_dependencies():
    """Quick check if core dependencies are available."""
    print("🔍 Checking dependencies...")
    
    deps = ["PIL", "numpy", "matplotlib"]
    missing = []
    
    for dep in deps:
        try:
            __import__(dep)
            print(f"✅ {dep} available")
        except ImportError:
            print(f"❌ {dep} missing")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Missing: {', '.join(missing)}")
        print("   Install with: pip install " + " ".join(missing))
        return False
    
    return True


def install_atpoe_fast():
    """Fast AtPoE installation - just install the package."""
    print("\n🎨 Installing AtPoE package...")
    
    if not Path("setup.py").exists():
        print("❌ setup.py not found. Run from AtPoE root directory.")
        return False
    
    try:
        # Quick development install
        result = subprocess.run(
            "pip install -e .", 
            shell=True, 
            capture_output=True, 
            text=True,
            timeout=60  # 1 minute timeout
        )
        
        if result.returncode == 0:
            print("✅ AtPoE installed successfully!")
            return True
        else:
            print(f"❌ Installation failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Installation timed out")
        return False
    except Exception as e:
        print(f"❌ Installation error: {e}")
        return False


def test_installation():
    """Quick test of AtPoE installation."""
    print("\n🧪 Testing installation...")
    
    try:
        # Test direct imports
        from atpoe.core.curve_generator import generate_initial_circle
        
        print("✅ Core modules imported successfully")
        
        # Quick functionality test
        curve = generate_initial_circle(1000, 450)
        print(f"✅ Curve generation works ({len(curve)} segments)")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def create_test_script():
    """Create a simple test script."""
    script = '''#!/usr/bin/env python3
"""
Quick AtPoE test script
"""

try:
    from atpoe.core.curve_generator import generate_initial_circle
    from PIL import Image, ImageDraw
    
    # Generate test curve
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
    image.save('atpoe_quick_test.png')
    print(f"✅ AtPoE test successful! Saved: atpoe_quick_test.png")
    print(f"   Generated {len(curve)} curve segments")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
'''
    
    with open("test_atpoe_quick.py", "w") as f:
        f.write(script)
    
    print("✅ Quick test script created: test_atpoe_quick.py")


def show_usage():
    """Show usage instructions."""
    print("\n🎯 AtPoE Fast Installation Complete!")
    print("=" * 40)
    
    print("\n📖 Quick Usage:")
    print("1. Test installation:")
    print("   python test_atpoe_quick.py")
    
    print("\n2. Command line:")
    print("   atpoe --curves 10 --length 15 --error 1.5")
    
    print("\n3. Python API:")
    print("   from atpoe.core.curve_generator import generate_initial_circle")
    print("   curve = generate_initial_circle(1000, 450)")


def main():
    """Main fast installation function."""
    print("🎨 AtPoE - Fast Installation")
    print("=" * 30)
    
    # Quick dependency check
    if not check_dependencies():
        print("\n❌ Dependencies missing. Install them first.")
        sys.exit(1)
    
    # Fast install
    if not install_atpoe_fast():
        print("\n❌ Installation failed.")
        sys.exit(1)
    
    # Quick test
    if not test_installation():
        print("\n❌ Installation test failed.")
        sys.exit(1)
    
    # Create test script
    create_test_script()
    
    # Show usage
    show_usage()


if __name__ == '__main__':
    main() 