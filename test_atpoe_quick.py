#!/usr/bin/env python3
"""
Quick AtPoE test script
"""

try:
    from atpoe.core.curve_generator import generate_initial_circle, generate_nested_curve
    from PIL import Image, ImageDraw
    
    # Generate multiple nested curves
    canvas_size = 1000
    curves = []
    
    # Generate initial circle
    curve = generate_initial_circle(canvas_size, 450)
    curves.append(curve)
    
    # Generate nested curves
    for i in range(4):  # Generate 4 more curves (5 total)
        new_curve = generate_nested_curve(curves[-1], 15, 2.4)
        if new_curve:
            curves.append(new_curve)
    
    # Create image
    image = Image.new('RGB', (canvas_size, canvas_size), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw all curves with different colors
    colors = ['black', 'blue', 'red', 'green', 'purple']
    for i, curve in enumerate(curves):
        color = colors[i % len(colors)]
        for j in range(len(curve)):
            p1 = curve[j]
            p2 = curve[(j + 1) % len(curve)]
            draw.line([p1, p2], fill=color, width=2)
    
    # Save
    image.save('atpoe_quick_test.png')
    print(f"✅ AtPoE test successful! Saved: atpoe_quick_test.png")
    print(f"   Generated {len(curves)} curves:")
    for i, curve in enumerate(curves):
        print(f"     Curve {i+1}: {len(curve)} segments")
    
except Exception as e:
    print(f"❌ Test failed: {e}")
