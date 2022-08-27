from flask_login import login_required, logout_user
from flask_restful import Resource

from main import successful_response

class Logout(Resource):
    @login_required
    def post(self):
        logout_user()
        return successful_response