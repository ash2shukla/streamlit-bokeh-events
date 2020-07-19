# Bokeh Plot Events
A streamlit component for bi-directional communication with bokeh plots.

#### Its just a workaround till streamlit team releases support for bi-directional communication with plots.

## Demo

![demo](assets/demo.gif)

## Installation

```bash
pip install bokeh-plot-events
```
## Usage

```python
import streamlit as st
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS

# import function
from bokeh_plot_events import bokeh_plot_events

# create plot
p = figure(tools="lasso_select")
cds = ColumnDataSource(
    data={
        "x": [1, 2, 3, 4],
        "y": [4, 5, 6, 7],
    }
)
p.circle("x", "y", source=cds)

# define events
cds.selected.js_on_change(
    "indices",
    CustomJS(
        args=dict(source=cds),
        code="""
        document.dispatchEvent(
            new CustomEvent("YOUR_EVENT_NAME", {detail: {your_data: "goes-here"}})
        )
        """
    )
)

# result will be a dict of {event_name: event.detail}
# events by default is "", in case of more than one events pass it as a comma separated values
# event1,event2 
# ( no spaces )
result = bokeh_plot_events(bokeh_plot=p, events="YOUR_EVENT_NAME", key="foo")

# use the result
st.write(result)
```
