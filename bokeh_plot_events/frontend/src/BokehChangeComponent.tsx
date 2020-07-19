import React, { ReactNode } from "react"
import {
  withStreamlitConnection,
  StreamlitComponentBase,
  Streamlit,
} from "./streamlit"
import { embed } from "@bokeh/bokehjs";

interface State {
  eventDetailMap: Map<string, object>;
}

class BokehChange extends StreamlitComponentBase<State> {
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

  componentDidMount() {
    const chart: any = document.getElementById(this.props.args["_id"])

    // empty the element
    while (chart.lastChild) {
      chart.lastChild.remove()
    }
    const events = this.props.args["events"]
    const debounceTime = this.props.args["debounce_time"]

    events.split(",").forEach((eventName: string) => document.addEventListener(eventName, this.debounced(debounceTime, this.handleEvent.bind(this))))

    const bokehJson = this.props.args["bokeh_plot"]
    embed.embed_item(JSON.parse(bokehJson))
    Streamlit.setFrameHeight(window.outerHeight)
  }

  componentWillUnmount() {
    const events = this.props.args["events"]
    const debounceTime = this.props.args["debounce_time"]
    // unsure whether removal of listener is correct or not
    events.split(",").forEach((eventName: string) => document.removeEventListener(eventName, this.debounced(debounceTime, this.handleEvent.bind(this))))
  }

  public render = (): ReactNode => {
    return (
      <div id={this.props.args["_id"]} className="stBokehChart"></div>
    )
  }
}

export default withStreamlitConnection(BokehChange)
