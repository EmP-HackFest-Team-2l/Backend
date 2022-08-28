from datetime import datetime
from flask import abort, request
from flask_login import current_user, login_required
from flask_restful import Resource

from main import messages_collection, successful_response
from models import AccountType, Message

class Index(Resource):
    @login_required
    def get(self):
        if current_user.account_type != AccountType.STAFF:
            return abort(403, description="You do not have access to this message.")

        # support for pagination could be easily added
        try:
            limit = min(int(request.args.get("limit")), 100)
        except (ValueError, TypeError):
            limit = 100

        db_messages = messages_collection.find(
            {"recipient": current_user.id},
            {"content": 0},
            limit=limit)

        messages = []
        for message in db_messages:
            message["_id"] = str(message["_id"])
            messages.append(message)
        
        return messages, 200

    @login_required
    def post(self):
        if current_user.account_type != AccountType.STUDENT:
            return abort(403, description="You do not have access to this message.")

        json_data = request.get_json()

        message = Message(json_data)

        error = message.validate()
        if error:
            return abort(400, description=error)

        json_data["send_time"] = datetime.now().isoformat()
        messages_collection.insert_one(json_data)
        
        return successful_response