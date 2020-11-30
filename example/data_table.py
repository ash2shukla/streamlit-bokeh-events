import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn
from streamlit_bokeh_events import streamlit_bokeh_events

df = pd.DataFrame({
        "x": [1, 2, 3, 4],
        "y": [4, 5, 6, 7],
})
# create plot
cds = ColumnDataSource(df)
columns = [
TableColumn(field="x"),
TableColumn(field="y"),
]

# define events
cds.selected.js_on_change(
"indices",
CustomJS(
        args=dict(source=cds),
        code="""
        document.dispatchEvent(
        new CustomEvent("INDEX_SELECT", {detail: {data: source.selected.indices}})
        )
        """
)
)
p = DataTable(source=cds, columns=columns)
result = streamlit_bokeh_events(bokeh_plot=p, events="INDEX_SELECT", key="foo", refresh_on_update=False, debounce_time=0, override_height=100)
if result:
        if result.get("INDEX_SELECT"):
                st.write(df.iloc[result.get("INDEX_SELECT")["data"]])
