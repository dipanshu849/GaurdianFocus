import sqlite3
import time
import sys 
sys.path.insert(1, "helper/")
import firstBrain as fb
from logger import get_logger   
logger = get_logger(__name__)


def startReasoning():
    logger.debug("Reasoning has started.")
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

        if len(data) != 1:
            fb.analyseData(data)
        else:
            logger.debug("There is not data to reason.")

    except sqlite3.Error as error:
        logger.debug("Error occured in connecting to sqlite: %s", error)

    finally:
        if conn:
            conn.close()

# startReasoning()