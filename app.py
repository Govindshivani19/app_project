import uuid
from flask import Flask
from api import *
from flask_jwt_extended import JWTManager
from os import getenv
# from db_connect import redis_client as rc
from flask_session import Session

application = Flask(__name__)
Session(application)

application.register_blueprint(auth_api, url_prefix='/auth')
application.register_blueprint(product_api, url_prefix='/product')


application.config['JWT_HEADER_NAME'] = "XCkToken"
application.config['JWT_HEADER_TYPE'] = ""

application.config['JWT_ACCESS_TOKEN_EXPIRES'] = 3600
application.config['JWT_SECRET_KEY'] = "1oUw#511.:sesM"
application.config['JWT_REFRESH_TOKEN_EXPIRES'] = 7200
application.config['SQLALCHEMY_POOL_SIZE'] = 100
application.config['SQLALCHEMY_POOL_RECYCLE'] = 280
application.config['JWT_BLACKLIST_ENABLED'] = True
application.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
application.config['JSON_SORT_KEYS'] = False
application.secret_key = uuid.uuid4().hex
jwt = JWTManager(application)


# @jwt.user_claims_loader
# def add_claims_to_access_token(user):
#     r_key = user['r_key']
#     rc.set(r_key, json.dumps(
#         {
#             'user_hash': user.get('user_hash'),
#             'customer_hash': user.get('customer_hash'),
#             'access_level': user.get('access_level'),
#             'mapped_accounts': user.get('mapped_accounts'),
#             'modules': user.get('modules'),
#             "sub_functions": user.get('sub_functions'),
#             "is_custom": user.get('is_custom')
#         }
#     ),
#            ex=87000
#            )
#     return {'user_hash': user['user_hash']}


@jwt.token_in_blacklist_loader
def check_if_token_is_revoked(payload):
    """
    This function checks if the user JWT token is block listed in redis cache or not.
    If a user tries to login with JWT token where user is already successfully logged. This function will make sure
    that protected routes in the application will not be accessible.
    :param payload: A data object containing user login specific information
    :return: It returns a True value if user already block listed. Otherwise return False
    """

    token_identifier = payload['jti']
    token_in_redis = rc.get(token_identifier)
    return token_identifier is not None


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user['r_key']


@application.route("/health")
def health():
    return "Hello API!"


# @application.after_request
# def after_request_func(response):
#     response.headers["Access-Control-Allow-Origin"] = "*"
#     ActivityLogging().add_item(response)
#     return response


if __name__ == "__main__":
    application.config['SESSION_TYPE'] = 'filesystem'
    application.run(host='0.0.0.0', debug=getenv('debug', True))
