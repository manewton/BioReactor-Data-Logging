import numpy as np
import pandas as pd
from collections import OrderedDict
from bokeh.plotting import figure
from bokeh.models import Plot, ColumnDataSource
from bokeh.properties import Instance
from bokeh.server.app import bokeh_app
from bokeh.server.utils.plugins import object_page
from bokeh.models.renderers import GlyphRenderer
from bokeh.models.widgets import HBox,Slider,TextInput, VBoxForm, CheckboxGroup

def get_stockdata(ticker):
    MyStock = pd.read_csv(
    "http://ichart.yahoo.com/table.csv?s="+ticker+"&a=0&b=1&c=2000&d=0&e=1&f=2015",
    parse_dates=['Date'])

    xyvalues = OrderedDict(AdjClose=MyStock['Adj Close'],Date=MyStock['Date'])
    for x in xyvalues.keys():
        xyvalues[x] =xyvalues[x][::-1]

    return xyvalues

def movingaverage(values,window):
    weigths = np.repeat(1.0, window)/window
    smas = np.convolve(values, weigths, 'valid')
    return smas # as a numpy array



class HackApp(HBox):

    extra_generated_classes = [["HackApp", "HackApp", "HBox"]]

    inputs = Instance(VBoxForm)

    text = Instance(TextInput)

    toggle = Instance(CheckboxGroup)
    MVA_1 = Instance(Slider)
    MVA_2 = Instance(Slider)


    plot = Instance(Plot)
    source = Instance(ColumnDataSource)
    source2 = Instance(ColumnDataSource)
    source3 = Instance(ColumnDataSource)

    @classmethod
    def create(cls):

        obj = cls()

        obj.source = ColumnDataSource(data=dict(x_y=[], y=[]))
        obj.source2 = ColumnDataSource(data=dict(x_z=[], z=[]))
        obj.source3 = ColumnDataSource(data=dict(x_a=[], a=[]))

        obj.text = TextInput(
            title="title", name='title', value='MSFT'
        )

        obj.toggle = CheckboxGroup( labels=["Closes","MVA_1","MVA_2"],active=[0,1,2])

        obj.MVA_1 = Slider(
            title="MVA_1", name='MVA_1',
            value=100, start=-0.0, end=500.0, step=10
        )
        obj.MVA_2 = Slider(
            title="MVA_2", name='MVA_2',
            value=200, start=-0.0, end=500.0, step=10
        )


        toolset = "crosshair,pan,reset,resize,save,wheel_zoom"


        plot = figure(title_text_font_size="12pt",
                      plot_height=400,
                      plot_width=400,
                      tools=toolset,
                      title=obj.text.value,
                      x_axis_type = "datetime"
        )




        plot.line('x_y', 'y', source=obj.source,
                  line_width=3,
                  line_alpha=0.6,
                  line_color="red",
                  name='closes'
        )

        plot.line('x_z', 'z', source=obj.source2,
                  line_width=3,
                  line_alpha=0.6,
                  line_color="blue",
                  name='av1'
        )

        plot.line('x_a', 'a', source=obj.source3,
                  line_width=3,
                  line_alpha=0.6,
                  line_color="green",
                  name='av2'
        )

        obj.plot = plot
        obj.update_data()

        obj.inputs = VBoxForm(
            children=[
                obj.text,
                obj.toggle,
                obj.MVA_1,
                obj.MVA_2,

            ]
        )

        obj.children.append(obj.inputs)
        obj.children.append(obj.plot)

        return obj

    def checkbox_handler(self,active):

        for n,nm in enumerate(['closes','av1','av2']):
            sel=self.plot.select(dict(name=nm))
            sel[0].glyph.line_alpha= 1 if n in self.toggle.active else 0


    def setup_events(self):

        super(HackApp, self).setup_events()
        if not self.text:
            return


        self.text.on_change('value', self, 'input_change')


        for w in ["MVA_1", "MVA_2"]:
            getattr(self, w).on_change('value', self, 'input_change')

        self.toggle.on_click(self.checkbox_handler)


    def input_change(self, obj, attrname, old, new):

        self.update_data()
        self.plot.title = self.text.value

    def update_data(self,hide=False):

        N = 200


        a=1
        b = self.MVA_1.value
        b2 = self.MVA_2.value


        print(self.toggle.active,"self.toggle")

        ticker  = self.text.value
        xyvalues=get_stockdata(ticker)

        y_min = min(xyvalues['AdjClose'] )*0.9
        y_max = max(xyvalues['AdjClose'])*1.1

        MA1 = b
        MA2 = b2

        Av1 = movingaverage(xyvalues['AdjClose'], MA1)
        Av2 = movingaverage(xyvalues['AdjClose'], MA2)
        SP1 = len(xyvalues['Date'][MA1-1:])
        SP2 = len(xyvalues['Date'][MA2-1:])
        Av1=Av1[-SP1:]
        Av2=Av2[-SP2:]
        avgdate1=xyvalues['Date'] [-SP1:]
        avgdate2=xyvalues['Date'] [-SP2:]






        x_y = []
        y = []
        x_z = []
        z = []
        x_a = []
        a = []

        for p in self.toggle.active:
            if p ==0:
                x_y = xyvalues['Date']
                y = xyvalues['AdjClose']
            if p ==1:
                x_z = avgdate1
                z = Av1
            if p ==2:
                x_a = avgdate2
                a = Av2



        self.source.data = dict(x_y=x_y, y=y)
        self.source2.data = dict(x_z=x_z, z=z)
        self.source3.data = dict(x_a=x_a, a=a)
        self.plot.y_range.start=y_min
        self.plot.y_range.end=y_max


@bokeh_app.route("/bokeh/hack/")
@object_page("sin")
def make_hack():
    app = HackApp.create()
    return app