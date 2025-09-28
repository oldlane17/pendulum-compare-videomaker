import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib import rcParams

# Configure matplotlib for better performance
rcParams['figure.max_open_warning'] = 0

class PendulumAnimator:
    """
    Create animations for pendulum systems
    """
    
    def __init__(self):
        self.shortnametosymbol = {
            "gamma": "γ", "lambda_val": "λ", "L": "L", "l": "l", 
            "acceleration": "a", "omega": "ω", "phi0": "ϕ0", "phi_dot0": "ϕ̇0"
        }
        self.shortnametounit = {
            "gamma": "", "lambda_val": "", "L": "m", "l": "m", 
            "acceleration": "m/s²", "omega": "s⁻¹", "phi0": "rad", "phi_dot0": "rad/s"
        }
    
    def create_single_animation(self, simulator, params, t_start, t_end, fps, description, output_path):
        """Create animation for single pendulum"""
        delta_t = 1.0 / fps
        duration_seconds = float(t_end - t_start)
        desired_frames = max(int(fps * duration_seconds), 2)
        interval_ms = 1000.0 / fps
        
        # Simulate pendulum
        time, phi = simulator.pendulum(
            params['gamma'], params['lambda_val'], params['L'], 
            params['acceleration'], params['phi0'], params['phi_dot0'], 
            t_start, t_end, delta_t
        )
        
        # Interpolate for smooth animation
        new_t = np.linspace(t_start, t_end, desired_frames, endpoint=False)
        new_phi = np.interp(new_t, time, phi)
        
        # Calculate wheel omega
        wheel_omega = params['omega'] / np.sqrt(params['L'])
        l = params['lambda_val'] * params['L']
        
        # Create figure
        fig = plt.figure(figsize=(9, 6), dpi=200)
        ax = fig.add_axes([0.1, 0.375, 0.8, 0.5])
        fig.set_facecolor('#02133e')
        
        # Set plot limits
        max_extent = params['L'] + l + 0.1
        ax.set_xlim([-max_extent, max_extent])
        ax.set_ylim([-max_extent, max_extent])
        
        # Styling
        ax.tick_params(axis='x', labelcolor='white')
        ax.tick_params(axis='y', labelcolor='white')
        ax.set_xlabel('metres', color='white', fontsize=14)
        ax.set_ylabel('metres', color='white', fontsize=14)
        ax.set_title(description, color='white', fontsize=20)
        ax.grid(color='#02133e')
        
        # Create pendulum artists
        point_wheel, = ax.plot([], [], 'ko', ms=6)
        line_main, = ax.plot([], [], 'ro-', lw=2)
        line_mass, = ax.plot([], [], 'bo-', lw=2)
        
        # Create legend
        settings_text = self._create_settings_text(params)
        leg = ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                       ncol=3, facecolor='#182a69', labelcolor='white', 
                       title_fontsize=12, frameon=True, title=settings_text)
        if leg and leg.get_title():
            leg.get_title().set_color('white')
        
        def init():
            line_main.set_data([], [])
            line_mass.set_data([], [])
            point_wheel.set_data([0], [0])
            return line_main, line_mass, point_wheel
        
        def animate(i):
            tau = wheel_omega * new_t[i]
            phi_i = new_phi[i]
            mount_x = params['L'] * np.sin(tau)
            mount_y = -params['L'] * np.cos(tau)
            mass_x = mount_x + l * np.sin(phi_i)
            mass_y = mount_y - l * np.cos(phi_i)

            line_main.set_data([0.0, mount_x], [0.0, mount_y])
            line_mass.set_data([mount_x, mass_x], [mount_y, mass_y])
            point_wheel.set_data([0.0], [0.0])
            return line_main, line_mass, point_wheel
        
        # Create animation
        ani = animation.FuncAnimation(
            fig, animate, frames=range(len(new_t)), init_func=init,
            interval=interval_ms, blit=True, repeat=False
        )
        
        # Save animation
        ani.save(output_path, fps=fps, dpi=200)
        plt.close(fig)
        
        print(f"Saved {output_path} at {fps} fps ({desired_frames} frames, {duration_seconds:.1f} s)")
    
    def create_comparison_animation(self, simulator, params1, params2, t_start, t_end, fps, description, output_path):
        """Create comparison animation for two pendulums"""
        delta_t = 1.0 / fps
        duration_seconds = float(t_end - t_start)
        desired_frames = max(int(fps * duration_seconds), 2)
        interval_ms = 1000.0 / fps
        
        # Simulate both pendulums
        time1, phi1 = simulator.pendulum(
            params1['gamma'], params1['lambda_val'], params1['L'], 
            params1['acceleration'], params1['phi0'], params1['phi_dot0'], 
            t_start, t_end, delta_t
        )
        
        time2, phi2 = simulator.pendulum(
            params2['gamma'], params2['lambda_val'], params2['L'], 
            params2['acceleration'], params2['phi0'], params2['phi_dot0'], 
            t_start, t_end, delta_t
        )
        
        # Interpolate for smooth animation
        new_t = np.linspace(t_start, t_end, desired_frames, endpoint=False)
        new_phi1 = np.interp(new_t, time1, phi1)
        new_phi2 = np.interp(new_t, time2, phi2)
        
        # Calculate wheel omegas
        wheel_omega1 = params1['omega'] / np.sqrt(params1['L'])
        wheel_omega2 = params2['omega'] / np.sqrt(params2['L'])
        
        l1 = params1['lambda_val'] * params1['L']
        l2 = params2['lambda_val'] * params2['L']
        
        # Create figure
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9), dpi=200, constrained_layout=True)
        fig.set_facecolor('#02133e')
        
        # Determine plot limits
        max_L = max(params1['L'], params2['L'])
        max_l = max(l1, l2)
        max_extent = max_L + max_l + 0.1
        
        for ax in (ax1, ax2):
            ax.set_xlim([-max_extent, max_extent])
            ax.set_ylim([-max_extent, max_extent])
            ax.tick_params(axis='x', labelcolor='white')
            ax.tick_params(axis='y', labelcolor='white')
            ax.set_xlabel('metres', color='white')
            ax.set_ylabel('metres', color='white')
            ax.grid(color='#02133e')
        
        ax1.set_title(f"{description} — Pendulum 1", color='white', fontsize=16)
        ax2.set_title(f"{description} — Pendulum 2", color='white', fontsize=16)
        
        # Create artists
        point_wheel1, = ax1.plot([], [], 'ko', ms=6)
        line_main1, = ax1.plot([], [], 'ro-', lw=2)
        line_mass1, = ax1.plot([], [], 'bo-', lw=2)
        
        point_wheel2, = ax2.plot([], [], 'ko', ms=6)
        line_main2, = ax2.plot([], [], 'ro-', lw=2)
        line_mass2, = ax2.plot([], [], 'bo-', lw=2)
        
        # Create legends
        settings_text1 = self._create_settings_text(params1)
        settings_text2 = self._create_settings_text(params2)
        
        leg1 = ax1.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                         ncol=3, facecolor='#182a69', labelcolor='white', 
                         title_fontsize=10, frameon=True, title=settings_text1)
        leg2 = ax2.legend(loc='upper center', bbox_to_anchor=(0.5, -0.12),
                         ncol=3, facecolor='#182a69', labelcolor='white', 
                         title_fontsize=10, frameon=True, title=settings_text2)
        
        for leg in [leg1, leg2]:
            if leg and leg.get_title():
                leg.get_title().set_color('white')
        
        def init():
            for artist in (line_main1, line_mass1, point_wheel1, line_main2, line_mass2, point_wheel2):
                artist.set_data([], [])
            return line_main1, line_mass1, point_wheel1, line_main2, line_mass2, point_wheel2
        
        def animate(i):
            # Pendulum 1
            tau1 = wheel_omega1 * new_t[i]
            phi_a = new_phi1[i]
            mount_x1 = params1['L'] * np.sin(tau1)
            mount_y1 = -params1['L'] * np.cos(tau1)
            mass_x1 = mount_x1 + l1 * np.sin(phi_a)
            mass_y1 = mount_y1 - l1 * np.cos(phi_a)
            
            line_main1.set_data([0.0, mount_x1], [0.0, mount_y1])
            line_mass1.set_data([mount_x1, mass_x1], [mount_y1, mass_y1])
            point_wheel1.set_data([0.0], [0.0])
            
            # Pendulum 2
            tau2 = wheel_omega2 * new_t[i]
            phi_b = new_phi2[i]
            mount_x2 = params2['L'] * np.sin(tau2)
            mount_y2 = -params2['L'] * np.cos(tau2)
            mass_x2 = mount_x2 + l2 * np.sin(phi_b)
            mass_y2 = mount_y2 - l2 * np.cos(phi_b)
            
            line_main2.set_data([0.0, mount_x2], [0.0, mount_y2])
            line_mass2.set_data([mount_x2, mass_x2], [mount_y2, mass_y2])
            point_wheel2.set_data([0.0], [0.0])
            
            return line_main1, line_mass1, point_wheel1, line_main2, line_mass2, point_wheel2
        
        # Create animation
        ani = animation.FuncAnimation(
            fig, animate, frames=range(len(new_t)), init_func=init,
            interval=interval_ms, blit=True, repeat=False
        )
        
        # Save animation
        ani.save(output_path, fps=fps, dpi=200)
        plt.close(fig)
        
        print(f"Saved {output_path} at {fps} fps ({desired_frames} frames, {duration_seconds:.1f} s)")
    
    def _create_settings_text(self, params):
        """Create formatted settings text for legend"""
        lines = []
        for key, value in params.items():
            symbol = self.shortnametosymbol.get(key, key)
            unit = self.shortnametounit.get(key, "")
            lines.append(f"{symbol}: {value:.3f} {unit}")
        return "\n".join(lines)

def create_animation(simulator, output_path, pend1_params, compare=False, 
                    compare_value=None, t_start=0.0, t_end=10.0, fps=60, 
                    description="Pendulum Simulation"):
    """
    Main function to create pendulum animations
    """
    animator = PendulumAnimator()
    
    if compare and compare_value:
        animator.create_comparison_animation(
            simulator, pend1_params, compare_value, t_start, t_end, 
            fps, description, output_path
        )
    else:
        animator.create_single_animation(
            simulator, pend1_params, t_start, t_end, fps, description, output_path
        )
