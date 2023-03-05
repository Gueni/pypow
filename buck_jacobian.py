import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from multiprocessing import Process, Queue
import time

# Inductance and capacitance values
L = 100e-6  # Inductance in Henrys
C = 220e-6  # Capacitance in Farads

# Switching frequency and duty cycle
fsw = 100e3  # Switching frequency in Hz
D = 0.1  # Duty cycle

# Load resistance
Rl = 10  # Load resistance in Ohms

# Simulation parameters
t0 = 0  # Initial time
tf = 1e-3  # Final time
dt = 1e-6  # Time step
n = int((tf - t0) / dt) + 1  # Number of time steps

# Initial conditions
IL0 = 0.0# Initial inductor current
VL0 = 5 # Initial voltage across inductor
VL1 = D * VL0  # Voltage across inductor during on-time
VL2 = (1 - D) * VL0  # Voltage across inductor during off-time
VC0 = 0  # Initial voltage across capacitor
x0 = np.array([IL0, VL0, VC0])  # Initial state vector

# Define the derivative function
def f(x, t):
    IL, VL, VC = x  # State variables
    if (t % (1/fsw)) < (D / fsw):
        dIL = (VL1 - VL) / L
        dVL = (1 / C) * (VC - VL)
    else:
        dIL = (VL2 - VL) / L
        dVL = (1 / C) * (VC - VL + (IL * Rl))
    dVC = -dVL
    return np.array([dIL, dVL, dVC])  # Return derivative vector

# Calculate the Jacobian matrix
Jf = np.array([
    [-1/L, 1/L, 0],
    [1/C, -1/C, -1/C],
    [0, 1/C, -1/C]
])

# Set up the figure and axes for the plot
fig, ax = plt.subplots()
ax.set_xlim(t0, tf)
ax.set_ylim(0, VL0 + 10)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Voltage (V)')

# Initialize the plot elements
line, = ax.plot([], [])
text = ax.text(0.02, 0.95, '', transform=ax.transAxes)

# Define the function to calculate the simulation
def calculate(q):
    x = x0
    q.put(x)
    for i in range(1, n):
        t = t0 + i * dt
        x = x + dt * f(x, t)
        q.put(x)

# Define the animation function
def animate(i):
    if not q.empty():
        x = q.get()
        x_plot[i] = x
        line.set_data(np.linspace(t0, t0 + i * dt, i + 1), x_plot[:i + 1, 1])
        text.set_text(f'Time = {t0 + i * dt:.7f} s')
    return line, text

# Set up the plot
x_plot = np.zeros((n, 3))
x_plot[0] = x0

if __name__ == "__main__":
    # Set up the queue and process for the simulation
    q = Queue()
    p = Process(target=calculate, args=(q,))
    p.start()

    # Set up the animation
    ani = FuncAnimation(fig, animate, frames=n-1, blit=True)

    # Start the simulation and animation
    plt.show()

    # Join the simulation process
    p.join()
