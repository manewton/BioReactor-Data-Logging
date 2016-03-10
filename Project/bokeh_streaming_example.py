import numpy as np
from numpy import pi
from random import shuffle

from bokeh.client import push_session
from bokeh.driving import cosine
from bokeh.plotting import figure, curdoc


p = figure(plot_width=400, plot_height=400)
x = [1, 2, 3, 4, 5]
y = [6, 7, 2, 4, 5]
r2 = p.line(x, y, color="navy", line_width=4)

# open a session to keep our local document in sync with server
session = push_session(curdoc())


def update():
    shuffle(y)
    r2 = p.line(x, y, color="navy", line_width=4)

curdoc().add_periodic_callback(update, 500) # update every 500ms

session.show() # open the document in a browser

session.loop_until_closed() # run forever
