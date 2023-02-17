# Define the frequency and amplitude of the sinusoidal input
f = 100  # 100 Hz
A = 1  # 1 A

import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# Circuit parameters
R = 1e3  # 1 kOhm
L = 10e-3  # 10 mH
# Generate the input waveform
t = np.linspace(0, 1/f, 1000)
u = A * np.sin(2 * np.pi * f * t)
# Define the transfer function of the RL circuit
tf = signal.TransferFunction([R, 0], [L, R])
# Simulate the circuit's response to the input waveform
t, y, _ = signal.lsim(tf, u, t)

# Plot the input and output waveforms
plt.plot(t, u, label='Input')
plt.plot(t, y, label='Output')
plt.xlabel('Time (s)')
plt.ylabel('Current (A)')
plt.title('Response of RL Circuit to Sinusoidal Input')
plt.legend()
plt.show()
