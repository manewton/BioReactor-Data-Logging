import pandas as pd

from bokeh.io import curdoc, show, vform, output_file
from bokeh.models import ColumnDataSource, VBox, HBox, Select, CheckboxButtonGroup
from bokeh.plotting import Figure


# Accept/Setup Dataframe to be Plotted
sample_data_live = 'sampledatalive.csv'
sample = pd.read_csv(sample_data_live, parse_dates = [0])
sampleSI = sample.set_index('Date')

source = ColumnDataSource(data=sampleSI)  # requires all columns have same length


def make_plot(sources, title):
    plot = Figure(x_axis_type="datetime", plot_width=800)
    plot.title = title
    plot.line(x="Date", y=datas[data_to_plot]['name'], source=sources, color="color", line_alpha="alpha")

    return plot


def update_plot(attrname, old, new):
    data_to_plot = data_select.value
    plot.title = datas[data_to_plot]['title']

    # src =
    source.data.update(data_to_plot)



data_to_plot = 'DO'
datas = {
    'DO': {
        'name': 'DO',
        'title': 'Dissolved Oxygen'
    },
    'pH': {
        'name': 'pH',
        'title': 'pH'
    },
    'NH4': {
        'name': 'NH4',
        'title': 'NH4 Conc.'
    },
    'N2 Mass Flow Controller': {
        'name': 'N2 Mass Flow Controller',
        'title': 'N2 Flow Rate'
    }
}

data_select = Select(value=data_to_plot, title='Data', options=sorted(datas.keys()))
plot = make_plot(source, datas[data_to_plot]['title'])

data_select.on_change('value', update_plot)

controls = VBox(data_select)

curdoc().add_root(HBox(controls, plot))
output_file("bokehplot.html", title="Bokeh Line Plot")
show(HBox(controls, plot))