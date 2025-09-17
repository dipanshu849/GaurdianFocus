import streamlit as st
import json
import graphviz
import time
from streamlit_autorefresh import st_autorefresh
# REF: https://github.com/kmcgrady/streamlit-autorefresh

"## LIVE MONITORING OF GUARDIAN"

AGENT_ARCHITECTURE = {
    "nodes": [
        "start",
        #
        "listening",
        "data_arrived",
        "data_updated",
        #
        "waiting",
        "first_brain",
        "first_brain_error",
        "max_attempt",
        "first_brain_response",
        "no_action",
        "web_search",
        "second_brain_response",
        "notification_sent",
        "end"
    ],
    "edges": [
        ("start", "listening"),
        ("listening", "data_arrived"),
        ("data_arrived", "data_updated"),
        ("data_updated", "listening"),
        #
        ("start", "waiting"),
        ("waiting", "first_brain"),
        ("first_brain", "first_brain_error"),
        ("first_brain_error", "max_attempt"),
        ("max_attempt", "waiting"),
        ("first_brain_error", "first_brain"),
        ("first_brain", "first_brain_response"),
        ("first_brain_response", "no_action"),
        ("no_action", "waiting"),
        ("first_brain_response", "web_search"),
        ("web_search", "second_brain_response"),
        ("second_brain_response", "notification_sent"),
        ("notification_sent", "end"),
        ("notification_sent", "waiting"),
        ("start", "notification_sent")
    ]
}

COUNTER_FILE = "state_handler/counter.txt"
LOG_FILE     = "events.jsonl"

with open(COUNTER_FILE, 'w') as f:
    f.write(f"0\n")

graph_holder = st.empty()

def draw_graph(event):
    # REF: https://graphviz.org/docs/attrs/fontsize/
    dot = graphviz.Digraph(comment='Agent Workflow')
    dot.attr(rankdir='TB', bgcolor='transparent', fontname='Helvetica', fontcolor='white')
    dot.attr('node', shape='box', style='rounded,filled', fillcolor='#000100', color='#6366F1', fontname='Helvetica', fontcolor='white')
    dot.attr('edge', color='#000110')

    for node in AGENT_ARCHITECTURE['nodes']:
        if node == event:
            dot.node(node, color='red', fillcolor='#000010', fontcolor='white', penwidth='1')
        elif node in ["listening", "waiting"] and event not in [None, "end"]:
            dot.node(node, color='red', fontcolor='white', penwidth='2')
        else:
            dot.node(node)

    for edge in AGENT_ARCHITECTURE['edges']:
        if edge[0] == event:
            dot.edge(edge[0], edge[1], color='white')
        else:
            dot.edge(edge[0], edge[1])

    return dot

with st.container(horizontal_alignment="center"):
    graph_holder.graphviz_chart(draw_graph(None))

@st.fragment(run_every="10s")
def load_events():
    expander_counter = 0
    event_counter    = 0
    with open(COUNTER_FILE, 'r') as f:
        lines = f.readlines()
        event_counter = int(lines[0])

    lines = None
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    if lines:
        iterator = 0
        condn = False
        event_reader = event_counter
        
        while True:
            if iterator == len(lines):
                break # extra subsection won't be created
            exp = st.expander(f"Response {expander_counter}", expanded=condn)
            with exp:
                for i in range(iterator, len(lines)):
                    line = lines[i]
                    iterator += 1
                    event = json.loads(line)
                    with st.container(border=True, horizontal=True):
                        st.write(f"Event: {event.get("event")}")
                        st.write(f"Data: {event.get("data")}")

                    if i >= event_reader:
                        event_reader += 1
                        graph_holder.graphviz_chart(draw_graph(event.get("event")))
                        with open(COUNTER_FILE, 'w') as f:
                            f.write(f"{event_reader}\n")
                        time.sleep(1)

                    if event.get("event") == "notification_sent":
                        condn = True
                        expander_counter += 1
                        break
                    
                condn = not condn

            if condn:
                break


    else:
        st.warning("No agent activity found yet")


load_events()