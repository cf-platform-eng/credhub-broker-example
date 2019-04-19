import os
import traceback

import flask

app = flask.Flask(__name__)


@app.route("/")
def index():
    return "Success"


@app.route("/env")
def env():
    body = "<html><head></head><body><pre>"
    for v in os.environ:
        body += "{}={}\n".format(v, os.environ.get(v))
    body += "</pre></body></html>"
    return body


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8090')))
        print("Exited normally")
    except:
        print(" * Exited with exception")
        traceback.print_exc()
