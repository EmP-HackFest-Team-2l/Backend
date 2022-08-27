from operator import index
from bson.objectid import ObjectId
from dotenv import load_dotenv
from flask import Flask, jsonify, request
from flask_login import LoginManager
from flask_restful import Api
import os
from pymongo import MongoClient
from urllib.parse import urlparse, urljoin


from models import User

"""
Load environment variables from .env file
"""
load_dotenv()


"""
Start Flask and Flask-RESTful
"""
app = Flask(__name__)
app.secret_key = os.environ["API_SECRET"]
app.app_context().push()
api = Api(app)


"""
Initialize database
"""
mongo_client = MongoClient(os.environ["MONGODB_URL"])
db = mongo_client["EduHack"]
users_collection = db["Users"]
messages_collection = db["Messages"]
# To increase lookup performance of the collection
messages_collection.create_index([("recipient", 1)])


"""
Initialize the login manager things
"""
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    user = users_collection.find_one(ObjectId(user_id))

    if not user:
        return None
    
    return User(user) 


"""
Utils
"""
successful_response = jsonify(success=True)
successful_response.status_code = 200

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc


"""
Adding all the resources/endpoints
Must be at the end of file to avoid circular imports
In a file to avoid polluting the scope
"""
def add_resources():
    from endpoints import Login
    api.add_resource(Login, "/auth/login")

    from endpoints import Logout
    api.add_resource(Logout, "/auth/logout")

    from endpoints import Signup
    api.add_resource(Signup, "/auth/signup")

    from endpoints import Index
    api.add_resource(Index, "/messages")

    from endpoints import Message
    api.add_resource(Message, "/messages/<id>")

    from endpoints import Dog
    api.add_resource(Dog, "/dog")
add_resources()