import streamlit as st
from dotenv import set_key, get_key

env_path = ".env"

def get_int(key):
    return int(get_key(env_path, key))

def get_float(key):
    return float(get_key(env_path, key))

def get_str(key):
    return get_key(env_path, key)

options_first_model = ["gemini-1.5-flash", "gemini-2.5-flash", "gemini-2.5-flash-lite"]
options_second_model = ["deepseek-r1-distill-llama-70b", "llama-3.1-8b-instant", "llama-3.3-70b-versatile", "meta-llama/llama-guard-4-12b", "moonshotai/kimi-k2-instruct"]

#
with st.container(border=True):
    st.slider(label="Guardian interval (in minutes)",
              min_value = 3, max_value = 15,
              value = get_int("GUARDIAN_RUN_INTERVAL_TIME_MINUTE"),
              key="GUARDIAN_RUN_INTERVAL_TIME_MINUTE")

    st.caption("For value below 3 minutes, chances for model overloading error increases")

    st.slider(label="Notification timeout for response (in seconds)", 
              min_value = 5, max_value = 50, 
              value = get_int("NOTIFICATION_TIMEOUT_FOR_ADVICE"),
              key="NOTIFICATION_TIMEOUT_FOR_ADVICE")

    st.slider(label="Notification timeout for ON and OFF guardian (in seconds)", 
              min_value = 2, max_value = 50, 
              value = get_int("NOTIFICATION_TIMEOUT_FOR_ON_OFF"),
              key="NOTIFICATION_TIMEOUT_FOR_ON_OFF")


#
with st.container(border=True):
    st.selectbox(label="First brain model", 
                 options=options_first_model,
                 index=options_first_model.index(get_str("FIRST_BRAIN_MODEL")),
                 key="FIRST_BRAIN_MODEL")

    st.slider(label="Max retry before the cycle is skipped", 
              min_value = 0, max_value = 5, 
              value = get_int("FIRST_BRAIN_MAX_RETRY"),
              key="FIRST_BRAIN_MAX_RETRY")


#
with st.container(border=True):
    st.selectbox(label="Second brain model", 
                 options=options_second_model,
                 index=options_second_model.index(get_str("SECOND_BRAIN_MODEL")),
                 key="SECOND_BRAIN_MODEL")

    st.slider(label="Second brain temperature", 
              min_value = 0.0, max_value = 2.0, 
              value = 0.2,
              key="SECOND_BRAIN_TEMPERATURE")

    st.slider(label="Second brain max output tokens", 
              min_value = 800, max_value = 2000, 
              value = get_int("SECOND_BRAIN_MAX_OUTPUT_TOKEN"),
              key="SECOND_BRAIN_MAX_OUTPUT_TOKEN")

# 
with st.container(border=True):
    st.slider(label="Time to wait before changing inactive tab to active (in seconds)", 
              min_value = 60, max_value=3600, 
              value = get_int("WAIT_TIME_TO_CHANGE_ACTIVE_TO_INACTIVE"),
              key="WAIT_TIME_TO_CHANGE_ACTIVE_TO_INACTIVE")
    

def save_changes():
    keys = [
        "GUARDIAN_RUN_INTERVAL_TIME_MINUTE",
        "NOTIFICATION_TIMEOUT_FOR_ADVICE",
        "NOTIFICATION_TIMEOUT_FOR_ON_OFF",
        "FIRST_BRAIN_MODEL",
        "FIRST_BRAIN_MAX_RETRY",
        "SECOND_BRAIN_MODEL",
        "SECOND_BRAIN_TEMPERATURE",
        "SECOND_BRAIN_MAX_OUTPUT_TOKEN",
        "WAIT_TIME_TO_CHANGE_ACTIVE_TO_INACTIVE",
    ]
    for k in keys:
        set_key(env_path, k, str(st.session_state[k]))
    st.success("Parameters saved")


st.button("SAVE", on_click=save_changes)