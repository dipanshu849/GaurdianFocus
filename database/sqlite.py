import sqlite3
import time
import os
import sys 
sys.path.insert(1, "helper/")
from dotenv import load_dotenv
load_dotenv()
# os.getenv('GEMINI_API_KEY')
from logger import get_logger   
logger = get_logger(__name__)
from file_logger import log_event


WAIT_TIME = int(os.getenv('WAIT_TIME_TO_CHANGE_ACTIVE_TO_INACTIVE'))

def cleanTable():
    logger.debug("Clearing the session [Deleting all rows of database]")
    conn = None
    try:
        conn = sqlite3.connect("currMemory.db")
        cur  = conn.cursor()

        query = "DELETE FROM tabs"

        cur.execute(query)

    finally:
        if conn:
            conn.commit()
            conn.close()

def addData(data): # [(id, title, url, isActive, startTime, uptime), (), ...]
    logger.debug("Adding new data")
    conn = None
    try:
        conn = sqlite3.connect("currMemory.db")
        cur  = conn.cursor()

        prevTabIdsQuery = "SELECT id FROM tabs"
        response = cur.execute(prevTabIdsQuery)
        allPrevTabIds = set(response.fetchall())

        new_added_tabs = 0
        for req in data:
            searchQuery = "SELECT * FROM tabs WHERE id=?"
            cur.execute(searchQuery, (req[0],))

            result = cur.fetchone()
            ID        = req[0]
            ISACTIVE  = req[3]
            STARTTIME = req[4]

            allPrevTabIds.discard((ID,))  # this tab haven't been closed

            if result:
                ISACTIVE_P  = result[3]
                STARTTIME_P = result[4]
                UPTIME_P    = result[5]
                # prev was active and now is also active
                if (ISACTIVE == ISACTIVE_P == True):
                    upTime = STARTTIME - STARTTIME_P
                    query = (f"UPDATE tabs "
                            f"SET upTime = {upTime} "
                            f"WHERE id=?")

                elif (ISACTIVE == ISACTIVE_P == False): # prev inactive and now also inactive
                    query = (f"UPDATE tabs "
                            f"SET startTime = {STARTTIME} "
                            f"WHERE id=?")

                elif (ISACTIVE_P == True and ISACTIVE == False): # prev active now inactive
                    currentTimeStamp = time.time()
                    if (STARTTIME_P + UPTIME_P - currentTimeStamp >= WAIT_TIME): # more than 10 minutes have passed since then
                        query = (f"UPDATE tabs "
                                f"SET startTime = {STARTTIME}, isActive = False, upTime = 0 "
                                f"WHERE id=?")

                    else:
                        continue
                        # do nothings
                        # as if the switch was small 
                        # the first IF will be execute and uptime will be counted

                elif (ISACTIVE_P == False and ISACTIVE == True):
                    upTime = STARTTIME - STARTTIME_P
                    query = (f"UPDATE tabs "
                            f"SET upTime = {upTime} "
                            f"WHERE id=?")

                cur.execute(query, (ID,))
                
            else:
                new_added_tabs += 1
                cur.execute("INSERT INTO tabs VALUES (?, ?, ?, ?, ?, ?)", req)
    
        removed_tabs = 0
        # Delete the data about closed tab
        for i in allPrevTabIds:
            query = (f"DELETE FROM tabs "
                    f"WHERE id=?")
            cur.execute(query, i)
            removed_tabs += 1
            
        conn.commit()
        log_event("data_updated", f"Removed tabs: {removed_tabs} New added tabs: {new_added_tabs}")


    except sqlite3.Error as error:
        print("Error occured: ", error)

    finally:
        if conn:
            conn.close()


if __name__ == '__main__':
    conn = sqlite3.connect("currMemory.db")
    
    cur  = conn.cursor()
    cur.execute("CREATE TABLE tabs(id, title, url, isActive, startTime, upTime)")


##
## REF: https://stackoverflow.com/questions/45569344/how-to-tell-if-a-value-exists-in-a-sqlite3-database-python
##      https://www.geeksforgeeks.org/python/python-sqlite/
##      https://docs.python.org/3/library/sqlite3.html