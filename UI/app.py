import streamlit as st

main_page  = st.Page("main_page.py",  title="Main Page",  icon=":material/home:",      default=True)
parameters = st.Page("parameters.py", title="Tuning",     icon=":material/settings:")
memory     = st.Page("memory.py",     title="Memory",     icon=":material/dataset_linked:")
monitoring = st.Page("monitoring.py", title="Monitoring", icon=":material/browse_activity:")

pg = st.navigation([main_page, parameters, monitoring, memory])

pg.run()


## REF: https://docs.streamlit.io/get-started/fundamentals/additional-features