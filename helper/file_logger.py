import json
import datetime

LOG_FILE = "events.jsonl"

def log_event(event_type, data):
    log_entry = {
        "time" : datetime.datetime.now().isoformat(),
        "event": event_type,
        "data" : data
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(log_entry) + "\n")