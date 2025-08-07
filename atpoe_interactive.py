#!/usr/bin/env python3
"""
Interactive AtPoE (Admitting the Possibilities of Error) CLI.
Allows running curves in batches with user feedback and parameter adjustments.
"""

import argparse
import sys
from pathlib import Path
from typing import List, Tuple, Optional, Dict
from PIL import Image, ImageDraw
import os

from atpoe.core.curve_generator import generate_nested_curve, generate_initial_circle


class InteractiveAtPoE:
    """Interactive AtPoE curve generator with user feedback."""
    
    def __init__(self, canvas_size: int = 1000):
        self.canvas_size = canvas_size
        self.curves = []
        self.current_image = None
        self.output_dir = "interactive_atpoe_output"
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Current parameters
        self.params = {
            'curves_per_batch': 3,
            'segment_length': 12,
            'error': 1.5,
            'distance': 8,
            'total_curves': 15
        }
        
        # Colors for curves
        self.colors = ['black', 'blue', 'red', 'green', 'purple', 'orange', 'brown', 'pink', 'gray', 'cyan']
    
    def initialize_canvas(self):
        """Initialize or reset the drawing canvas."""
        self.current_image = Image.new('RGB', (self.canvas_size, self.canvas_size), 'white')
        print(f"Canvas initialized: {self.canvas_size}x{self.canvas_size} pixels")
    
    def generate_curves_batch(self, num_curves: int) -> List[List[Tuple[float, float]]]:
        """Generate a batch of curves with current parameters."""
        batch_curves = []
        
        for i in range(num_curves):
            if len(self.curves) == 0:
                # First curve - generate initial circle
                curve = generate_initial_circle(self.canvas_size, 450, self.params['segment_length'])
                print(f"Generated initial circle ({len(curve)} segments)")
            else:
                # Generate nested curve
                curve = generate_nested_curve(
                    self.curves[-1], 
                    self.params['distance'], 
                    self.params['error'], 
                    self.params['segment_length']
                )
                print(f"Generated curve {len(self.curves) + 1} ({len(curve)} segments)")
            
            if curve:
                batch_curves.append(curve)
                self.curves.append(curve)
            else:
                print(f"Failed to generate curve {len(self.curves) + 1}")
                break
        
        return batch_curves
    
    def draw_curves_on_canvas(self, curves_batch: List[List[Tuple[float, float]]]):
        """Draw the new curves on the canvas."""
        if not self.current_image:
            self.initialize_canvas()
        
        draw = ImageDraw.Draw(self.current_image)
        
        # Draw only the new curves in this batch
        start_idx = len(self.curves) - len(curves_batch)
        
        for i, curve in enumerate(curves_batch):
            curve_idx = start_idx + i
            color = self.colors[curve_idx % len(self.colors)]
            
            # Draw the curve
            for j in range(len(curve)):
                p1 = curve[j]
                p2 = curve[(j + 1) % len(curve)]
                draw.line([p1, p2], fill=color, width=2)
    
    def save_current_image(self, filename: str = None):
        """Save the current image."""
        if not filename:
            filename = f"atpoe_interactive_{len(self.curves)}_curves.png"
        
        filepath = os.path.join(self.output_dir, filename)
        self.current_image.save(filepath)
        print(f"Saved image to: {filepath}")
        return filepath
    
    def display_current_status(self):
        """Display current parameters and progress."""
        print(f"\n{'='*60}")
        print("CURRENT STATUS")
        print(f"{'='*60}")
        print(f"Total curves generated: {len(self.curves)}")
        print(f"Target total curves: {self.params['total_curves']}")
        print(f"Curves per batch: {self.params['curves_per_batch']}")
        print(f"Segment length: {self.params['segment_length']}px")
        print(f"Error level: {self.params['error']}px")
        print(f"Distance between curves: {self.params['distance']}px")
        print(f"Canvas size: {self.canvas_size}x{self.canvas_size}px")
        
        if len(self.curves) >= self.params['total_curves']:
            print("\n🎉 Target number of curves reached!")
    
    def get_user_feedback(self) -> Dict:
        """Get parameter changes from user."""
        print(f"\n{'='*60}")
        print("PARAMETER ADJUSTMENT")
        print(f"{'='*60}")
        print("Enter new values or press Enter to keep current values:")
        
        new_params = self.params.copy()
        
        # Curves per batch
        try:
            input_val = input(f"Curves per batch (current: {self.params['curves_per_batch']}): ").strip()
            if input_val:
                new_params['curves_per_batch'] = int(input_val)
        except ValueError:
            print("Invalid input, keeping current value")
        
        # Segment length
        try:
            input_val = input(f"Segment length (current: {self.params['segment_length']}px): ").strip()
            if input_val:
                new_params['segment_length'] = int(input_val)
        except ValueError:
            print("Invalid input, keeping current value")
        
        # Error level
        try:
            input_val = input(f"Error level (current: {self.params['error']}px): ").strip()
            if input_val:
                new_params['error'] = float(input_val)
        except ValueError:
            print("Invalid input, keeping current value")
        
        # Distance
        try:
            input_val = input(f"Distance between curves (current: {self.params['distance']}px): ").strip()
            if input_val:
                new_params['distance'] = int(input_val)
        except ValueError:
            print("Invalid input, keeping current value")
        
        # Total curves
        try:
            input_val = input(f"Target total curves (current: {self.params['total_curves']}): ").strip()
            if input_val:
                new_params['total_curves'] = int(input_val)
        except ValueError:
            print("Invalid input, keeping current value")
        
        return new_params
    
    def run_interactive_session(self):
        """Run the main interactive session."""
        print("Interactive AtPoE - Admitting the Possibilities of Error")
        print("="*60)
        print("This interactive session allows you to:")
        print("- Generate curves in batches")
        print("- See results after each batch")
        print("- Adjust parameters between batches")
        print("- Continue until target is reached")
        print("="*60)
        
        # Initialize
        self.initialize_canvas()
        
        while len(self.curves) < self.params['total_curves']:
            print(f"\n{'='*60}")
            print(f"BATCH {len(self.curves) // self.params['curves_per_batch'] + 1}")
            print(f"{'='*60}")
            
            # Calculate how many curves to generate in this batch
            remaining = self.params['total_curves'] - len(self.curves)
            batch_size = min(self.params['curves_per_batch'], remaining)
            
            print(f"Generating {batch_size} curves...")
            
            # Generate and draw curves
            curves_batch = self.generate_curves_batch(batch_size)
            self.draw_curves_on_canvas(curves_batch)
            
            # Save and display status
            self.save_current_image()
            self.display_current_status()
            
            # Check if we've reached the target
            if len(self.curves) >= self.params['total_curves']:
                print("\n🎉 Target number of curves reached!")
                break
            
            # Ask user if they want to continue or adjust parameters
            print(f"\n{'='*60}")
            print("NEXT STEPS")
            print(f"{'='*60}")
            print("1. Continue with current parameters")
            print("2. Adjust parameters")
            print("3. Save and exit")
            
            choice = input("\nEnter your choice (1-3): ").strip()
            
            if choice == '1':
                print("Continuing with current parameters...")
                continue
            elif choice == '2':
                new_params = self.get_user_feedback()
                self.params.update(new_params)
                print("Parameters updated!")
            elif choice == '3':
                print("Saving final image and exiting...")
                self.save_current_image("atpoe_interactive_final.png")
                break
            else:
                print("Invalid choice, continuing with current parameters...")
        
        print(f"\nSession complete! Generated {len(self.curves)} curves total.")


def main():
    """Main function for interactive AtPoE."""
    parser = argparse.ArgumentParser(
        description="Interactive AtPoE - Admitting the Possibilities of Error",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python atpoe_interactive.py
  python atpoe_interactive.py --canvas-size 1200
        """
    )
    
    parser.add_argument(
        '--canvas-size', '-s',
        type=int,
        default=1000,
        help='Canvas size in pixels (default: 1000)'
    )
    
    args = parser.parse_args()
    
    # Run interactive session
    try:
        atpoe = InteractiveAtPoE(args.canvas_size)
        atpoe.run_interactive_session()
    except KeyboardInterrupt:
        print("\n\nSession interrupted by user.")
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
