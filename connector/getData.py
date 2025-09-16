from flask import Flask, jsonify, request
import sys 
sys.path.insert(1, "helper/")
sys.path.insert(1, "database/")
from logger import get_logger   
logger = get_logger(__name__)
from file_logger import log_event



# custom
import sqlite as sq

app = Flask(__name__)

@app.route("/log-activity", methods=['POST'])
def fetchData():
    logger.debug("Data received from extension")
    activity_data = request.get_json()

    data = []
    for i in activity_data:
        currValues = activity_data[i].values()
        tupleCurr  = tuple(currValues)

        data.append(tupleCurr)

    log_event("data_arrived", f"Received data for {len(data)} tabs.")
    sq.addData(data)

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


## Refrence: https://flask.palletsprojects.com/en/stable/quickstart/