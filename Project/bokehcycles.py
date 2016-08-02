''' Present an interactive function explorer with slider widgets.
Scrub the sliders to change the properties of the ``sin`` curve, or
type into the title text box to update the title of the plot.
Use the ``bokeh serve`` command to run the example by executing:
    bokeh serve sliders.py
at your command prompt. Then navigate to the URL
    http://localhost:5006/sliders
in your browser.
'''

import pandas as pd
import datetime
from bokeh.plotting import figure
from bokeh.layouts import row, widgetbox
from bokeh.models import ColumnDataSource, BoxAnnotation
from bokeh.models.widgets import CheckboxGroup, Select
from bokeh.io import curdoc
from bokeh.models import LinearAxis, Range1d, Label
from R1datautils import save_r1masterfile, build_cycleprobedf,\
    build_cyclemeasuredf




# Simplify function calls
build_probedf = build_cycleprobedf
build_measuredf = build_cyclemeasuredf

# CONSTANTS
IGNORE_BEFORE = '5-22-16'

# Name next to checkbox: [Name of column in df, key name in visibility dict]
MEASURE_LABELS = {'NO2-': ['NO2-', 'no2'],
                  'NO3-': ['NO3-', 'no3'],
                  'NH4+': ['NH4+', 'nh4']}
PROBE_LABELS = {'Dissolved Oxygen': ['DO mg/L', 'do'],
               'NH4+ Probe': ['NH4 mg/L' ,'nh4_probe'],
               'pH': ['pH','ph'],
               'ORP': ['ORP mV', 'orp']}

# Define Defaults to plot
DEFAULT_PROBES = [0, 3]
DEFAULT_MEASURED = [0, 1, 2]

# Dictionaries to contain plot and visibility parameters
DEFAULT_PLOT_PARAMS = dict(status='Successful', start_aerobic=0,
                           y_axis_range=(0, 0), y_axis2_alpha=0,
                           y_axis2_max=100, title='Select Cycle')
DEFAULT_VISIBLE = dict(no2=[None, 0], no3=[None, 0], nh4=[None, 0],
                       do=[None, 0], nh4_probe=[None, 0], ph=[None, 0],
                       orp=[None, 0])

# To turn things off, set them too this in a visible dict
OFF = [None, 0]




# TODO: Checkboxes to include what we want <--
# TODO: make legend its own figure
# TODO: Hover Tool Tips
# TODO: Update documentation & cleanup
# TODO: Control & Calibrator Tools (date range slider?)
# TODO: Live plotting & long term performance evaluation plots

# Get List of Dates for dropdown menu
masterdf = save_r1masterfile(True)
masterdf = masterdf[masterdf.index > IGNORE_BEFORE]
date_list = masterdf.index.format()

# Create Controls
cycle = Select(title='Cycle Date', value=date_list[-1],
               options=date_list)
probes = CheckboxGroup(labels=PROBE_LABELS.keys(),
                       active=DEFAULT_PROBES,
                       disabled=False)
measure = CheckboxGroup(labels=MEASURE_LABELS.keys(),
                        active=DEFAULT_MEASURED)


def get_to_plot(what_to_plot, probe):
    """
    Loops through checked boxes and returns names of columns requested to plot
    :param what_to_plot: list of ints, taken from checkboxgroup.active
    :param probe: boolean, true to look at probe data false for measured.
    :return: List of strs, names of columns in dataframe
    """
    to_plot = []
    # If we want probe data, look at probe labels for that checkbox group
    if probe:
        for each in what_to_plot:
            to_plot.append(PROBE_LABELS.keys()[each])  # Return checkbox label
    else:  # Else look at measured check box group labels
        for each in what_to_plot:
            to_plot.append(MEASURE_LABELS.keys()[each])  # Return cbox label
    return to_plot


def get_all_to_plot(what_to_plot_probe, what_to_plot_measure):
    to_plot_probe = get_to_plot(what_to_plot_probe, True)
    to_plot_measure = get_to_plot(what_to_plot_measure, False)
    return to_plot_probe, to_plot_measure


def turn_on(parameter):
    # return column names to be used as legend labels
    if parameter in PROBE_LABELS:
        legend_label = PROBE_LABELS[parameter][0]
    elif parameter in MEASURE_LABELS:
        legend_label = MEASURE_LABELS[parameter][0] + ' mgN/L'
    else:
        raise
    on = [legend_label, 1]
    return on


def set_visibile(to_plot_probe, to_plot_measure):
    """
    Uses the to_plot function to set visibility of plots and adjust legend
    :param what_to_plot_probe: list of ints, taken from probe checkbox group
    :param what_to_plot_measure: list of ints, from measure checkbox group
    :param data: probe or measured data column source dictionary to write to
    :return: list of strs, things we want plotted
    """
    new_visible = DEFAULT_VISIBLE
    for each in new_visible:
        # THe error is here right now
        if each in to_plot_probe:
            new_visible[each] = turn_on(each)
        elif each in to_plot_measure:
            new_visible[each] = turn_on(each)
        else:
            new_visible[each] = OFF
    return new_visible


def get_y_axis_max(to_plot_probe, to_plot_measure, probe_data, measure_data):
    y_axis_max = 0
    for each in to_plot_measure:
        y_axis_max = max(max(measure_data[MEASURE_LABELS[each][0]])*1.1,
                         y_axis_max)
    if to_plot_probe is not []:
        for each in to_plot_probe:
            if each is not 'ORP':
                y_axis_max = max(max(probe_data[PROBE_LABELS[each][0]])*1.1,
                                 y_axis_max)
    return y_axis_max


def get_plot_new_date(what_to_plot_probe, what_to_plot_measure, date):
    plot_params = DEFAULT_PLOT_PARAMS
    # Name the plot
    plot_params['title'] = 'Concentrations During\nCycle on %s' % date
    # Get parameters to plot
    to_plot_probe, to_plot_measure = get_all_to_plot(what_to_plot_probe,
                                                     what_to_plot_measure)
    # With the new date, update the measured data column dict source
    measure_data = build_measuredf(date)
    # Return the probe data if requested
    if to_plot_probe == []:
        # Inform status and use sample timing to find aerobic phase start time
        plot_params['status'] = 'No Probe Data Requested'
        plot_params['start_aerobic'] = measure_data['x'][1]
        probe_data = build_probedf(date, True)  # Get a blank probe df
    else:
        probe_data, start_aerobic, available = build_probedf(date)
        plot_params['start_aerobic'] = start_aerobic
        # If there was no probe data collected during that cycle, say so.
        if available:
            plot_params['status'] = 'Successful'
        else:
            plot_params['status'] = 'Probe data for this cycle not available.'
            to_plot_probe = []
    visible = set_visibile(to_plot_probe, to_plot_measure)

    # If we have probe data, use that to determine y axis max too
    ymax = get_y_axis_max(to_plot_probe,
                          to_plot_measure,
                          probe_data,
                          measure_data)
    # define the y axis range
    plot_params['y_axis_range'] = (0, ymax)
    # Do we need a 2nd axis b/c we are plotting ORP? What is req'd range?
    plot_params['y_axis2_alpha'] = True if 'ORP' in to_plot_probe else False
    if plot_params['y_axis2_alpha'] is True:
        plot_params['y_axis2_max'] = max(probe_data['ORP mV'])*1.05
    all_dicts = [plot_params, visible, probe_data, measure_data]
    return all_dicts


# Get data for intial plot.
all_dicts = get_plot_new_date(DEFAULT_PROBES, DEFAULT_MEASURED, date_list[-1])
plot_d = all_dicts[0]
visible_d = all_dicts[1]
probe_source = ColumnDataSource(data=all_dicts[2])
measured_source = ColumnDataSource(data=all_dicts[3])

# Set up plot
#TODO: Double check plot params got set properly
plot = figure(plot_height=400, plot_width=650, title=plot_d['title'],
              tools="crosshair,pan,reset,save,wheel_zoom",
              x_axis_type='datetime', y_range=plot_d['y_axis_range'])
plot.xaxis.axis_label = 'Time'
plot.yaxis.axis_label = 'Concentraton, mg/L or pH'
#status_display = figure(plot_height=100, plot_width=650)
#citation = Label(text=plot_d['status'],
#                 border_line_color='black')
#status_display.add_layout(citation)


# Set up 2nd Y axis
# plot.extra_y_ranges = {'ORP': Range1d(start=0, end=plot_d['y_axis2_max'])}
# plot.add_layout(LinearAxis(y_range_name='ORP', axis_label='ORP, mV'), 'left')

# Define all plots
no3_pts = plot.circle('Timestamps', 'NO3-', source=measured_source,
                      size=10, color='black',
                      legend=visible_d['no3'][0], alpha=visible_d['no3'][1])
no3_line = plot.line('Timestamps', 'NO3-', source=measured_source,
                     line_dash=[10, 10], color='black',
                     legend=visible_d['no3'][0], alpha=visible_d['no3'][1])

nh4_pts = plot.square('Timestamps', 'NH4+', source=measured_source,
            size=10, color='black',
            legend=visible_d['nh4'][0], alpha=visible_d['nh4'][1])
nh4_line = plot.line('Timestamps', 'NH4+', source=measured_source,
          color='black',
          legend=visible_d['nh4'][0], alpha=visible_d['nh4'][1])

no2_pts = plot.diamond('Timestamps', 'NO2-', source=measured_source,
             size=10, color='black',
             legend=visible_d['no2'][0], alpha=visible_d['no2'][1])
no2_line = plot.line('Timestamps', 'NO2-', source=measured_source,
          line_dash=[2, 10], color='black',
          legend=visible_d['no2'][0], alpha=visible_d['no2'][1])

# Probe Plots
do_line = plot.line('Date', 'DO mg/L', source=probe_source,
                    color='black',
                    legend=visible_d['do'][0], alpha=visible_d['do'][1])
ph_line = plot.line('Date', 'pH', source=probe_source,
                    color='black',  line_width=3,
                    legend=visible_d['ph'][0], alpha=visible_d['ph'][1])
#orp_line = plot.line('Date', 'ORP mV', source=probe_source, # ORP - Plot 7
#                     color='grey',  y_range_name='ORP',
#                     legend=visible_d['orp'][0], alpha=visible_d['orp'][1])
nh4_probe_line = plot.line('Date', 'NH4 mg/L', source=probe_source,
                           color='black', line_width=2,
                           legend=visible_d['nh4_probe'][0],
                           alpha=visible_d['nh4_probe'][1])

# Set up legend
plot.legend.location = 'left_center'
plot.legend.label_text_font_size = '8pt'
plot.legend.background_fill_alpha = 0.5

# Box annotations

aerobic = BoxAnnotation(plot=plot,
                        fill_alpha=0.05,
                        fill_color='gray',
                        right=plot_d['start_aerobic'].value/10e5)
plot.renderers.extend([aerobic])

# Set up callbacks

def update_date(attrname, old, new):
    # Get updated data if we changed the cycle we're looking at:

    all_dicts = get_plot_new_date(probes.active, measure.active, str(new))

    plot_d = all_dicts[0]
    visible_d = all_dicts[1]

    new_probe = ColumnDataSource(data=all_dicts[2])
    new_measure = ColumnDataSource(data=all_dicts[3])

    probe_source.data = new_probe.data
    measured_source.data = new_measure.data
    print 'hey'
    # Assign new data dictionaries
    plot.title.text = plot_d['title']
    plot.y_range = Range1d(start=0, end=plot_d['y_axis_range'][1])
    print 'hey2'
    #plot.extra_y_ranges = y_axis2
    #plot.add_layout(LinearAxis(y_range_name='ORP', axis_label='ORP, mV'),
    #                'right')
    aerobic.right = plot_d['start_aerobic'].value/10e5
    print 'hey3'
    # Find all the plots associated with a given visibility status
    vis_glyphs = {each: [] for each in visible_d.keys()}
    for each in plot.renderers:
        if each.level is 'glyph':
            name = each.glyph.y
            # Use y column name to find visibility dictionary entry
            if name in MEASURE_LABELS.keys():
                for each2 in MEASURE_LABELS:
                    if name in MEASURE_LABELS[each2]:
                        vis_name = MEASURE_LABELS[each2][1]
                        break
            else:
                for each2 in PROBE_LABELS:
                    if name in PROBE_LABELS[each2]:
                        vis_name = PROBE_LABELS[each2][1]
                        break
            for each2 in vis_glyphs:
                if each2 == vis_name:
                    vis_glyphs[each2].append(each)
    # TODO: Set visibility programatically
    legend = plot.legend[0].legends
    legend = []
    for each in visible_d:
        # Set visibility of all plots
        for each2 in vis_glyphs[each]:
            each2.glyph.line_alpha = visible_d[each][1]
            try:
                each2.glyph.fill_alpha = visible_d[each][1]
            except:
                continue
        if visible_d[each] == OFF:
            continue
        else:
            legend.append((visible_d[each][0], vis_glyphs[each]))
    plot.legend[0].legends = legend

    #[orp_line.legend, orp_line.alpha] = visible_d['orp']
cycle.on_change('value', update_date)

# Set up layouts and add to document
inputs = widgetbox(cycle, probes, measure)

curdoc().add_root(row(inputs, plot, width=1200))
curdoc().title = "Reactor 1 Cycle Test Visualization"
