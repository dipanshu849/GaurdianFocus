## PURPOSE: SENT NOTIFICATION
## Run as start up application on device

import sys
sys.path.append('/home/dipanshu/Desktop/besideYou/source/venv/lib/python3.12/site-packages')

from plyer import notification # Android, Windows, macOS, Linux
import time

if (__name__ == '__main__'):
    notification.notify(
        app_name = "Focus",
        title   = "Gaurdian",
        message = "Dipanshu this is working, I am coming alive",
        timeout = 2
    )


# REF: https://www.geeksforgeeks.org/python/python-desktop-notifier-using-plyer-module/

