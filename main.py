from dotenv import load_dotenv
import os
from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
api = Api(app)

load_dotenv()

mongo_client = MongoClient(os.environ["MONGODB_URL"], server_api=ServerApi('1'))
db = mongo_client["EduHack"]
user_credentials = db["UserCredentials"]

from endpoints.Login import Login
api.add_resource(Login, "/login")
