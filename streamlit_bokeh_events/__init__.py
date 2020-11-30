from bokeh.embed import json_item
import json

import os
from random import choices
from string import ascii_letters
import streamlit.components.v1 as components

_RELEASE = True

if not _RELEASE:
    _component_func = components.declare_component(
        "streamlit_bokeh_events", url="http://localhost:3001",
    )
else:
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    build_dir = os.path.join(parent_dir, "frontend/build")
    _component_func = components.declare_component("streamlit_bokeh_events", path=build_dir)


def streamlit_bokeh_events(bokeh_plot=None, events="", key=None, debounce_time=1000, refresh_on_update=True, override_height=None):
    """Returns event dict

    Keyword arguments:
    bokeh_plot -- Bokeh figure object (default None)
    events -- Comma separated list of events dispatched by bokeh eg. "event1,event2,event3" (default "")
    debounce_time -- Time in ms to wait before dispatching latest event (default 1000)
    refresh_on_update -- Should the chart be re-rendered on refresh (default False)
        : Set to False if you are not updating the datasource at runtime
    override_height -- Override plot viewport height
    """
    if key is None:
        raise ValueError("key can not be None.")

    div_id = "".join(choices(ascii_letters, k=16))
    fig_dict = json_item(bokeh_plot, div_id)
    json_figure = json.dumps(fig_dict)
    component_value = _component_func(
        bokeh_plot=json_figure,
        events=events,
        key=key,
        _id=div_id,
        default=None,
        debounce_time=debounce_time,
        refresh_on_update=refresh_on_update,
        override_height=override_height
    )
    return component_value


if not _RELEASE:
    import streamlit as st
    import pandas as pd
    from bokeh.plotting import figure
    from bokeh.models import ColumnDataSource, CustomJS
    from bokeh.models import DataTable, TableColumn
    from bokeh.plotting import figure

    st.set_page_config(layout="wide")
    # import function
    # from streamlit_bokeh_events import streamlit_bokeh_events
    col1, col2 = st.beta_columns(2)
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
