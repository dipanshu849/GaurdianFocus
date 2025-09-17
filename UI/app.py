import streamlit as st

# Define the pages
main_page  = st.Page("main_page.py", title="Main Page", icon=":material/home:", default=True)
parameters = st.Page("parameters.py", title="Tuning")
memory     = st.Page("memory.py", title="Memory")
monitoring = st.Page("monitoring.py", title="Monitoring")

# Set up navigation
pg = st.navigation([main_page, parameters, monitoring, memory])

# Run the selected page
pg.run()
