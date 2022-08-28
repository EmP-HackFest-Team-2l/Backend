from flask_login import login_required
from flask_restful import Resource

from models import AccountType
from main import users_collection

class Staff(Resource):
    @login_required
    def get(self):
        staff_list = users_collection.find({
            "account_type": AccountType.STAFF.name
        }, {
            "password": 0
        })

        final_list = []
        for staff_member in staff_list:
            staff_member["_id"] = str(staff_member["_id"])
            final_list.append(staff_member)

        return final_list