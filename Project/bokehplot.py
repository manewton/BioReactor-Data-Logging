"""
Written By: Michael Newton, Alex Baryshev
For: Winkler Lab/CSE599 Winter Quarter 2016
Purpose: Uses Bokeh to plot streaming data from Bioreactor

Requirements:
        - Accepts a .csv file named R1data.csv located in google drive
        - Requires Python 2.7 to interface with pydrive API
        - File must be run from command line first starting the Bokeh server
            -- Then call this file from command line
"""
import os
import imp
import datetime
import pandas as pd
from bokeh.client import push_session
from bokeh.plotting import Figure, output_server, curdoc, gridplot
dl = imp.load_source('downloader', os.getcwd() +
                          '/Project/downloader.py')


# Prepare output to server
output_server("BioReactor_Data_Logging")

# Retrieves latest updated data file from google drive
three_hours_ago = datetime.datetime.now()-datetime.timedelta(hours=3)
now = datetime.datetime.now()
R1_data_frame = dl.get_values_from(1, now, three_hours_ago)

x_low = R1_data_frame.index[1]
x_high = R1_data_frame.index[-1]
n_min = 2

# Initialize plot figures
DO_plot = Figure(x_axis_type="datetime", plot_width=450, plot_height=400,
                 x_range=[x_low - pd.DateOffset(minutes=n_min), x_high + pd.DateOffset(minutes=n_min)],
                 y_range=[0, 8])
NH4_plot = Figure(x_axis_type="datetime", plot_width=450, plot_height=400,
                  x_range=[x_low - pd.DateOffset(minutes=n_min), x_high + pd.DateOffset(minutes=n_min)],
                  y_range=[0, 1])
pH_plot = Figure(x_axis_type="datetime", plot_width=450, plot_height=400,
                 x_range=[x_low - pd.DateOffset(minutes=n_min), x_high + pd.DateOffset(minutes=n_min)],
                 y_range=[0, 14])
N2_MFC_plot = Figure(x_axis_type="datetime", plot_width=450, plot_height=400,
                     x_range=[x_low - pd.DateOffset(minutes=n_min), x_high + pd.DateOffset(minutes=n_min)],
                     y_range=[0, 500])
Air_MFC_plot = Figure(x_axis_type="datetime", plot_width=450, plot_height=400,
                      x_range=[x_low - pd.DateOffset(minutes=n_min), x_high + pd.DateOffset(minutes=n_min)],
                      y_range=[0, 500])


# Make plot function for each of the desired data sets.
def make_plot(title1, plot1, title2, plot2, title3, plot3, title4, plot4, title5, plot5, sample_df):
    plot1.title = title1
    plot2.title = title2
    plot3.title = title3
    plot4.title = title4
    plot5.title = title5
    plot1.yaxis.axis_label = data_dict['DO']['title']
    plot1.yaxis.axis_label_text_font_style = "italic"
    plot2.yaxis.axis_label = data_dict['Ammonium']['title']
    plot2.yaxis.axis_label_text_font_style = "italic"
    plot3.yaxis.axis_label = data_dict['pH']['name']
    plot3.yaxis.axis_label_text_font_style = "italic"
    plot4.yaxis.axis_label = data_dict['N2 Mass Flow Controller']['title']
    plot4.yaxis.axis_label_text_font_style = "italic"
    plot5.yaxis.axis_label = data_dict['Air Mass Flow Controller']['title']
    plot5.yaxis.axis_label_text_font_style = "italic"
    plot1.line(x=sample_df.index, y=sample_df[title1], color="navy")
    plot2.line(x=sample_df.index, y=sample_df[title2], color="firebrick")
    plot3.line(x=sample_df.index, y=sample_df[title3], color="#28D0B4", line_width=2)
    plot4.line(x=sample_df.index, y=sample_df[title4], color="orange")
    plot5.line(x=sample_df.index, y=sample_df[title5], color="black")
    p = gridplot([[plot1, plot2, plot3], [plot4, plot5, None]])
    return p


# Create a dictionary of names and titles for each important data set.
# TODO: Update this
data_dict = {
    'DO': {
        'name': 'DO mg/L',
        'title': 'Dissolved Oxygen (mg/L)'
    },
    'pH': {
        'name': 'pH',
        'title': 'pH'
    },
    'Ammonium': {
        'name': 'NH4 mg/L',
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
plot = make_plot(data_dict['DO']['name'], DO_plot,
                 data_dict['Ammonium']['name'], NH4_plot,
                 data_dict['pH']['name'], pH_plot,
                 data_dict['N2 Mass Flow Controller']['name'], N2_MFC_plot,
                 data_dict['Air Mass Flow Controller']['name'], Air_MFC_plot, R1_data_frame)

# Push the session to the server
session = push_session(curdoc())


# Update callback function to refresh data source and plots.
def update():
    three_hours_ago = datetime.datetime.now()-datetime.timedelta(hours=3)
    now = datetime.datetime.now()
    data_frame = dl.get_values_from(1, now, three_hours_ago)
    make_plot(data_dict['DO']['name'], DO_plot,
              data_dict['Ammonium']['name'], NH4_plot,
              data_dict['pH']['name'], pH_plot,
              data_dict['N2 Mass Flow Controller']['name'], N2_MFC_plot,
              data_dict['Air Mass Flow Controller']['name'], Air_MFC_plot, data_frame)

curdoc().add_periodic_callback(update, 1)
session.show()
session.loop_until_closed()
