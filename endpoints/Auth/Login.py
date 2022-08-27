from flask import abort, redirect, request
from flask_login import login_user
from flask_restful import Resource
from werkzeug.security import check_password_hash

from main import is_safe_url, successful_response, users
from models import User

class Login(Resource):
    def post(self):
        json_data = request.get_json()

        if not json_data["username"]:
            return abort(400, description="Username not supplied.")
        elif not json_data["password"]:
            return abort(400, description="Password not supplied.")

        user = users.find_one({"username": json_data["username"]})
        if not user:
            raise abort(401, description="Username or password incorrect.")

        user = User(user)
        if not check_password_hash(user.password, json_data["password"]):
            raise abort(401, description="Username or password incorrect.")

        remember = "remember" in json_data and json_data["remember"]
        login_user(User(user), remember=remember)

        # Validate that the redirect point is a safe place to redirect to
        next = request.args.get("next")
        if (next):
            if not is_safe_url(next):
                return abort(400)

            return redirect(next)
        else:
            return successful_response