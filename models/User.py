from flask_login import UserMixin

from .AccountType import AccountType

class User(UserMixin):
    def __init__(self, user_dict):
        self.id: str = user_dict["_id"]
        self.username: str = user_dict["username"]
        self.password: str = user_dict["password"]
        self.account_type: AccountType = AccountType(user_dict["account_type"])