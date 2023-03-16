import pandas as pd
import plotly.express as px
import plotly.graph_objs as go

# Load CSV data into a pandas DataFrame
df = pd.read_csv('data.csv')

# Create figure object
fig = go.Figure()

# Add trace for current
fig.add_trace(go.Scatter(x=df['time'], y=df['current'], name='Current'))

# Add trace for voltage
fig.add_trace(go.Scatter(x=df['time'], y=df['voltage'], name='Voltage'))

# Add trace for power
fig.add_trace(go.Scatter(x=df['time'], y=df['power'], name='Power'))

# Set layout with sliders
fig.update_layout(
    sliders=[
        dict(
            active=1,
            currentvalue=dict(
                prefix='Constant 1: ',
                xanchor='right',
                font=dict(size=16)
            ),
            pad=dict(t=50),
            steps=[
                dict(
                    label='1',
                    method='update',
                    args=[{'visible': [True, True, True]},
                          {'title': 'Constant 1: 1'}]
                ),
                dict(
                    label='2',
                    method='update',
                    args=[{'visible': [True, False, True]},
                          {'title': 'Constant 1: 2'}]
                ),
                dict(
                    label='3',
                    method='update',
                    args=[{'visible': [False, True, True]},
                          {'title': 'Constant 1: 3'}]
                )
            ]
        ),
        dict(
            active=0,
            currentvalue=dict(
                prefix='Constant 2: ',
                xanchor='right',
                font=dict(size=16)
            ),
            pad=dict(t=50),
            steps=[
                dict(
                    label='1',
                    method='update',
                    args=[{'visible': [True, True, True]},
                          {'title': 'Constant 2: 1'}]
                ),
                dict(
                    label='2',
                    method='update',
                    args=[{'visible': [True, True, False]},
                          {'title': 'Constant 2: 2'}]
                ),
                dict(
                    label='3',
                    method='update',
                    args=[{'visible': [True, False, True]},
                          {'title': 'Constant 2: 3'}]
                )
            ]
        ),
        dict(
            active=0,
            currentvalue=dict(
                prefix='Variable: ',
                xanchor='right',
                font=dict(size=16)
            ),
            pad=dict(t=50),
            steps=[
                dict(
                    label='10',
                    method='update',
                    args=[{'y': [df['current'], df['voltage'], df['power'] * 10]},
                          {'title': 'Variable: 10'}]
                ),
                dict(
                    label='20',
                    method='update',
                    args=[{'y': [df['current'], df['voltage'], df['power'] * 20]},
                          {'title': 'Variable: 20'}]
                ),
                dict(
                    label='30',
                    method='update',
                    args=[{'y': [df['current'], df['voltage'], df['power'] * 30]},
                          {'title': 'Variable: 30'}]
                )
            ]
        )
    ],
    title='Constant 1: 1, Constant 2: 1, Variable: 10'
)

# Show the figure
fig.show()
