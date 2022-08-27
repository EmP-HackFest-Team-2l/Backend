from flask import abort, redirect, request
from flask_login import login_user
from flask_restful import Resource
from werkzeug.security import check_password_hash

from main import is_safe_url, successful_response, users_collection
from models import User

class Login(Resource):
    def post(self):
        json_data = request.get_json()

        user = User(json_data)

        error = user.validate(validate_account_type=False)
        if error:
            return abort(400, description=error)

        db_user = users_collection.find_one({"username": user.username})
        if not db_user:
            return abort(401, description="Username or password incorrect.")

        if not check_password_hash(db_user["password"], user.password):
            return abort(401, description="Username or password incorrect.")

        remember = "remember" in json_data and json_data["remember"]
        login_user(User(db_user), remember=remember)

        # Validate that the redirect point is a safe place to redirect to
        next = request.args.get("next")
        if (next):
            if not is_safe_url(next):
                return abort(400)

            return redirect(next)
        else:
            return successful_response