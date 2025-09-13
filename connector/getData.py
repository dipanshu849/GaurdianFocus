from flask import Flask, jsonify, request
import sys
sys.path.insert(1, "database/")
import sqlite as sq

app = Flask(__name__)

@app.route("/log-activity", methods=['POST'])
def helloWorld():
    activity_data = request.get_json()

    data = []
    for i in activity_data:
        currValues = activity_data[i].values()
        tupleCurr  = tuple(currValues)

        data.append(tupleCurr)

    sq.addData(data)

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


## Refrence: https://flask.palletsprojects.com/en/stable/quickstart/