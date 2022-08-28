from bson.objectid import ObjectId
from flask import abort
from flask_login import login_required
from flask_restful import Resource

from main import users_collection

class GetUser(Resource):
    @login_required
    def get(self, id):
        user = users_collection.find_one(ObjectId(id), {"password": 0})

        if user is None:
            return abort(400, description="No user associated with id.")
        
        user["_id"] = id
        return user