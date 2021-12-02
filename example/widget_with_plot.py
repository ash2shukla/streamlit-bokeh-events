import streamlit as st
import pandas as pd
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, CustomJS
from bokeh.models import DataTable, TableColumn
from bokeh.plotting import figure
from streamlit_bokeh_events import streamlit_bokeh_events

st.set_page_config(layout="wide")
# import function
# from streamlit_bokeh_events import streamlit_bokeh_events
col1, col2 = st.columns(2)
df = pd.read_csv('https://raw.githubusercontent.com/mwaskom/seaborn-data/master/iris.csv')
# create plot
cds = ColumnDataSource(df)
columns = list(map(lambda colname: TableColumn(field=colname, title=colname), df.columns))

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

table = DataTable(source=cds, columns=columns)
with col1:
    result = streamlit_bokeh_events(
        bokeh_plot=table,
        events="INDEX_SELECT",
        key="foo",
        refresh_on_update=False,
        debounce_time=0,
        override_height=500
    )
    if result:
        if result.get("INDEX_SELECT"):
            st.write(df.iloc[result.get("INDEX_SELECT")["data"]])

plot = figure(tools="lasso_select,zoom_in")
df["colors"] = df.species.replace({"setosa": "#583d72", "versicolor": "#9f5f80", "virginica": "#ffba93"})
cds_lasso = ColumnDataSource(df)
cds_lasso.selected.js_on_change(
    "indices",
    CustomJS(
        args=dict(source=cds_lasso),
        code="""
        document.dispatchEvent(
            new CustomEvent("LASSO_SELECT", {detail: {data: source.selected.indices}})
        )
        """
    )
)

plot.circle("sepal_length", "sepal_width", fill_alpha=0.5, color="colors", size=10, line_color=None, source=cds_lasso)
with col2:
    result_lasso = streamlit_bokeh_events(
        bokeh_plot=plot,
        events="LASSO_SELECT",
        key="bar",
        refresh_on_update=False,
        debounce_time=0)
    if result_lasso:
        if result_lasso.get("LASSO_SELECT"):
            st.write(df.iloc[result_lasso.get("LASSO_SELECT")["data"]])
