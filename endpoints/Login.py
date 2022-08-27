from main import user_credentials
from flask_restful import Resource

class Login(Resource):
    def get(self):
        user = user_credentials.find_one()
        user.pop("_id")
        print(user)
        return user