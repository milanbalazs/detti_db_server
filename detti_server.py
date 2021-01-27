import os
import sys
from flask import Flask, request
from flask_restful import Resource, Api

# Get the path of the directory of the current file.
PATH_OF_FILE_DIR: str = os.path.join(os.path.realpath(os.path.dirname(__file__)))

# Append the path of the tools folder to find modules.
sys.path.append(PATH_OF_FILE_DIR)

from detti_db import DettiDB  # noqa: E402

detti_db = DettiDB()
app = Flask(__name__)
api = Api(app)


class GetItem(Resource):
    def get(self, db_key):
        return detti_db[db_key]


class SetItem(Resource):
    def put(self):
        for key, value in request.form.items():
            detti_db[key] = value
        return "OK"


api.add_resource(GetItem, "/get/<string:db_key>")
api.add_resource(SetItem, "/set")

if __name__ == "__main__":
    app.run(debug=True)
