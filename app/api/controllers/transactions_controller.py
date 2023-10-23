import json
import pickle
from flask import Flask, Response, jsonify, make_response, request
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.transactions_fetcher import fetch_transactions

transactions_bp = Blueprint("transactions", __name__, url_prefix="/api")
APP_NAME = "Transactions Controller"


## Manual actions ##
@transactions_bp.route("/add_transaction", methods=["POST"])
@jwt_required()
def add_transaction():
    pass #TODO: implement -> This is an option to manually add a transaction

@transactions_bp.route("/delete_transaction", methods=["POST"])
@jwt_required()
def delete_transaction():
    pass #TODO: implement -> This is an option to manually delete a transaction

@transactions_bp.route("/get_transactions", methods=["GET"])
@jwt_required()
def get_transactions():
    pass #TODO: implement -> Return transactions for a user -> filtered and sorted

@transactions_bp.route("/update_transaction", methods=["POST"])
@jwt_required()
def update_transaction():
    pass #TODO: implement -> This is an option to manually update a transaction



# @transactions_bp.route("/get", methods=['GET'])
# def get():
#     # with open("credentials.json", "r") as file:
#     #     user_credentails = json.loads(file.read())

#     # # res = fetch_transactions.apply_async(user_credentails, queue='transactions_fetch', countdown=0)
#     # res = fetch_transactions(user_credentails=user_credentails)
#     # transactions = parse_transactions_html(res)
#     # serialized_data = pickle.dumps(transactions)
    
#     with open("pickle", "rb") as file:
#         transactions = pickle.load(file)
#     return Response(json.dumps(transactions, ensure_ascii=False), content_type='application/json; charset=utf-8')
#     return make_response(json.dumps(transactions, ensure_ascii=False), 200)
#     return json.dumps(transactions, ensure_ascii=False)