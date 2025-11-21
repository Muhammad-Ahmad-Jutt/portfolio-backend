# this file will handle the login and signup 

from flask import Blueprint,request, jsonify
from flask_jwt_extended import create_access_token


authbp=Blueprint("auth",__name__)

@authbp.post('/sign-up')
def signup():

    print(request.data)
    data = request.json
    print(data.json)
    return data.json