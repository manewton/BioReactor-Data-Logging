''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''

import imp
import os
import pandas as pd
from bokeh.plotting import Figure
from bokeh.models import ColumnDataSource, HBox, VBoxForm, BoxAnnotation
from bokeh.models.widgets import Slider, TextInput, Select
from bokeh.io import curdoc

# Can't import local modules absolutely with bokeh, so doing it relatively
master = imp.load_source('R1datautils', os.getcwd()+'/Project/R1datautils.py')
dload = imp.load_source('downloader', os.getcwd()+'/Project/downloader.py')




# CONSTANTS
CYCLE_TIMING = ['Begin', 'End of Anaerobic', 'End of Aerobic']
CYCLE_COLUMNS = ['Timestamps', 'NO2-', 'NO3-', 'NH4+']
TS = '\nTimestamps'

# Set up data
source = ColumnDataSource(data=dict(x=[],
                                    y1=[], leg1=[],
                                    y2=[], leg2=[],
                                    y3=[], leg3=[]))
# TODO: Use hover tooltips instead of a legend until they figure out legend updating

# R1 Master file:
masterdf = master.save_r1masterfile(False)

# Create Input controls
date_list = masterdf.index.format()
cycle = Select(title='Cycle Date', value='',
               options=date_list)

# Set up plot
plot = Figure(plot_height=400, plot_width=700, title="Select Cycle",
              tools="crosshair,pan,reset,resize,save,wheel_zoom",
              x_axis_type="datetime")
leg1='test'
plot.circle('x', 'y1', source=source, size=10, color='black',
            legend=leg1)
plot.line('x', 'y1', source=source, line_dash=[4, 4], color='black',
          legend=leg1)

plot.square('x', 'y2', source=source, size=10, color='black',
            legend='NH4+ (mgN/L)')
plot.line('x', 'y2', source=source, color='black', legend='NH4+ (mgN/L)')

plot.diamond('x', 'y3', source=source, size=10, color='black',
            legend='NO2- (mgN/L)')
plot.line('x', 'y3', source=source, line_dash=[4, 1], color='black',
            legend='NO2- (mgN/L)')

# Set up legend
plot.legend.location = "left_center"

# Box annotations
aerobic = BoxAnnotation(plot=plot, fill_alpha=0.05, fill_color='gray')
plot.renderers.extend([aerobic])

# Set up callbacks
def update_title(attrname, old, new):
    plot.title = 'Concentrations During\nCycle on %s' % cycle.value

cycle.on_change('value', update_title)

def update_data(attrname, old, new):
    # Define Selected Data
    selected = pd.DataFrame(index=CYCLE_TIMING,
                            columns=CYCLE_COLUMNS)

    # Timestamps
    ts = masterdf.filter(regex=TS).loc[cycle.value]
    ts.rename(index=lambda x: x.replace(TS, ''),inplace=True)
    for idx, each in enumerate(ts):
        selected['Timestamps'].iloc[idx] = masterdf.index[1] + \
                                       pd.DateOffset(hours=each.hour,
                                                     minutes=each.minute)
    #bigdf = dload.get_values_from(1, ts['Begin'], timestamp2=ts['End of Anaerobic'])

    # TODO: This is so super broken egggghhhhh
    # Format Values measured by the gallery
    galvals = masterdf.filter(regex='\nGallery').loc[cycle.value]
    no2 = galvals.filter(regex='NO2-')
    no2.rename(lambda val: val.replace('NO2- (mgN/L)\nGallery - ', ''), inplace=True)
    selected['NO2-'] = no2
    no3 = galvals.filter(regex='NO3-')
    no3.rename(lambda val: val.replace('NO3- (mgN/L)\nGallery - ', ''), inplace=True)
    selected['NO3-'] = no3
    nh4 = galvals.filter(regex='NH4+')
    nh4.rename(lambda val: val.replace('NH4+ (mgN/L)\nGallery - ', ''), inplace=True)
    selected['NH4+'] = nh4
    print selected['NO3-']
    print selected['NH4+']
    print selected['NO2-']
    # Generate the new curve
    source.data = dict(x=selected['Timestamps'],
                       y1=selected['NO3-'],
                       leg1='NO3- mgN/L',
                       y2=selected['NH4+'],
                       y3=selected['NO2-'])

    # Move box annotation
    gas_on = selected['Timestamps'].iloc[1]
    aerobic.right = gas_on.value/10e5
    plot.renderers.extend([aerobic])


for controls in [cycle]:
    controls.on_change('value', update_data)

# Set up layouts and add to document
inputs = VBoxForm(children=[cycle])

curdoc().add_root(HBox(children=[inputs, plot], width=900))


# TODO: Add NH4+, DO, pH, ORP
# TODO: Checkboxes to include what we want
