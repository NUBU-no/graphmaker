import io
from matplotlib.backends.backend_svg import FigureCanvasSVG
import pandas as pd
import seaborn as sns
import matplotlib

matplotlib.use('agg') 

def make_file(fig):
    output = io.BytesIO()
    FigureCanvasSVG(fig).print_svg(output)
    return output


def make_graph(data, settings=dict()):
    standard_settings = {'x': 'key',
                         'y': 'value',
                         'hue': 'time',
                         'alpha': 0.8,
                         'kind': 'bar',
                         }
    standard_settings.update(settings)
    settings = standard_settings.copy()
    g = sns.catplot(x=settings['x'], y=settings['y'], hue=settings['hue'],
                                      data=data, kind=settings['kind'], alpha=settings['alpha'])

    if settings['yellow_hline']:
        g.ax.axhline(int(settings['yellow_hline']), color = 'yellow', alpha=0.5, linestyle='--')
    if settings['red_hline']:
        g.ax.axhline(int(settings['red_hline']), color = 'red', alpha=0.5, linestyle='--')
    return g.fig


def create_graph_file(data, settings):
    fig = make_graph(data=data, settings=settings)
    return make_file(fig=fig)
