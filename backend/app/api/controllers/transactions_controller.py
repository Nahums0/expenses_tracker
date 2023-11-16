from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.transaction_fetchers.max_fetcher import fetch_transactions_from_max

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

@transactions_bp.route("/force_transactions_fetch", methods=["POST"])
@jwt_required()
def force_transactions_fetch():
    pass #TODO: implement -> This is an option to force a transaction fetch for a user
