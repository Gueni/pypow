
import time
import plotly.graph_objs as go
import plotly.offline as pyo
from scipy import signal
"""
This code defines the circuit parameters of an RL circuit with an inductor,
creates a transfer function of the circuit using scipy.signal.
TransferFunction, generates a step input, and simulates the circuit's response
using scipy.signal.step. It then creates a Plotly figure of the step response
using plotly.graph_objs.Scatter and adds it to the figure using 
plotly.graph_objs.Figure.add_trace.

The code then sets the title and axis labels of the figure using 
plotly.graph_objs.Layout.update_layout and saves the figure as an HTML file
using plotly.offline.plot. The auto_open parameter is set to True, which means
the HTML file will automatically open in a new browser tab once it is generated.

When you run this code, it will create an HTML file named "inductor.html" in the
current working directory and automatically open it in a new browser tab. The HTML
file will contain the step response plot of the RL circuit with the inductor.

"""
# Circuit parameters
R = 1e3  # 1 kOhm
L = 10e-3  # 10 mH

# Define the transfer function of the RL circuit
tf = signal.TransferFunction([0, 1], [L, R])

# Generate a step input and simulate the circuit's response
t, y = signal.step(tf)

# Create a Plotly figure of the step response
fig = go.Figure()
fig.add_trace(go.Scatter(x=t, y=y, mode='lines', name='Current through Inductor'))

# Set the title and axis labels of the figure
fig.update_layout(title='Step Response of RL Circuit with Inductor',
                  xaxis_title='Time (s)', yaxis_title='Current (A)')

# Add a legend to the figure
fig.update_layout(legend=dict(
    x=0,
    y=1,
    traceorder='normal',
    font=dict(
        family='sans-serif',
        size=12,
        color='black'
    ),
    bgcolor='LightSteelBlue',
    bordercolor='Black',
    borderwidth=2
))

# Get the current Unix timestamp
unix_timestamp = int(time.time())
# Save the figure as an HTML file
pyo.plot(fig, filename = str(unix_timestamp)+'inductor.html', auto_open=False)