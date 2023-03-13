import numpy as np
import matplotlib.pyplot as plt

# Motor parameters
R = 1.0     # resistance
L = 0.1     # inductance
J = 0.01    # moment of inertia
B = 0.1     # damping coefficient
Kt = 0.5    # torque constant
Kb = 0.5    # back-emf constant
N = 3       # number of poles

# Control parameters
Kp = 5      # proportional gain
Kd = 1      # derivative gain

# Simulation parameters
t0 = 0      # initial time
tf = 5     # final time
dt = 0.01  # time step

# Initial conditions
theta0 = 0      # initial position
omega0 = 0      # initial velocity
i0 = 5          # initial current

# Function to compute the derivatives of the state variables
def f(t, x, u):
    theta, omega, i = x
    v = Kb*N*omega    # back-emf voltage
    di_dt = (-R*i + v + u)/L    # current rate of change
    domega_dt = (Kt*i - B*omega)/J    # velocity rate of change
    dtheta_dt = omega    # position rate of change
    return dtheta_dt, domega_dt, di_dt

# Arrays to store the state variables and control inputs
t_array = np.arange(t0, tf, dt)
theta_array = np.zeros_like(t_array)
omega_array = np.zeros_like(t_array)
i_array = np.zeros_like(t_array)
u_array = np.zeros_like(t_array)

# Initial conditions
theta_array[0] = theta0
omega_array[0] = omega0
i_array[0] = i0

# Simulation loop
for i in range(1, len(t_array)):
    # Compute control input
    error = -theta_array[i-1]
    error_dot = -omega_array[i-1]
    u = Kp*error + Kd*error_dot

    # Simulate one time step
    x = theta_array[i-1], omega_array[i-1], i_array[i-1]
    dx_dt = f(t_array[i-1], x, u)
    theta_array[i] = theta_array[i-1] + dx_dt[0]*dt
    omega_array[i] = omega_array[i-1] + dx_dt[1]*dt
    i_array[i] = i_array[i-1] + dx_dt[2]*dt
    u_array[i] = u

# Plot the results
fig, axs = plt.subplots(3, 1, figsize=(8, 8))

axs[0].plot(t_array, theta_array)
axs[0].set_xlabel('Time (s)')
axs[0].set_ylabel('Position (rad)')

axs[1].plot(t_array, omega_array)
axs[1].set_xlabel('Time (s)')
axs[1].set_ylabel('Velocity (rad/s)')

axs[2].plot(t_array, u_array)
axs[2].set_xlabel('Time (s)')
axs[2].set_ylabel('Control input (V)')

plt.tight_layout()
plt.show()
