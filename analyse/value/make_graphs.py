import random

import pandas as pd
import plotly.graph_objects as go

from analyse.utils import unique, average, set_plotly_theme

data = pd.read_json("results.json")

bca = pd.json_normalize(data.bca)
gaDarwin = pd.json_normalize(data.gaDarwin)
gaDeVries = pd.json_normalize(data.gaDeVries)

n = len(bca)
sizes = unique(bca["size"].values)  # размеры задач
k = len(sizes)
m = n // k  # количество запусков для одной и той же задачи


def average_value(df):
    return [average(df["value"][m * i:m * (i + 1)].values, integer=False) for i in range(k)]


bca_average_value = average_value(bca)
gaDarwin_average_value = average_value(gaDarwin)
gaDeVries_average_value = average_value(gaDeVries)
sizes = [str(size) for size in sizes]

set_plotly_theme(theme="presentation")
figure = go.Figure(data=[
    go.Bar(name="Иммунный",
           x=sizes,
           y=bca_average_value,
           marker_color="#70e500",
           ),
    go.Bar(name="Пчелиный",
           x=sizes,
           y=gaDarwin_average_value,
           marker_color="#ffbc00",
           ),
    go.Bar(name="Муравьиный",
           x=sizes,
           y=gaDeVries_average_value,
           marker_color="#1921b0",
           )
])

figure.update_layout(

    bargap=0.25,
    width=900,
    height=700,
    font={
        'family': "Arial",
        'size': 14,
        'color': "black",
    },
    xaxis_title="Размер задачи",
    yaxis_title="Значение ЦФ",
    legend={
        'orientation': 'h',
        'yanchor': "bottom",
        'y': 1.0,
        'x': 0.6
    }
)
figure.show()
