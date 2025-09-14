## PURPOSE: SENT NOTIFICATION
## Run as start up application on device

import sys
sys.path.append('venv/lib/python3.12/site-packages')

from plyer import notification # Android, Windows, macOS, Linux
import time

def send_notification(title, message):
    notification.notify(
        app_name = "Focus",
        title   = title,
        message = message,
        timeout = 50
    )    


# REF: https://www.geeksforgeeks.org/python/python-desktop-notifier-using-plyer-module/

