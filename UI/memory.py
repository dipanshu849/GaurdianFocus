import streamlit as st
import sqlite3 as sq
import pandas as pd
import numpy as np

"## Memory"

st.button("Refresh")
def load_table():
    conn = None

    try:
        conn = sq.connect("currMemory.db")
        cur = conn.cursor()

        cur.execute("SELECT * FROM tabs")
        rows = cur.fetchall()

        data = []

        for row in rows:
            row = list(row)
            row[5] = (row[5] / 60000)    # need rechecking
            data.append(row)


        if st.checkbox("Show Data", value=True):
            memory_data = pd.DataFrame(
                data,
                columns=["Id", "Title", "Url", "IsActive", "StartTime", "UpTime (in minutes)"]
            )

            st.dataframe(memory_data, height=800)

    except Exception as e:
        print("Error occured: ", e)
        # if conn:
        #     conn.close()

load_table()