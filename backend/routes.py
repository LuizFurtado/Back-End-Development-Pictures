from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for  # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    try:
        if len(data) == 0:
            return {"message": "No pictures available"}, 204
        return jsonify(data), 200
    except NameError:
        return {"message": "Internal server error"}, 500

######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    try:
        if len(data) == 0:
            return {"message": "No pictures available"}, 204
        for picture in data:
            if picture['id'] == id:
                return jsonify(picture), 200
        return {"message": "No picture found with the given id"}, 404
    except NameError:
        return {"message": "Internal server error"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    if not request.is_json:
        return jsonify({"error": "Request must be in JSON format"}), 400
    new_picture = request.json
    if not new_picture:
        return jsonify({"error": "Picture data is empty"}), 400
    try:
        for picture in data:
            if picture["id"] == new_picture["id"]:
                return jsonify({"Message": f"picture with id {picture['id']} already present"}), 302
        data.append(new_picture)
        return jsonify(new_picture), 201
    except NameError:
        return {"message": "Internal server error"}, 500
        


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    pass

######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    pass
