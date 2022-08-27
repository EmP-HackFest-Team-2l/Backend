from flask import abort, request
from flask_login import login_user
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from main import successful_response, user_credentials
from models import User

class Signup(Resource):
    def post(self):
        json_data = request.get_json()

        if not json_data["username"]:
            return abort(400, description="`username` not supplied.")
        elif not json_data["password"]:
            return abort(400, description="`password` not supplied.")
        elif not json_data["account_type"]:
            return abort(400, description="`account_type` not supplied.")

        user = user_credentials.find_one({"username": json_data["username"]})
        if user:
            return abort(400, description="Username already taken.")

        new_user = {
            "username": json_data["username"],
            "password": generate_password_hash(json_data["password"]),
            "account_type": json_data["account_type"]
        }

        user_credentials.insert_one(new_user)

        login_user(User(new_user))

        return successful_response