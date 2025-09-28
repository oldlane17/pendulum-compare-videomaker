import numpy as np

class PendulumSimulator:
    """
    Physics simulator for pendulum systems
    """
    
    def __init__(self):
        pass
    
    def pendulum(self, gamma, lambda_val, L, acceleration, phi0, phi_dot0, t_start, t_end, delta_t):
        """
        Simulate pendulum motion using Leapfrog algorithm
        """
        l = lambda_val * L
        omega = np.sqrt(acceleration / l)
        Omega = np.sqrt(omega**2 / gamma) if gamma > 0 else omega
        delta_tau = Omega * delta_t
        N = int((t_end - t_start) / delta_t)

        phi = phi0
        phi_dot = phi_dot0

        time_list = []
        phi_list = []

        for _ in range(N):
            time_list.append(t_start)
            phi_list.append(phi)
            tau = omega * t_start

            # Update position with Leapfrog
            phi_dot += (-gamma * np.sin(phi) - lambda_val * np.sin(phi)) * delta_tau / 2
            phi += phi_dot * delta_tau
            phi_dot += (-gamma * np.sin(phi) - lambda_val * np.sin(phi - tau - tau)) * delta_tau / 2

            t_start += delta_t

        return np.array(time_list), np.array(phi_list)
    
    def calculate_omega(self, acceleration, l):
        """Calculate omega from acceleration and length"""
        return np.sqrt(acceleration / l)
