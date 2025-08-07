#!/usr/bin/env python3
"""
Demo version of Interactive AtPoE that shows the workflow with predefined responses.
This demonstrates how the interactive session works without requiring user input.
"""

import sys
import os
from unittest.mock import patch
from atpoe_interactive import InteractiveAtPoE


def demo_interactive_session():
    """Run a demo of the interactive session with predefined responses."""
    print("🎬 DEMO: Interactive AtPoE Session")
    print("="*60)
    print("This demo shows how the interactive session works.")
    print("It will generate curves in batches and 'adjust' parameters.")
    print("="*60)
    
    # Create interactive AtPoE instance
    atpoe = InteractiveAtPoE(canvas_size=1000)
    
    # Demo responses for different batches
    demo_responses = [
        # Batch 1: Continue with current parameters
        ['1'],
        # Batch 2: Adjust parameters (increase error, decrease distance)
        ['2', '', '', '2.5', '6', ''],  # Keep most params, change error to 2.5, distance to 6
        # Batch 3: Continue with new parameters
        ['1'],
        # Batch 4: Adjust parameters (increase segment length)
        ['2', '', '15', '', '', ''],  # Change segment length to 15
        # Batch 5: Save and exit
        ['3']
    ]
    
    # Initialize canvas
    atpoe.initialize_canvas()
    
    batch_num = 0
    response_index = 0
    
    while len(atpoe.curves) < atpoe.params['total_curves'] and response_index < len(demo_responses):
        print(f"\n{'='*60}")
        print(f"BATCH {batch_num + 1}")
        print(f"{'='*60}")
        
        # Calculate batch size
        remaining = atpoe.params['total_curves'] - len(atpoe.curves)
        batch_size = min(atpoe.params['curves_per_batch'], remaining)
        
        print(f"Generating {batch_size} curves...")
        
        # Generate and draw curves
        curves_batch = atpoe.generate_curves_batch(batch_size)
        atpoe.draw_curves_on_canvas(curves_batch)
        
        # Save and display status
        atpoe.save_current_image()
        atpoe.display_current_status()
        
        # Check if we've reached the target
        if len(atpoe.curves) >= atpoe.params['total_curves']:
            print("\n🎉 Target number of curves reached!")
            break
        
        # Show the menu
        print(f"\n{'='*60}")
        print("NEXT STEPS")
        print(f"{'='*60}")
        print("1. Continue with current parameters")
        print("2. Adjust parameters")
        print("3. Save and exit")
        
        # Use demo response
        if response_index < len(demo_responses):
            responses = demo_responses[response_index]
            
            # Simulate user input
            with patch('builtins.input', side_effect=responses):
                choice = responses[0]
                print(f"\nDemo choice: {choice}")
                
                if choice == '1':
                    print("Continuing with current parameters...")
                elif choice == '2':
                    print("Adjusting parameters...")
                    new_params = atpoe.get_user_feedback()
                    atpoe.params.update(new_params)
                    print("Parameters updated!")
                elif choice == '3':
                    print("Saving final image and exiting...")
                    atpoe.save_current_image("atpoe_interactive_demo_final.png")
                    break
        
        batch_num += 1
        response_index += 1
    
    print(f"\n🎬 Demo complete! Generated {len(atpoe.curves)} curves total.")
    print(f"Check the 'interactive_atpoe_output' directory for generated images.")


def main():
    """Main function for the demo."""
    try:
        demo_interactive_session()
    except Exception as e:
        print(f"Demo error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
