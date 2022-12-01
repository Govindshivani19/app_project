import smtplib
from email.message import EmailMessage

from flask import Blueprint
from flask import request
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity

from api.helper import return_response
from db_connect import Session
from model.db_models import Product, User, Ordered_info

product_api = Blueprint('product_api', __name__)


@product_api.route("/get_products", methods=['GET', 'OPTIONS'])
# @jwt_required
@cross_origin()
def get_products():
    try:
        if request.method == "OPTIONS":
            return return_response({"Content-Type": "application/json"}, 200)
        result = []
        res = {
            'data': result,
        }
        session = Session(expire_on_commit=False)
        try:
            products_info = session.query(Product).all()
            if products_info:
                for product in products_info:
                    prod_res = {
                        'id': product.id,
                        'category': product.category_name,
                        'name': product.product_name,
                        'price': product.price,
                        'discounted_price': product.discounted_price,
                        'discounted_percentage': product.discounted_percentage,
                        'image_url': product.image_url
                    }
                    result.append(prod_res)
                res['status'] = 200
                res['msg'] = "products info fetched successfully"
            else:
                res['status'] = 200
                res['msg'] = "no products info "
            return res
        except Exception as ex:
            return return_response({'msg': "Internal Error!, Please try later",
                                    "data": ""}, status=500)
    except Exception as e:
        return return_response({'msg': "Internal Error!, Please try later",
                                "data": ""}, status=500)


@product_api.route("/ordered_products", methods=['POST', 'OPTIONS'])
# @jwt_required
@cross_origin()
def ordered_products():
    try:
        if request.method == "OPTIONS":
            return return_response({"Content-Type": "application/json"}, 200)
        if not request.is_json:
            return return_response(
                {"msg": "Missing JSON in request", "data": ""},
                400)

        user_id = request.json.get('user_id', None)
        ordered_data = request.json.get('ordered_data', {})
        session = Session(expire_on_commit=False)
        if not user_id:
            return return_response(
                {"msg": "Missing user_id parameter", "data": ""},
                400)
        if len(ordered_data) == 0:
            return return_response(
                {"msg": "Missing ordered_data parameter", "data": ""},
                400)

        res = dict()
        try:
            user = session.query(User).filter(User.id == user_id).first()
            if user is None:
                message = "User does not exists !! "
                return return_response({"msg": message, "data": ""}, 400)
            if user is not None:
                order_data = Ordered_info()
                order_data.user_id = user_id
                order_data.ordered_data = ordered_data
                session.add(order_data)
                session.commit()

                res["msg"] = "Ordered placed Successfully"
                send_email('shivanigovind4251@gmail.com')
                return return_response(res, status=200)
        except Exception as ex:
            return return_response({'msg': "Internal Error!, Please try later",
                                    "data": ""}, status=500)
    except Exception as e:
        return return_response({'msg': "Internal Error!, Please try later",
                                "data": ""}, status=500)


def send_email(sender_email):
    EMAIL_ADDRESS = 'harryroger1602@gmail.com'
    EMAIL_PASSWORD = 'harry143@$'
    msg = EmailMessage()
    msg['Subject'] = 'Ordered Placed'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = sender_email
    msg.set_content('''
    <!DOCTYPE html>
    <html>
        <body>
            <div style="background-color:#eee;padding:10px 20px;">
                <h2 style="font-family:Georgia, 'Times New Roman', Times, serif;color#454349;">My newsletter</h2>
            </div>
            <div style="padding:20px 0px">
                <div style="height: 500px;width:400px">
                    <img src="https://dummyimage.com/500x300/000/fff&text=Dummy+image" style="height: 300px;">
                    <div style="text-align:center;">
                        <h3>Article 1</h3>
                        <p>Lorem ipsum dolor sit amet consectetur, adipisicing elit. A ducimus deleniti nemo quibusdam iste sint!</p>
                        <a href="#">Read more</a>
                    </div>
                </div>
            </div>
        </body>
    </html>
    ''', subtype='html')

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
