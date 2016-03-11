import os
import sys
import time

import pandas as pd
from bokeh.io import output_file
from bokeh.models import ColumnDataSource, HBox
from bokeh.plotting import Figure, output_server, curdoc, show, gridplot

# Prepare output to server
output_server("BioReactor_Data_Logging")

# Retrieves latest updated data file from google drive
curdir = os.path.join(__file__, os.pardir)
pardir = os.path.join(curdir, os.pardir)
py27dir = os.path.abspath(pardir) + '/py27googledriveconnect'
sys.path.insert(0, py27dir)
# from downloader import download_latest

# datafile = os.path.abspath(pardir) + '/SampleData/R1data.csv'
# download_latest(1, 'R1data.csv')

# Accept/Setup Dataframe to be Plotted
sample_data_live = 'R1datatest.csv'
sample = pd.read_csv(sample_data_live, parse_dates=[0])
sampleSI = sample.set_index('Date')

source = ColumnDataSource(data=sampleSI)  # requires all columns have same length

# Initialize plot figures
plot1 = Figure(x_axis_type="datetime", plot_width=800)
plot2 = Figure(x_axis_type="datetime", plot_width=800)
plot3 = Figure(x_axis_type="datetime", plot_width=800)
plot4 = Figure(x_axis_type="datetime", plot_width=800)
plot5 = Figure(x_axis_type="datetime", plot_width=800)


def make_plot(title1, plot1, title2, plot2, title3, plot3, title4, plot4, title5, plot5):
    plot1.title = title1
    plot2.title = title2
    plot3.title = title3
    plot4.title = title4
    plot5.title = title5
    plot1.yaxis.axis_label = datas['DO']['title']
    plot1.yaxis.axis_label_text_font_style = "italic"
    plot2.yaxis.axis_label = datas['Ammonium']['title']
    plot2.yaxis.axis_label_text_font_style = "italic"
    plot3.yaxis.axis_label = datas['pH']['name']
    plot3.yaxis.axis_label_text_font_style = "italic"
    plot4.yaxis.axis_label = datas['N2 Mass Flow Controller']['title']
    plot4.yaxis.axis_label_text_font_style = "italic"
    plot5.yaxis.axis_label = datas['Air Mass Flow Controller']['title']
    plot5.yaxis.axis_label_text_font_style = "italic"
    plot1.line(x=sampleSI.index, y=sampleSI[title1], color="navy")
    plot2.line(x=sampleSI.index, y=sampleSI[title2], color="firebrick")
    plot3.line(x=sampleSI.index, y=sampleSI[title3], color="#28D0B4", line_width=2)
    plot4.line(x=sampleSI.index, y=sampleSI[title4], color="orange")
    plot5.line(x=sampleSI.index, y=sampleSI[title5], color="black")
    p = gridplot([[plot1, plot2], [plot3, plot4], [plot5, None]])
    return p


# def update_plot(attrname, old, new):
#     data_to_plot = data_select.value
#     new_name = datas[data_to_plot]['name']
#     new_df = pd.DataFrame(sampleSI[new_name])
#     # src =
#     make_plot(new_name, plot)


data_to_plot = 'DO'
datas = {
    'DO': {
        'name': 'DO mg/L',
        'title': 'Dissolved Oxygen (mg/L)'
    },
    'pH': {
        'name': 'pH',
        'title': 'pH'
    },
    'Ammonium': {
        'name': 'Ammonium',
        'title': 'NH4 Conc. (mg/L)'
    },
    'N2 Mass Flow Controller': {
        'name': 'N2 Mass Flow Controller',
        'title': 'N2 Flow Rate (SCCM)'
    },
    'Air Mass Flow Controller': {
        'name': 'Air Mass Flow Controller',
        'title': 'Air Flow Rate (SCCM)'
    }
}

# data_select = Select(value=data_to_plot, title='Data', options=sorted(datas.keys()))
plot = make_plot(datas['DO']['name'], plot1, datas['Ammonium']['name'], plot2, datas['pH']['name'], plot3,
                 datas['N2 Mass Flow Controller']['name'], plot4, datas['Air Mass Flow Controller']['name'], plot5)
# data_select.on_change('value', update_plot)
#
# controls = VBox(data_select)

curdoc().add_root(HBox(plot))
output_file("bokehplot.html", title="Bokeh Line Plot")
show(HBox(plot))

# Set up streaming for data plots.
# while True:
#     # Somehow need to update the data of the source object "source"
#
#     # Store the updated source on the server
#     curdoc().store_objects(source)
#     time.sleep(0.5)
