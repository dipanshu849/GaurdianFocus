import streamlit as st

# Define the pages
main_page = st.Page("main_page.py", title="Main Page", icon="🎈", default=True)
memory = st.Page("memory.py", title="Memory")
monitoring = st.Page("monitoring.py", title="Monitoring")

# Set up navigation
pg = st.navigation([main_page, memory, monitoring])

# Run the selected page
pg.run()
