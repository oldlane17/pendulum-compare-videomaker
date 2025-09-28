#!/usr/bin/env python3
"""
Pendulum Simulator - A physics-based pendulum animation system
"""

import argparse
import sys
import os

# Add the pendulum package to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'pendulum'))

from pendulum.simulator import PendulumSimulator
from pendulum.animator import create_animation

def parse_pendulum_args(arg_list):
    """Parse pendulum arguments from list"""
    if len(arg_list) != 8:
        raise ValueError(f"Expected 8 arguments for pendulum, got {len(arg_list)}")
    
    return {
        'gamma': float(arg_list[0]),
        'lambda_val': float(arg_list[1]),
        'L': float(arg_list[2]),
        'l': float(arg_list[3]),
        'acceleration': float(arg_list[4]),
        'omega': float(arg_list[5]),
        'phi0': float(arg_list[6]),
        'phi_dot0': float(arg_list[7])
    }

def main():
    parser = argparse.ArgumentParser(
        description='Pendulum Simulator - Create physics-based pendulum animations',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Example usage:
  # Single pendulum
  python main.py --path "output.mp4" --pend1 0.25 0.075 0.03 0.4 9.81 5.0 -0.785 0.0
  
  # Compare two pendulums
  python main.py --path "comparison.mp4" \\
    --pend1 0.25 0.075 0.03 0.4 9.81 5.0 -0.785 0.0 \\
    --pend2 0.5 0.075 0.03 0.4 9.81 8.0 -0.785 0.0
  
Argument order for pendulums:
  gamma, lambda_val, L, l, acceleration, omega, phi0, phi_dot0
        """
    )
    
    parser.add_argument('--path', type=str, required=True,
                       help='Output path for the animation file')
    
    parser.add_argument('--pend1', nargs=8, type=float, required=True,
                       metavar=('GAMMA', 'LAMBDA', 'L', 'l', 'ACCEL', 'OMEGA', 'PHI0', 'PHI_DOT0'),
                       help='Parameters for first pendulum (8 values required)')
    
    parser.add_argument('--pend2', nargs=8, type=float, required=False,
                       metavar=('GAMMA', 'LAMBDA', 'L', 'l', 'ACCEL', 'OMEGA', 'PHI0', 'PHI_DOT0'),
                       help='Parameters for second pendulum (for comparison)')
    
    parser.add_argument('--t_start', type=float, default=0.0,
                       help='Start time for simulation (default: 0.0)')
    
    parser.add_argument('--t_end', type=float, default=10.0,
                       help='End time for simulation (default: 10.0)')
    
    parser.add_argument('--fps', type=int, default=60,
                       help='Frames per second for animation (default: 60)')
    
    parser.add_argument('--desc', type=str, default='Pendulum Simulation',
                       help='Description for the animation')
    
    args = parser.parse_args()
    
    try:
        # Parse pendulum parameters
        pend1_params = parse_pendulum_args(args.pend1)
        
        if args.pend2:
            pend2_params = parse_pendulum_args(args.pend2)
            compare_value = (pend1_params, pend2_params)
            compare = True
        else:
            compare_value = None
            compare = False
        
        # Create output directory if it doesn't exist
        output_dir = os.path.dirname(args.path)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Create simulator instance
        simulator = PendulumSimulator()
        
        # Generate animation
        create_animation(
            simulator=simulator,
            output_path=args.path,
            pend1_params=pend1_params,
            compare=compare,
            compare_value=compare_value,
            t_start=args.t_start,
            t_end=args.t_end,
            fps=args.fps,
            description=args.desc
        )
        
        print(f"Animation successfully saved to: {args.path}")
        
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
