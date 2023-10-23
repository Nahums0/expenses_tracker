from flask import Blueprint, request
from app.database.models import (
    Category,
    Transaction,
    User,
    AppUserCredentials,
    UserCategoryData,
    UserParsedCategory,
    db,
)
from config.app import INVITE_KEY
from app.helper import RegistrationForm, UserLoginForm, create_response, hash_password, verify_password
from app.logger import log
from flask_jwt_extended import (
    JWTManager, create_access_token,
    jwt_required, get_jwt_identity
)

APP_NAME = "Category Controller"
category_bp = Blueprint("category", __name__, url_prefix="/api")

@category_bp.route("/get_categories_spending", methods=["GET"])
@jwt_required()
def get_categories_spending():
    pass #TODO: Implement -> return all of the user's spending grouped by categories


@category_bp.route("/create_category", methods=["POST"])
@jwt_required()
def create_category():
    pass #TODO: Implement -> create a new category


@category_bp.route("/delete_category", methods=["POST"])
@jwt_required()
def delete_category():
    pass #TODO: Implement -> delete a category


@category_bp.route("/rename_category", methods=["POST"])
@jwt_required()
def rename_category():
    pass #TODO: Implement -> rename a category


@category_bp.route('/set_merchant/<by>', methods=['POST'])
@jwt_required()
def set_merchant(by="id"):
    merchant_name = request.form.get('merchant_name')
    target_category_id = request.form.get('target_category_id')
    email = get_jwt_identity()
    
    if by != "id":
        # Create a new category
        target_category_id = create_category()




    db.session.add(
        UserParsedCategory(
            chargingBusiness=merchant_name,
            userEmail=email,
            targetCategoryId=target_category_id,
        )
    )
    db.session.commit()
