from bson.objectid import ObjectId
from flask import abort, request
from flask_login import current_user, login_required
from flask_restful import Resource

from main import messages_collection, string_to_bool, successful_response
from models.AccountType import AccountType

class Message(Resource):
    @login_required
    def get(self, id):
        if current_user.account_type != AccountType.STAFF:
            return abort(403, description="You do not have access to this message.")

        message = messages_collection.find_one(ObjectId(id))

        if not message or current_user.id != message["recipient"]:
            return abort(403, description="You do not have access to this message.")

        message.pop("_id")
        return message

    @login_required
    def put(self, id):
        if current_user.account_type != AccountType.STAFF:
            return abort(403, description="You do not have access to this message.")

        message = messages_collection.find_one(ObjectId(id), {"recipient": 1})

        if not message or current_user.id != message["recipient"]:
            return abort(403, description="You do not have access to this message.")

        update_dict = {}

        favorite = string_to_bool(request.args.get("favorite"))
        if (favorite is not None):
            update_dict["favorite"] = favorite
        
        read = string_to_bool(request.args.get("read"))
        if (read is not None):
            update_dict["read"] = read
            
        res = messages_collection.update_one({"_id": ObjectId(id)},
                                             {"$set": update_dict})

        if not res.matched_count:
            return abort(400, description="`id` given has no corresponding message.")
        return successful_response