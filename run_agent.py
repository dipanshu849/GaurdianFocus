import sys 
sys.path.insert(1, "helper/")
sys.path.insert(1, "actions/")
sys.path.insert(1, "brain/")
sys.path.insert(1, "database/")


import subprocess
import time
import atexit 
import schedule
import threading
import notification as ntf
import brainCaller as bc
import os
from logger import get_logger   
from file_logger import log_event
from sqlite import cleanTable
from dotenv import load_dotenv

logger = get_logger(__name__)
load_dotenv()

COUNTER_FILE = "state_handler/counter.txt"
LOG_FILE     = "events.jsonl"

# REMOVE PREVIOUS DATA
cleanTable() 
with open(LOG_FILE, "w") as f:
    pass
with open(COUNTER_FILE, 'w') as f:
    f.write(f"0\n")

log_event("start", "Guardina is watching you")

PYTHON_EXECUTABLE            = sys.executable # to ensure it uses the same Python interpreter
GET_DATA_SCRIPT              = "connector/getData.py"
GUARDIAN_CHECK_INTERVAL_TIME_MINUTE = int(os.getenv('GUARDIAN_RUN_INTERVAL_TIME_MINUTE'))
NOTIFICATION_TIMEOUT_ON_OFF  = int(os.getenv('NOTIFICATION_TIMEOUT_FOR_ON_OFF'))

listener_process  = None

def cleanUp():
    if listener_process:
        listener_process.terminate()
        listener_process.wait()

    ntf.send_notification("Guardian OFF", "Hope you did well", NOTIFICATION_TIMEOUT_ON_OFF)
    log_event("end", "Guardina is OFF")

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

    ntf.send_notification("Guardian ON", "I Will be there for help", NOTIFICATION_TIMEOUT_ON_OFF)

    while True:
        time.sleep(1)

except KeyboardInterrupt:
    # ntf.send_notification("Guardian @_@", "Some error occured", 20)
    logger.debug("Process terminated")