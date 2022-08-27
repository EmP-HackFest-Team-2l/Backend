import os
# import dns.resolver
from flask import Flask
from flask_restful import Api
from pymongo import MongoClient
from pymongo.server_api import ServerApi

app = Flask(__name__)
api = Api(app)

# dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
# dns.resolver.default_resolver.nameservers=['8.8.8.8']

mongo_client = MongoClient(os.environ["MONGODB_URL"], server_api=ServerApi('1'))
db = mongo_client["EduHack"]
user_credentials = db["UserCredentials"]


from endpoints.Login import Login
api.add_resource(Login, "/login")
