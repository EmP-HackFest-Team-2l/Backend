from bson.objectid import ObjectId
from flask import abort, request
from flask_login import current_user, login_required
from flask_restful import Resource

from main import messages_collection, successful_response
from models.AccountType import AccountType

class Message(Resource):
    @login_required
    def get(self, id):
        if current_user.account_type != AccountType.STAFF:
            return abort(403, description="You do not have access to this message.")

        message = messages_collection.find_one(ObjectId(id))

        if not message or current_user.id != message["recipient"]:
            return abort(403, description="You do not have access to this message.")

        return message

    @login_required
    def put(self, id):
        if current_user.account_type != AccountType.STAFF:
            return abort(403, description="You do not have access to this message.")

        message = messages_collection.find_one(ObjectId(id))

        if not message or current_user.id != message["recipient"]:
            return abort(403, description="You do not have access to this message.")

        favorite = request.args.get("favorite")
        
        if favorite == "true":
            favorite_val = True
        elif favorite == "false":
            favorite_val = False
        else:
            return abort(400, description="`favorite` has an invalid value.")
            
        res = messages_collection.update_one(id, {"favorite", favorite_val})
        if not res.matched_count:
            return abort(400, description="`id` given has no corresponding message.")

        return successful_response