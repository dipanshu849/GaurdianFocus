## PURPOSE: SENT NOTIFICATION
## Run as start up application on device

import sys 
sys.path.insert(1, "helper/")
sys.path.append('venv/lib/python3.12/site-packages')

from logger import get_logger   
logger = get_logger(__name__)
from file_logger import log_event


from plyer import notification # Android, Windows, macOS, Linux
import time

def send_notification(title, message, time):
    notification.notify(
        app_name = "Focus",
        title   = title,
        message = message,
        timeout = time
    )    
    logger.debug("Notification send with message: %s", message)
    log_event("notification_sent", f"Title: {title} message: {message}")



# REF: https://www.geeksforgeeks.org/python/python-desktop-notifier-using-plyer-module/

