import subprocess
import sys 
sys.path.insert(1, "helper/")
sys.path.insert(1, "actions/")
sys.path.insert(1, "brain/")
sys.path.insert(1, "database/")
# sys.path.insert(1, "connector/")
import time
import atexit 
import schedule
import threading

from logger import get_logger   
logger = get_logger(__name__)

import notification as ntf
import brainCaller as bc
from sqlite import cleanTable

import os
from dotenv import load_dotenv
load_dotenv()
# os.getenv('GEMINI_API_KEY')

cleanTable() # REMOVE PREVIOUS DATA

PYTHON_EXECUTABLE            = sys.executable # to ensure it uses the same Python interpreter
GET_DATA_SCRIPT              = "connector/getData.py"
GUARDIAN_CHECK_INTERVAL_TIME_MINUTE = int(os.getenv('GUARDIAN_RUN_INTERVAL_TIME_MINUTE'))

listener_process  = None

def cleanUp():
    if listener_process:
        listener_process.terminate()
        listener_process.wait()

    ntf.send_notification("Guardian OFF", "Hope you did well", 20)

atexit.register(cleanUp)

def safe_startReasoning():
    try:
        bc.startReasoning()
    except Exception as exc:
        logger.debug("Scheduler job crashed: %s", exc)


schedule.every(GUARDIAN_CHECK_INTERVAL_TIME_MINUTE).minutes.do(safe_startReasoning)
def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)


try:
    listener_process  = subprocess.Popen([PYTHON_EXECUTABLE, GET_DATA_SCRIPT])
    logger.debug("Started Listener With PID: %s", listener_process.pid)

    scheduler_thread  = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    ntf.send_notification("Guardian ON", "I Will be there for help", 20)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    ntf.send_notification("Guardian @_@", "Some error occured", 20)
    logger.debug("Process terminated")