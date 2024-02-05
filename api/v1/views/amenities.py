#!/usr/bin/python3
"""amenities view"""

from api.v1.views import app_views
from flask import jsonify, abort, request
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route("/amenities", strict_slashes=False, methods=["GET"])
@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["GET"])
def get_amenties(amenity_id):
    """Retrieves the list of all amenties object of a state"""
    list_amenity = []
    if amenity_id is None:
        all_objs = storage.all(Amenity).values()
        for v in all_objs:
            list_amenity.append(v.to_dict())
        return jsonify(list_amenity)
    else:
        result = storage.get(Amenity, amenity_id)
        if result is None:
            abort(404)
        return jsonify(result.to_dict())


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["DELETE"])
def delete_amenity(amenity_id):
    """deletes a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route("/amenities", strict_slashes=False, methods=["POST"])
def create_amenity():
    """creates a amenity"""
    data = request.get_json(force=True, silent=True)
    if not data:
        abort(404, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')
    amenity = Amenity(**data)
    amenity.save
    return jsonify(amenity.to_dict()), 201


@app_views.route("/amenities/<amenity_id>", strict_slashes=False,
                 methods=["PUT"])
def update_amenity(amenity_id):
    """updates a amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    data = request.json
    ignore_keys = ['id', 'state_id', 'created_at', 'updated_at']
    for key , value in data.items():
        if key not in ignore_keys:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict()), 200