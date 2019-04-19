import os
import traceback

import flask
import json
import random
import requests
import uuid

app = flask.Flask(__name__)


@app.route("/")
def index():
    return flask.jsonify({"ok": "yes"})


@app.route("/v2/catalog")
def catalog():
    cat = {
        "services": [{
            "name": "credhub-example-service",
            "id": "e76a6581-7e8e-4c3d-9e11-906ee5109c77",
            "description": "Credhub Example service.",
            "bindable": True,
            "plans": [{
                "name": "credhub-example-plan-1",
                "id": "7b16c0ff-5e1a-4081-b40d-8ffc1106a385",
                "description": "Credhub example fake Server.",
            }]
        }
        ]
    }

    return flask.jsonify(cat)


@app.route("/v2/service_instances/<instance_id>", methods=["PUT"])
def provision(instance_id):
    return flask.jsonify({})


@app.route("/v2/service_instances/<instance_id>/service_bindings/<binding_id>", methods=["PUT"])
def bind(instance_id, binding_id):
    rd = random.Random()
    rd.seed()
    password = "{}".format(uuid.UUID(int=rd.getrandbits(128)))
    creds = {
        "credentials": {
            "user": "root",
            "password": password
        }
    }

    credhubkey = "/c/example-broker-client/credhub-example-service/f95ddffd-f9b2-4694-9d3d-85c311c69fcc/cred3"
    credhub = {
        "name": credhubkey,
        "type": "json",
        "value": {
            "user": "root",
            "password": password
        }
    }

    headers = {
        'Content-type': 'application/json',
        'authorization': "bearer " + os.getenv("TOKEN")
    }

    response = requests.put(
        os.getenv("CREDHUB_SERVER") + "/api/v1/data",
        data=json.dumps(credhub), headers=headers, verify=False
    )

    if response.status_code > 399:
        raise Exception("Saving credentials to CredHub failed with HTTP Status code: {}".format(response.status_code))

    return flask.jsonify({"credentials": {"key": credhubkey}})


if __name__ == "__main__":
    try:
        app.run(host='0.0.0.0', port=int(os.getenv('PORT', '8080')))
        print("Exited normally")
    except:
        print(" * Exited with exception")
        traceback.print_exc()
