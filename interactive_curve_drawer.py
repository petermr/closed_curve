"""
Interactive Curve Drawing System with Graphics Bundles.
Allows drawing curves in batches with different visual styles and error levels.
"""

import sys
import os
import time
from typing import List, Tuple, Optional, Dict
from PIL import Image, ImageDraw
import json

# Import our systems
from graphics_bundle import BundleLibrary, BundleSelector, GraphicsBundle
from collision_detector import IncrementalCollisionDetector

# Import step5 functions
sys.path.append('experiments/step5_correct_approach')
from step5_correct_approach import generate_nested_curve, generate_initial_circle, draw_curves


class InteractiveCurveDrawer:
    """Interactive system for drawing curves with graphics bundles."""
    
    def __init__(self, canvas_size: int = 1000):
        self.canvas_size = canvas_size
        self.bundle_library = BundleLibrary()
        self.bundle_selector = BundleSelector(self.bundle_library)
        self.collision_detector = IncrementalCollisionDetector()
        self.all_curves = []
        self.current_image = None
        self.output_dir = "interactive_output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Drawing state
        self.current_bundle = None
        self.current_error = 1.5
        self.curve_count = 0
        self.batch_count = 0
    
    def initialize_canvas(self):
        """Initialize the drawing canvas."""
        self.current_image = Image.new('RGB', (self.canvas_size, self.canvas_size), 'white')
        print(f"Canvas initialized: {self.canvas_size}x{self.canvas_size} pixels")
    
    def select_graphics_bundle(self) -> Optional[GraphicsBundle]:
        """Let user select a graphics bundle."""
        print(f"\n{'='*60}")
        print("SELECT GRAPHICS BUNDLE")
        print(f"{'='*60}")
        
        bundle = self.bundle_selector.select_bundle()
        
        if bundle:
            self.current_bundle = bundle
            print(f"Selected bundle: {bundle.name}")
            print(f"  Style: {bundle.stroke_style.value}")
            print(f"  Width: {bundle.width}")
            print(f"  Color: {bundle.color}")
        
        return bundle
    
    def set_error_level(self) -> float:
        """Let user set the error level for curve generation."""
        print(f"\n{'='*60}")
        print("SET ERROR LEVEL")
        print(f"{'='*60}")
        print("Error level controls the 'human-like' variation in curves.")
        print("Higher values create more irregular curves.")
        print("Recommended range: 0.5 - 5.0")
        
        while True:
            try:
                error_input = input(f"\nEnter error level (current: {self.current_error}): ").strip()
                
                if not error_input:
                    return self.current_error
                
                error = float(error_input)
                if 0.0 <= error <= 10.0:
                    self.current_error = error
                    print(f"Error level set to: {error}")
                    return error
                else:
                    print("Please enter a value between 0.0 and 10.0")
                    
            except ValueError:
                print("Please enter a valid number")
    
    def draw_curves_with_bundle(self, num_curves: int, bundle: GraphicsBundle, error: float) -> List[List[Tuple[float, float]]]:
        """Draw a batch of curves with the specified graphics bundle."""
        print(f"\nDrawing {num_curves} curves with bundle '{bundle.name}' and error {error}")
        
        curves_batch = []
        segment_length = 15  # Fixed for now
        
        for i in range(num_curves):
            if self.curve_count == 0:
                # First curve - generate initial circle
                curve = generate_initial_circle(self.canvas_size, 450)
            else:
                # Generate nested curve
                curve = generate_nested_curve(self.all_curves[-1], segment_length, 15, error)
            
            # Check for collisions
            if self.collision_detector.add_curve(curve):
                print(f"Collision detected at curve {self.curve_count + 1}, stopping batch")
                break
            
            curves_batch.append(curve)
            self.all_curves.append(curve)
            self.curve_count += 1
            
            print(f"  Drew curve {self.curve_count} ({len(curve)} segments)")
        
        return curves_batch
    
    def draw_curves_on_canvas(self, curves: List[List[Tuple[float, float]]], bundle: GraphicsBundle):
        """Draw curves on the canvas with the specified graphics bundle."""
        if not curves:
            return
        
        draw = ImageDraw.Draw(self.current_image)
        
        for curve in curves:
            # Draw curve segments
            for i in range(len(curve)):
                p1 = curve[i]
                p2 = curve[(i + 1) % len(curve)]
                
                # Apply graphics bundle
                if bundle.dash_pattern:
                    # For now, use solid lines (PIL doesn't support dashed lines directly)
                    draw.line([p1, p2], fill=bundle.color, width=int(bundle.width))
                else:
                    # Solid line
                    draw.line([p1, p2], fill=bundle.color, width=int(bundle.width))
    
    def save_current_image(self, batch_name: str = None):
        """Save the current canvas to a file."""
        if batch_name is None:
            batch_name = f"batch_{self.batch_count:03d}"
        
        filename = os.path.join(self.output_dir, f"{batch_name}.png")
        self.current_image.save(filename)
        print(f"Image saved: {filename}")
        return filename
    
    def display_current_status(self):
        """Display current drawing status."""
        print(f"\n{'='*60}")
        print("CURRENT STATUS")
        print(f"{'='*60}")
        print(f"Total curves drawn: {self.curve_count}")
        print(f"Total batches: {self.batch_count}")
        print(f"Current bundle: {self.current_bundle.name if self.current_bundle else 'None'}")
        print(f"Current error: {self.current_error}")
        print(f"Canvas size: {self.canvas_size}x{self.canvas_size}")
        print(f"Output directory: {self.output_dir}")
        print(f"{'='*60}")
    
    def run_interactive_session(self):
        """Run the main interactive drawing session."""
        print("Interactive Curve Drawing System")
        print("="*50)
        print("This system allows you to draw curves in batches with different")
        print("graphics styles and error levels. You can interrupt and change")
        print("parameters between batches.")
        
        # Initialize canvas
        self.initialize_canvas()
        
        while True:
            print(f"\n{'='*60}")
            print("INTERACTIVE DRAWING MENU")
            print(f"{'='*60}")
            print("1. Select graphics bundle")
            print("2. Set error level")
            print("3. Draw batch of curves")
            print("4. Create custom bundle")
            print("5. Display current status")
            print("6. Save current image")
            print("7. Start new canvas")
            print("8. Quit")
            print(f"{'='*60}")
            
            choice = input("\nEnter your choice (1-8): ").strip()
            
            if choice == '1':
                self.select_graphics_bundle()
                
            elif choice == '2':
                self.set_error_level()
                
            elif choice == '3':
                if not self.current_bundle:
                    print("Please select a graphics bundle first (option 1)")
                    continue
                
                try:
                    num_curves = int(input("Number of curves to draw: ").strip())
                    if num_curves <= 0:
                        print("Please enter a positive number")
                        continue
                except ValueError:
                    print("Please enter a valid number")
                    continue
                
                # Draw the batch
                curves_batch = self.draw_curves_with_bundle(num_curves, self.current_bundle, self.current_error)
                self.draw_curves_on_canvas(curves_batch, self.current_bundle)
                self.batch_count += 1
                
                # Auto-save
                self.save_current_image(f"batch_{self.batch_count:03d}_{self.current_bundle.name.replace(' ', '_')}")
                
                print(f"\nBatch complete! Drew {len(curves_batch)} curves.")
                
            elif choice == '4':
                custom_bundle = self.bundle_selector.create_custom_bundle_interactive()
                if custom_bundle:
                    self.current_bundle = custom_bundle
                    print(f"Using custom bundle: {custom_bundle.name}")
                
            elif choice == '5':
                self.display_current_status()
                
            elif choice == '6':
                filename = input("Enter filename (or press Enter for auto-name): ").strip()
                if not filename:
                    filename = f"interactive_drawing_{int(time.time())}"
                self.save_current_image(filename)
                
            elif choice == '7':
                confirm = input("Start new canvas? This will clear the current drawing. (y/N): ").strip().lower()
                if confirm == 'y':
                    self.initialize_canvas()
                    self.all_curves = []
                    self.curve_count = 0
                    self.batch_count = 0
                    print("New canvas started!")
                
            elif choice == '8':
                print("\nSaving final image...")
                self.save_current_image("final_interactive_drawing")
                print("Interactive session ended.")
                break
                
            else:
                print("Please enter a valid choice (1-8)")
    
    def run_automated_demo(self):
        """Run an automated demo showing different bundles and error levels."""
        print("Running automated demo...")
        
        self.initialize_canvas()
        
        # Demo parameters
        demo_configs = [
            {"bundle_name": "Classic Black", "error": 1.0, "curves": 3},
            {"bundle_name": "Classic Red", "error": 2.0, "curves": 3},
            {"bundle_name": "Dashed Green", "error": 1.5, "curves": 3},
            {"bundle_name": "Bold Orange", "error": 3.0, "curves": 3},
            {"bundle_name": "Dotted Purple", "error": 0.8, "curves": 3},
        ]
        
        for i, config in enumerate(demo_configs):
            print(f"\nDemo batch {i+1}: {config['bundle_name']} with error {config['error']}")
            
            bundle = self.bundle_library.get_bundle(config['bundle_name'])
            if not bundle:
                print(f"Bundle '{config['bundle_name']}' not found, skipping...")
                continue
            
            curves_batch = self.draw_curves_with_bundle(config['curves'], bundle, config['error'])
            self.draw_curves_on_canvas(curves_batch, bundle)
            self.batch_count += 1
            
            # Save intermediate result
            self.save_current_image(f"demo_batch_{i+1:02d}")
            
            # Pause for user to see
            input("Press Enter to continue to next batch...")
        
        print("\nDemo complete!")
        self.save_current_image("demo_final")


def main():
    """Main function to run the interactive curve drawer."""
    drawer = InteractiveCurveDrawer()
    
    print("Interactive Curve Drawing System")
    print("="*50)
    print("1. Interactive session")
    print("2. Automated demo")
    
    choice = input("\nChoose mode (1 or 2): ").strip()
    
    if choice == '1':
        drawer.run_interactive_session()
    elif choice == '2':
        drawer.run_automated_demo()
    else:
        print("Invalid choice. Running interactive session...")
        drawer.run_interactive_session()


if __name__ == '__main__':
    main() 