import streamlit as st
from bokeh.models.widgets import ColorPicker
from bokeh.models import CustomJS
from streamlit_bokeh_events import streamlit_bokeh_events

selected_color = "#ff4466" 
color_picker = ColorPicker(color=selected_color, title="Choose color:", width=200)
color_picker.js_on_change("color", CustomJS(code="""
    document.dispatchEvent(new CustomEvent("COLOR_PICKED", {detail: {pickedColor: cb_obj.color}}))
    """))
result = streamlit_bokeh_events(
    color_picker,
    events="COLOR_PICKED",
    key="picker",
    refresh_on_update=False,
    override_height=75,
    debounce_time=0)

if result:
    if "COLOR_PICKED" in result:
        selected_color = result.get("COLOR_PICKED")["pickedColor"]

st.write(selected_color)