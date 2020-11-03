import numpy as np
import plotly.graph_objects as go


def plot_chart(df):
    x = np.arange(df.shape[0])

    interval = 20
    vals = np.arange(df.shape[0], step=interval)
    labels = list(df[::interval].index)

    fig = go.Figure(
        data=[go.Candlestick(
            x=x,
            open=df['Open'],
            high=df['High'],
            low=df['Low'],
            close=df['Close']),
        ],
        layout=go.Layout(
            xaxis=dict(
                tickvals=vals,
                ticktext=labels,
                tickangle=-45
            ),
        )
    )
    fig.show()


plot_chart(df_t)
