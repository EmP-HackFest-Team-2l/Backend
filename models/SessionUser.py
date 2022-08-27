from flask_login import UserMixin

class SessionUser(UserMixin):
    def __init__(self, user_dict):
        self.id = user_dict["_id"]