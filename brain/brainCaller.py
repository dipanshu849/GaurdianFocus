import sqlite3
import time
import firstBrain as fb

def startReasoning():
    conn = None
    try:
        conn = sqlite3.connect("currMemory.db")
        cur  = conn.cursor()

        cur.execute("SELECT * FROM tabs")
        rows = cur.fetchall()

        data = [
            ["id", "title", "url", "isActive", "startTime", "upTime (in minutes)"]
        ]

        for row in rows:
            row = list(row)
            row[5] = (row[5] / 60000)    # need rechecking
            data.append(row)

        fb.analyseData(data)

    except sqlite3.Error as error:
        print("Error occured: ", error)

    finally:
        if conn:
            conn.close()

startReasoning()