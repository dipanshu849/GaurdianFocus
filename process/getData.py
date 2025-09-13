from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route("/log-activity", methods=['POST'])
def helloWorld():
    activity_data = request.get_json()
    print(activity_data)
    # url           = activity_data.get('url')
    # title         = activity_data.get('title')

    # print(f"Browser is on {title}")
    # print(f"With Url on {url}")

    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=True)


## Refrence: https://flask.palletsprojects.com/en/stable/quickstart/