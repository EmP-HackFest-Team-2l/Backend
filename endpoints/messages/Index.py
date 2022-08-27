from datetime import datetime
from flask import abort, request
from flask_login import current_user, login_required
from flask_restful import Resource

from main import messages_collection, successful_response
from models import AccountType, Message

class Index(Resource):
    @login_required
    def post(self):
        if current_user.account_type != AccountType.STUDENT:
            return abort(403, description="You do not have access to this message.")

        json_data = request.get_json()

        message = Message(json_data)

        error = message.validate()
        if error:
            return abort(400, description=error)

        json_data["send_time"] = datetime.now()        
        messages_collection.insert_one(json_data)
        
        return successful_response