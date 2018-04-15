## D3IpyPlus
[![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/maclandrol/d3IpyPlus/master?filepath=example%2Fd3ipyplus_example.ipynb)

This repository is an experiment trying to incorporate D3 into IPython Notebook (Jupyter). The main objective is to take advantage of Jupyter's interface which enables manipulation of the DOM, to build interactive, JavaScript-powered plots. 

### Why ?

Because IPython Notebook is really convenient. In fact, since the notebook support markdown, HTML (through ```IPython.core.display```) in addition to python/julia/R type cells, it is suitable for writing a complete blog post or a web-oriented scientific essay with only little post-editing needed. Therefore, it would be nice to have a way to automatically incorporate interactive graphs in it, by writing python code. There are actually ways to perfom such task :

- [d3py](https://github.com/mikedewar/d3py)
- [vincent](https://github.com/wrobstory/vincent/)
- [Altair](https://github.com/altair-viz/altair_notebooks)
- [PyGal](http://pygal.org/en/stable/)
- [vispy](https://github.com/vispy/vispy)
- [Plotly](https://plot.ly/python/ipython-notebook-tutorial/)
- [holoviews](https://holoviews.org)
- [Bokeh](https://bokeh.pydata.org/en/latest/). 
- etc

All of them are pretty good, and if you are reading this, you have probably already heard of them. Truthfully, you should try either [Altair](https://github.com/altair-viz/altair_notebooks) or [holoviews](https://holoviews.org), if you are looking for a well maintained package that will prove useful in the long term.

D3IpyPlus's plots are based on [D3plus](https://d3plus.org) which has a nice API, and is much easier to work with than __d3js__. The main idea was inspired from https://github.com/cid-harvard/visualization-notebook-templates. 


### Basic ScatterPlot Example

Don't forget that this will only works in Ipython notebook.

```python
from D3IpyPlus import ScatterPlot

sample_data = [
    {"value": 100, "weight": .45, "type": "alpha"},
    {"value": 70, "weight": .60, "type": "beta"},
    {"value": 40, "weight": -.2, "type": "gamma"},
    {"value": 15, "weight": .1, "type": "delta"}
 ]

# you can pass a container_id parameter, that will correspond to 
# the id of the div to which your plot will be attached
# Alternatively, a unique div id will be automatically generated if the argument is missing.
scplot = ScatterPlot(x='value', y='weight', id='type', width=600, size=10)
# The following will display the plot inside the notebook
scplot.draw(sample_data)
# You can also dump html source corresponding to the plot
print(scplot.dump_html(sample_data))
# which will output the following html
```
```html
    <script src='http://www.d3plus.org/js/d3.js' type='text/javascript'></script>
    <script src='http://www.d3plus.org/js/d3plus.js' type='text/javascript'></script>
    <div id='d3viz_1'></div>
    <style>
        
    </style>
    <script>
        
        
    (function (){
        
        var viz_data = [{"type": "alpha", "weight": 0.45, "value": 100}, {"type": "beta", "weight": 0.6, "value": 70}, {"type": "gamma", "weight": -0.2, "value": 40}, {"type": "delta", "weight": 0.1, "value": 15}];

        var visualization = d3plus.viz()
            .container('#d3viz_1')
            .type('scatter')
            .color('type')
	.text('type')
	.y('weight')
	.x('value')
	.id('type')
	.size(10)
            .data(viz_data)
            .draw();

    })();
    
    </script>
```

### Detailed examples

Detailed examples are available in the [example](/example) folder. A Binder link is also available if you want a live version (click on the badge) [![Binder](https://mybinder.org/badge.svg)](https://mybinder.org/v2/gh/maclandrol/d3IpyPlus/master?filepath=example%2Fd3ipyplus_example.ipynb)






