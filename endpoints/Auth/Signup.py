from flask import abort, request
from flask_login import login_user
from flask_restful import Resource
from werkzeug.security import generate_password_hash

from main import successful_response, user_credentials
from models import SessionUser

class Signup(Resource):
    def post(self):
        json_data = request.get_json()

        if not json_data["username"]:
            return abort(400, description="Username not supplied.")
        elif not json_data["password"]:
            return abort(400, description="Password not supplied.")

        user = user_credentials.find_one({"username": json_data["username"]})
        if user:
            return abort(400, description="Username already taken.")

        new_user = {
            "username": json_data["username"],
            "password": generate_password_hash(json_data["password"])
        }

        user_credentials.insert_one(new_user)

        login_user(SessionUser(new_user))

        return successful_response