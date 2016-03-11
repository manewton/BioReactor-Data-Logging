import pandas as pd

from bokeh.io import curdoc, show, vform, output_file
from bokeh.models import ColumnDataSource, VBox, HBox, Select, CheckboxButtonGroup
from bokeh.plotting import Figure
import os
import sys
curdir = os.path.join(__file__, os.pardir)
pardir = os.path.join(curdir, os.pardir)
py27dir = os.path.abspath(pardir)+'/py27googledriveconnect'
sys.path.insert(0, py27dir)
from downloader import download_latest

datafile = os.path.abspath(pardir)+'/DataManagement/R1data'
download_latest(1, 'R1data')

# Accept/Setup Dataframe to be Plotted
sample_data_live = datafile
sample = pd.read_csv(sample_data_live, parse_dates=[0])
sampleSI = sample.set_index('Date')

source = ColumnDataSource(data=sampleSI)  # requires all columns have same length

plot = Figure(x_axis_type="datetime", plot_width=800)

def make_plot(title, plot):
    plot.title = title
    plot.line(x=sampleSI.index, y=sampleSI[title], color="color", line_alpha="alpha")
    return plot


def update_plot(attrname, old, new):
    data_to_plot = data_select.value
    new_name=datas[data_to_plot]['name']
    new_df=pd.DataFrame(sampleSI[new_name])
    # src =
    make_plot(new_name, plot)


data_to_plot = 'DO'
datas = {
    'DO': {
        'name': 'DO mg/L',
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
plot = make_plot(datas[data_to_plot]['name'], plot)
data_select.on_change('value', update_plot)

controls = VBox(data_select)

curdoc().add_root(HBox(controls, plot))
output_file("bokehplot.html", title="Bokeh Line Plot")
show(HBox(controls, plot))