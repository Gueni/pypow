import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

# Class A Amplifier Parameters
Vcc = 12.0  # Supply Voltage
Rc = 1000.0  # Collector Resistance
Re = 100.0  # Emitter Resistance
R1 = 100000.0  # Input Resistance
R2 = 100000.0  # Bias Resistance
C1 = 0.1e-6  # Input Capacitor
C2 = 10.0e-6  # Output Capacitor
beta = 200.0  # Transistor beta

# Input Signal Parameters
fs = 100e3  # Sampling Frequency
f0 = 10e3  # Signal Frequency
A = 1.0  # Signal Amplitude

# Calculate Bias Voltage
Vb = Vcc * R2 / (R1 + R2)

# Generate Input Signal
t = np.arange(0, 1/f0, 1/fs)
Vin = A * signal.square(2 * np.pi * f0 * t)

# Amplifier Model
def amplifier(Vin):
    Vbe = 0.7  # Base-Emitter Voltage
    Ic = (Vcc - Vbe - Vin) / (Rc + (1 + beta) * Re)
    Vout = -Ic * Rc
    return Vout

# Simulate Amplifier
Vout = np.zeros(len(t))
for i in range(len(t)):
    Vout[i] = amplifier(Vin[i])

# Plot Input and Output Waveforms
fig, (ax1, ax2) = plt.subplots(2, 1, sharex=True, figsize=(8, 6))
ax1.plot(t, Vin)
ax1.set_ylabel('Input\nVoltage (V)')
ax2.plot(t, Vout)
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Output\nVoltage (V)')
plt.tight_layout()
plt.show()
