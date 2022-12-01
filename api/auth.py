import uuid
from sqlite3 import IntegrityError

from flask import request
from flask_cors import cross_origin

from flask import Blueprint
from flask_jwt_extended import (create_access_token, create_refresh_token)

from api.helper import return_response
from db_connect import Session
from model.db_models import User

auth_api = Blueprint('auth_api', __name__)


@auth_api.route("/signup", methods=['POST', 'OPTIONS'])
def signup():
    if request.method == "OPTIONS":
        return return_response({"Content-Type": "application/json"}, 200)
    if not request.is_json:
        return return_response({"msg": "Missing JSON in request"}, 400)
    first_name = request.json.get('first_name', None)
    last_name = request.json.get('last_name', None)
    email = request.json.get('email', None)
    password = request.json.get('password', None)

    if not email:
        return return_response({"msg": "Email missing.", "data": ""}, 400)
    if not password:
        return return_response({"msg": "Password missing.", "data": ""}, 400)
    if not first_name:
        return return_response({"msg": "First name missing.", "data": ""}, 400)
    if not last_name:
        return return_response({"msg": "Last name missing.", "data": ""}, 400)
    session = Session(expire_on_commit=False)
    try:
        email = email.lower()
        user = session.query(User).filter(User.email == email).first()
        if user is not None:
            message = "User exists already !! Please try with alternative " \
                      "email id."
            return return_response({"msg": message, "data": ""}, 400)
        else:
            user = User()
            user.email = email.lower()
            user.password = password
            user.first_name = first_name
            user.last_name = last_name
            session.add(user)
            session.commit()

            return return_response({"msg": "Signup is successful",
                                    "data": ""}, 200)
    except Exception as e:
        return return_response({"msg": "Internal Error!, Please try later",
                                "data": ""}, 500)
    finally:
        session.close()


@auth_api.route("/login", methods=['POST', 'OPTIONS'])
@cross_origin()
def login():
    """User login API"""
    try:
        if request.method == "OPTIONS":
            return return_response({"Content-Type": "application/json"}, 200)
        if not request.is_json:
            return return_response(
                {"msg": "Missing JSON in request", "data": ""},
                400)

        email = request.json.get('email', None)
        password = request.json.get('password', None)
        session = Session(expire_on_commit=False)
        if not email:
            return return_response(
                {"msg": "Missing email parameter", "data": ""},
                400)
        if not password:
            return return_response(
                {"msg": "Missing password parameter", "data": ""},
                400)

        res = dict()
        try:
            user = session.query(User).filter(User.email == email.lower()).first()
            if user is None:
                message = "User does not exists !! Please try to signup."
                return return_response({"msg": message, "data": ""}, 400)
            if user is not None:
                if user.email == email.lower() and user.password == password:
                    user_info = {
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'r_key': uuid.uuid4().hex
                    }
                    res["data"] = {
                        'access_token': create_access_token(identity=user_info,fresh=True),
                        'refresh_token': create_refresh_token(identity=user_info),
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email
                    }

                    res["msg"] = "Login Successful"
                    return return_response(res, status=200)
                else:
                    res["data"] = {}
                    res["msg"] = "Username/Password incorrect!! please try again"
                    return return_response(res, status=400)
        except Exception as ex:
            print(ex)
            return return_response({'msg': "Internal Error!, Please try later",
                                    "data": ""}, status=500)
    except Exception as e:
        return return_response({'msg': "Internal Error!, Please try later",
                                "data": ""}, status=500)
