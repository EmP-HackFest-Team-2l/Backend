from flask_login import current_user, login_required
from flask_restful import Resource

class User(Resource):
    @login_required
    def get(self):
        return {
            "_id": str(current_user.id),
            "username": current_user.username,
            "account_type": current_user.account_type.name
        }