from bokeh.models import ColumnDataSource, CustomJS
from bokeh.palettes import Category20
from bokeh.plotting import figure
from bokeh.transform import linear_cmap
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.datasets import make_blobs
# include state from: https://gist.github.com/ash2shukla/ff180d7fbe8ec3a0240f19f4452acde7
from state import provide_state
st.set_page_config(layout="wide")

from streamlit_bokeh_events import streamlit_bokeh_events

@st.cache
def load_data():
    X, y = make_blobs(n_features=2, centers=3)
    return pd.DataFrame({"x": X[:, 0], "y": X[:, 1], "label": y})
    
@provide_state
def main(state):
    df = load_data()

    st.title("Clustering")
    st.subheader("Umap Embedding")

    col1, col2 = st.beta_columns([2,1])

    with col1:
        p1 = figure(sizing_mode="stretch_both",
                    tools="pan,box_select,lasso_select,wheel_zoom,reset", 
                    active_drag="lasso_select",
                    active_scroll="wheel_zoom",
                    **(state.zoom or {}))

        cmap = linear_cmap("label", palette=Category20[20], low=df["label"].min(), high=df["label"].max())
        cds = ColumnDataSource(df)
        cds.selected.indices = state.selected_points or []
        p1.circle("x", "y", source=cds, color=cmap, line_color=cmap)

        cds.selected.js_on_change("indices", CustomJS(args=dict(source=cds, plot=p1),
                code="""
                document.dispatchEvent(new CustomEvent("select_event", 
                        {detail: {
                            indices: cb_obj.indices, 
                            zoom: {
                                y_range: [plot.y_range.start, plot.y_range.end],
                                x_range: [plot.x_range.start, plot.x_range.end]
                                }
                            }
                        }))
                """
            )
        )
        event_result = streamlit_bokeh_events(p1, "select_event", key="select_event")

    with col2:
        if event_result is not None:
            state.selected_points = event_result["select_event"]["indices"]
            state.zoom = event_result["select_event"]["zoom"]
            st.dataframe(df.iloc[event_result["select_event"]["indices"]])

main()