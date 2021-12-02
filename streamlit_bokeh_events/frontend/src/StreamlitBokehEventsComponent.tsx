import React, { ReactNode } from "react"
import {
  Streamlit,
  StreamlitComponentBase,
  withStreamlitConnection,
} from "streamlit-component-lib"
import { embed } from "@bokeh/bokehjs";

interface State {
  eventDetailMap: Map<string, object>;
}

class StreamlitBokehEventsComponent extends StreamlitComponentBase<State> {
  public state = { eventDetailMap: new Map() };

  debounced(delay: number, fn: Function) {
    let timerId: any;
    return function (...args: any[]) {
      if (timerId) {
        clearTimeout(timerId);
      }
      timerId = setTimeout(() => {
        fn(...args);
        timerId = null;
      }, delay);
    }
  }

  handleEvent(event: any) {
    this.setState(
      prevState => ({ eventDetailMap: prevState.eventDetailMap.set(event.type, event.detail) }),
      () => Streamlit.setComponentValue(Object.fromEntries(this.state.eventDetailMap))
    )
  }
  
  _plotChart() {
    const chart: any = document.getElementById(this.props.args["_id"])

    // empty the element
    while (chart.lastChild) {
      chart.lastChild.remove()
    }
    const events = this.props.args["events"]
    const debounceTime = this.props.args["debounce_time"]

    events.split(",").forEach((eventName: string) => document.addEventListener(eventName.trim(), this.debounced(debounceTime, this.handleEvent.bind(this))))

    const bokehJson = this.props.args["bokeh_plot"]
    const figure = JSON.parse(bokehJson)
    embed.embed_item(figure)
    const plot = figure && figure.doc && figure.doc.roots && figure.doc.roots.references
        ? figure.doc.roots.references.find((e: any) => e.type === "Plot")
        : undefined
    // if height is not defined pick up the default bokeh plot height.
    let height = (plot && plot.attributes.plot_height) || 600;
    if (this.props.args["override_height"]) {
      height = this.props.args["override_height"]
    }
    Streamlit.setFrameHeight(height);
  }

  componentDidMount() {
    this._plotChart();
  }

  componentDidUpdate() {
    if ( this.props.args["refresh_on_update"]) {
      this._plotChart();
    }
  }

  componentWillUnmount() {
    const events = this.props.args["events"]
    const debounceTime = this.props.args["debounce_time"]
    // unsure whether removal of listener is correct or not
    events.split(",").forEach((eventName: string) => document.removeEventListener(eventName.trim(), this.debounced(debounceTime, this.handleEvent.bind(this))))
  }

  public render = (): ReactNode => {
    return (
      <div id={this.props.args["_id"]} className="stBokehChart"></div>
    )
  }
}

export default withStreamlitConnection(StreamlitBokehEventsComponent)
