import sys
print(sys.path);
sys.path.append('/home/dipanshu/Desktop/besideYou/source/venv/lib/python3.12/site-packages');
from plyer import notification
import time

notification.notify(
    app_name = "Focus",
    title   = "Gaurdian",
    message = "Dipanshu this is working, I am coming alive",
    timeout = 2
)