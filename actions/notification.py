## PURPOSE: SENT NOTIFICATION
## Run as start up application on device

import sys 
sys.path.insert(1, "helper/")
sys.path.append('venv/lib/python3.12/site-packages')

from logger import get_logger   
logger = get_logger(__name__)


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



# REF: https://www.geeksforgeeks.org/python/python-desktop-notifier-using-plyer-module/

