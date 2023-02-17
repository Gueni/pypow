import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Circuit parameters
R = 1e3  # 1 kOhm
L = 10e-3  # 10 mH

# Define the transfer function of the RL circuit
tf = signal.TransferFunction([R, 0], [L, R])

# Generate a step input and simulate the circuit's response
t, y = signal.step(tf)

# Plot the step response
plt.plot(t, y)
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Step Response of RL Circuit')
plt.show()
