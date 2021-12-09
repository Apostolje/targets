import pandas as pd
import plotly.graph_objects as go

from analyse.utils import unique, average, set_plotly_theme, figures_to_html

data = pd.read_json("results.json")

bca = pd.json_normalize(data.bca)
gaDarwin = pd.json_normalize(data.gaDarwin)
gaDeVries = pd.json_normalize(data.gaDeVries)

n = len(bca)
sizes = unique(bca["size"].values)  # размеры задач
k = len(sizes)
m = n // k  # количество запусков для одной и той же задачи


def average_time(df):
    return [average(df["time"][m * i:m * (i + 1)].values) for i in range(k)]


bca_average_time = average_time(bca)
gaDarwin_average_time = average_time(gaDarwin)
gaDeVries_average_time = average_time(gaDeVries)

set_plotly_theme("presentation")
figure = go.Figure()
figure.add_trace(go.Scatter(x=sizes, mode="lines",
                            y=bca_average_time,
                            name="Иммунный",
                            line={'color': "#70e500"},
                            ))

figure.add_trace(go.Scatter(x=sizes, mode="lines",
                            y=gaDarwin_average_time,
                            name="Пчелиный",
                            line={'color': "#ffbc00"},
                            ))

figure.add_trace(go.Scatter(x=sizes, mode="lines",
                            y=gaDeVries_average_time,
                            name="Муравьиный",
                            line={'color': "#1921b0"},
                            ))

figure.update_layout(
    width=900,
    height=700,
    font={
        'family': "Arial",
        'size': 14,
        'color': "black",
    },
    xaxis_title="Размер задачи",
    yaxis_title="Время выполнения (сек.)",
    legend={
        'orientation': 'h',
        'yanchor': "bottom",
        'y': 1.0,
        'x': 0.6
    }
)

figures_to_html([figure], filename="comparison.html")
figure.show()
