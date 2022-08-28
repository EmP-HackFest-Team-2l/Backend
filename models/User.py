from flask_login import UserMixin

from .AccountType import AccountType

class User(UserMixin):
    def __init__(self, user_dict):
        self.id: str = str(user_dict.get("_id"))
        self.username: str = user_dict.get("username")
        self.password: str = user_dict.get("password")

        self._account_type_string = user_dict.get("account_type")
        self.account_type: AccountType
        if "account_type" not in user_dict \
            or self._account_type_string not in AccountType.__members__:
            self.account_type = None
        else:
            self.account_type = AccountType[user_dict["account_type"]]

        # Note that user has no reference to messages to avoid many queries
        # for referenced message objects, and to avoid having to load long
        # arrays of ids whenever the user is queried

    def validate(self, validate_account_type=True) -> str:
        if not self.username:
            return "`username` is not set."
        elif not isinstance(self.username, str):
            return "`username` is not a string."
        
        elif not self.password:
            return "`password` is not set."
        elif not isinstance(self.password, str):
            return "`password` is not a string."
        
        elif not self.account_type and validate_account_type:
            if self._account_type_string is None:
                return "`account_type` is not set."
            else:
                return "`account_type` has an invalid value."