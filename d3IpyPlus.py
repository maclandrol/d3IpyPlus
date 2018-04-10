from IPython.core.display import display, HTML, Javascript

import json
import pandas as pd
import pprint
import os

def rgb2hexcolor(r, g, b):
    """Convert 3 integer r, g, b values into hexadecimal #ff00ac format color."""
    return '#' + ''.join('{:02x}'.format(a) for a in [int(r), int(g), int(b)])


class Raw(str):
    """Placeholder class that's the same as a string BUT is treated specially
    by to_js and not quoted."""
    pass


def to_js(indata):
    if isinstance(indata, basestring):
        return "'{}'".format(indata)
    if isinstance(indata, list):
        return "[" + ",".join(to_js(x) for x in indata) + "]"
    if type(indata) == bool:
        return "{}".format(indata).lower()
    if type(indata) in [float, int]:
        return "{}".format(indata)
    if isinstance(indata, dict):
        return "{" + ",".join(to_js(k)+": "+to_js(v) for k, v in indata.items()) + "}"
    elif isinstance(indata, Raw):
        return str(indata)
    else:
        raise ValueError("""Cannot convert object to Javascript. Unsupported format""")


class PyD3Plus(object):

    JS_LIBS = ['http://www.d3plus.org/js/d3.js',
               'http://www.d3plus.org/js/d3plus.js']

    def __init__(self, container="d3viz", height=500, width=500, legend=False, **kwargs):
        self.container_id = container
        self.height = height
        self.width = width
        self.css = ""
        self.js = ""
        self.legend = legend
        self._create_container()
    
    def setCSS(self, css):
        try:
            val = open(css).read()
            css = val
        except:
            pass
        self.css = css.strip().lstrip('<style>').rstrip('</style>')


    def setJS(self, js):
        try:
            val = open(js).read()
            js = val
        except:
            pass
        self.js = js.strip().lstrip('<style>').rstrip('</style>')


    def _create_container(self):
        container = """<div id='{cont}' style='height:{height}px;width:{width}px'></div>"""\
            .format(cont=self.container_id, height=self.height, width=self.width)
        display(HTML(container))

    @classmethod
    def __process_data(df, cols, process_func):
        if cols and isinstance(columns, list):
            df = df[cols]
        if process_func and callable(process_func):
            return process_func(df)
        return df

    @classmethod
    def from_csv(cls, filename, sep=',', columns=None, process_func=None):
        df = pd.read_csv(filename, sep=sep)
        return cls.__process_data(df)

    @classmethod
    def from_json(cls, filename, columns=None, process_func=None):
        df = pd.read_json(filename)
        return cls.__process_data(df)
    
    @classmethod
    def from_np2d(cls, nparray):
        pass


    def format_data(self, data):
        if type(data) == pd.DataFrame:
            return data.to_json(orient='records')
        elif isinstance(data, list) and len(data) > 0 and type(data[0]) == dict:
            return json.dumps(data)
        elif isinstance(data, basestring):
            return data
        else:
            raise ValueError("Cannot handle your input data")       

    def draw(self, data):
        """Draw a visualization in an ipython notebook."""
        json_data = self.format_data(data)
        display(self.generate_js(json_data))

    def dump_html(self, data, container_id=None):
        """Dump a single-file self-contained html string designed to be loaded
        up into the browser on its own or embedded in a page."""
        json_data = self.format_data(data)

        html_template = """
        {scripts}
        <div id='{container_id}'></div>
        <style>
        {css}
        </style>
        <script>
        {js}
        {code}
        </script>
        """
        script_template = "<script src='{src}' type='text/javascript'></script>"

        scripts = "".join([script_template.format(src=x) for x in self.JS_LIBS])
        code = self.generate_js(json_data).data

        return html_template.format(container_id=self.container_id, scripts=scripts, css=self.css, js=self.js, code=code)

    def generate_js(self, json_data):
        raise NotImplementedError()



class GenericPlot(PyD3Plus):
    def __init__(self, id, ptype=None, **kwargs):
        super(GenericPlot, self).__init__(**kwargs)
        if not ptype:
            ptype = 'tree_map'
        self.ptype = ptype
        self.id = id
        self.__dict__.update(kwargs) # yeah, i dont have trust issue

    def _format_params(self):
        params = ""
        for k, v in self.__dict__.items():
            if k not in ['container_id', 'width', 'height', 'ptype', 'js', 'css']:
                params += ".{key}({val})\n".format(key=k, val=to_js(v))
        return Raw(params)

    def generate_js(self, json_data):

        js = """
        (function (){{
          {supjs}
          var viz_data = {viz_data};

          var visualization = d3plus.viz()
          .container({container})
          .type({ptype})
          .id({id})
          {dtformat}
          .data(viz_data)
          .draw();

        }})();
        """.format(
            supjs=Raw(self.js),
            viz_data=json_data,
            container=to_js("#" + self.container_id),
            ptype=to_js(self.ptype),
            id=to_js(self.id),
            dtformat=self._format_params()
        )
        return Javascript(lib=self.JS_LIBS, data=js, css=self.css)



class Treemap(PyD3Plus):

    def __init__(self, id=['group', 'id'], value="value", name=None, color=None, tooltip=[], **kwargs):
        super(Treemap, self).__init__(**kwargs)
        self.id = id
        if name is None:
            self.name = id
        else:
            self.name = name
        if color is None:
            self.color = id
        else:
            self.color = color
        self.value = value
        self.tooltip=tooltip

    def generate_js(self, json_data):

        js = """
        (function (){{

          var viz_data = {viz_data};

          var visualization = d3plus.viz()
          .legend({legend})
          .container({container})
          .type("tree_map")
          .size({{
            'value': {value},
            'threshold': false
          }})
          .id({id})
          .color({color})
          .text({text})
          .tooltip({tooltip})
          .depth(1)
          .data(viz_data)
          .draw();

        }})();
        """.format(
            viz_data=json_data,
            container=to_js("#" + self.container_id),
            id=to_js(self.id),
            value=to_js(self.value),
            color=to_js(self.color),
            legend=to_js(self.legend),
            text=to_js(self.name),
            tooltip=to_js(self.tooltip)
        )

        return Javascript(lib=self.JS_LIBS, data=js, css=self.css)


class Scatterplot(PyD3Plus):

    def __init__(self, x="x", y="y", id="id", name=None, color=None, size=10, tooltip=[], **kwargs):
        super(Scatterplot, self).__init__(**kwargs)
        self.id = id
        self.x = x
        self.y = y
        if name is None:
            self.name = id
        else:
            self.name = name
        if color is None:
            self.color = id
        else:
            self.color = color
        self.size=size
        self.tooltip=tooltip

    def generate_js(self, json_data):
        js = """
        (function (){{

          var viz_data = {viz_data};

          var visualization = d3plus.viz()
          .data(viz_data)
          .legend({legend})
          .container({container})
          .type("scatter")
          .id({id})
          .color({color})
          .text({text})
          .tooltip({tooltip})
          .x({x})
          .y({y})
          .depth(1)
          .size({size})
          .draw();

        }})();
        """.format(
            viz_data=json_data,
            container=to_js("#" + self.container_id),
            id=to_js(self.id),
            size=to_js(self.size),
            color=to_js(self.color),
            text=to_js(self.name),
            x=to_js(self.x),
            y=to_js(self.y),
            legend=to_js(self.legend),
            tooltip=to_js(self.tooltip)
        )

        return Javascript(lib=self.JS_LIBS, data=js, css=self.css)



class Lineplot(PyD3Plus):

    def __init__(self, id="id", x="x", y="y", name=None, color=None, tooltip=[], **kwargs):
        super(Lineplot, self).__init__(**kwargs)
        self.id = id
        self.x = x
        self.y = y
        if name is None:
            self.name = id
        else:
            self.name = name
        if color is None:
            self.color = id
        else:
            self.color = color
        self.tooltip=tooltip

    def generate_js(self, json_data):
        js = """
        (function (){{

          var viz_data = {viz_data};

          var visualization = d3plus.viz()
          .data(viz_data)
          .legend({legend})
          .container({container})
          .type("line")
          .id({id})
          .color({color})
          .text({text})
          .tooltip({tooltip})
          .x({x})
          .y({y})
          .draw();

        }})();
        """.format(
            viz_data=json_data,
            container=to_js("#" + self.container_id),
            id=to_js(self.id),
            color=to_js(self.color),
            text=to_js(self.name),
            tooltip=to_js(self.tooltip),
            x=to_js(self.x),
            y=to_js(self.y),
            legend=to_js(self.legend)
        )

        return Javascript(lib=self.JS_LIBS, data=js, css=self.css)