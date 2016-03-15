"""
Written By: Michael Newton, Alex Baryshev
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Uses Bokeh to plot streaming data from Bioreactor

To Do:
+ Incorporate changes from bokehplot_test_alex.py to allow for good demonstration of streaming data.
"""
import os
import sys

import pandas as pd
from bokeh.client import push_session
from bokeh.plotting import Figure, output_server, curdoc, gridplot
from downloader import download_latest

# Prepare output to server
output_server("BioReactor_Data_Logging")

# Retrieves latest updated data file from google drive
curdir = os.path.join(__file__, os.pardir)
pardir = os.path.join(curdir, os.pardir)
py27dir = os.path.abspath(pardir) + '/py27googledriveconnect'
sys.path.insert(0, py27dir)

datafile = os.path.abspath(pardir) + '/Data_Management/R1data'
download_latest(1, 'R1data')

# Accept/Setup Dataframe to be Plotted
sample_data_live = datafile
sample = pd.read_csv(sample_data_live, parse_dates=[0])
sampleSI = sample.set_index('Date')
# sampleSI = sampleSI.tail(100)

# Initialize plot figures
plot1 = Figure(x_axis_type="datetime", plot_width=650, y_range=(0, 5))
plot2 = Figure(x_axis_type="datetime", plot_width=650, y_range=(0, 80))
plot3 = Figure(x_axis_type="datetime", plot_width=650, y_range=(6.5, 8.5))
plot4 = Figure(x_axis_type="datetime", plot_width=650, y_range=(-50, 550))
plot5 = Figure(x_axis_type="datetime", plot_width=650)


# Make plot function for each of the desired data sets.
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

# Create a dictionary of names and titles for each important data set.
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

# Initial call to plot function.
plot = make_plot(datas['DO']['name'], plot1, datas['Ammonium']['name'], plot2, datas['pH']['name'], plot3,
                 datas['N2 Mass Flow Controller']['name'], plot4, datas['Air Mass Flow Controller']['name'], plot5)

# Push the session to the server
session = push_session(curdoc())


# Update callback function to refresh datasource and plots.
def update():
    datafile = os.path.abspath(pardir) + '/Data_Management/R1data'
    download_latest(1, 'R1data')
    sample_data_live = datafile
    sample = pd.read_csv(sample_data_live, parse_dates=[0])
    sampleSI = sample.set_index('Date')
    # sampleSI = sampleSI.tail(100)
    print sampleSI
    plot1.line(x=sampleSI.index, y=sampleSI['DO mg/L'], color="navy")
    plot2.line(x=sampleSI.index, y=sampleSI[datas['Ammonium']['name']], color="firebrick")
    plot3.line(x=sampleSI.index, y=sampleSI[datas['pH']['name']], color="#28D0B4", line_width=2)
    plot4.line(x=sampleSI.index, y=sampleSI[datas['N2 Mass Flow Controller']['name']], color="orange")
    plot5.line(x=sampleSI.index, y=sampleSI[datas['Air Mass Flow Controller']['name']], color="black")
    p = gridplot([[plot1, plot2], [plot3, plot4], [plot5, None]])
    return p

curdoc().add_periodic_callback(update, 3000)
session.show()

session.loop_until_closed()
