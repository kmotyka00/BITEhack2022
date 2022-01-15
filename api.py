#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
from flask import request, Flask, current_app
import os

app = Flask(__name__)


@app.route("/", methods=['POST'])
def save_json():
    data = request.get_json()
    user_id = str(data["id"])+".json"
    if not os.path.exists(os.path.join(current_app.root_path, "client_data/json_files")):
        os.makedirs(os.path.join(current_app.root_path, "client_data/json_files"))
    path_to_json = os.path.join(current_app.root_path, "client_data/json_files", user_id)
    with open(path_to_json, 'w') as outfile:
        outfile.write(json.dumps(data))
    return {"info": "accepted"}, 202


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)

