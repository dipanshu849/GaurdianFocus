import streamlit as st
import json
import graphviz

"## LIVE MONITORING OF GUARDIAN"

st.button("Refresh")
COUNTER_FILE = "counter.txt"
LOG_FILE     = "events.jsonl"

def load_events():
    expander_counter = 0

    lines = None
    with open(LOG_FILE, 'r') as f:
        lines = f.readlines()

    if lines:
        iterator = 0
        condn = False
        
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