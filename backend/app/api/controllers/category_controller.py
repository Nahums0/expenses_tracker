from flask import Blueprint, request
from sqlalchemy import or_
from app.database.models import Category, UserCategoryData, UserParsedCategory, db
from app.helper import create_response
from app.logger import log
from flask_jwt_extended import jwt_required, get_jwt_identity

APP_NAME = "Category Controller"
category_bp = Blueprint("categories", __name__, url_prefix="/api")

@category_bp.route("/get_categories_spending", methods=["GET"])
@jwt_required()
def get_categories_spending():
    pass  # TODO: Implement logic to get categories spending


@category_bp.route("/get-user-categories", methods=["GET"])
@jwt_required()
def get_user_categories():
    """
    Retrieve categories specific to a user.
    """
    email = get_jwt_identity()
    try:
        log(APP_NAME, "DEBUG", f"Fetching categories for email: {email}")
        # Query user-specific categories
        user_categories = UserCategoryData.query.filter(UserCategoryData.userEmail == email)
        user_categories = [category.serialize() for category in user_categories]

        return create_response("Successfully fetched user's categories", 200, user_categories)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error fetching categories for email: {email}: {str(e)}")
        return create_response("An error occurred while fetching categories", 500)


@category_bp.route("/create_category", methods=["POST"])
@jwt_required()
def create_category():
    pass  # TODO: Implement logic to create a new category


@category_bp.route("/delete_category", methods=["POST"])
@jwt_required()
def delete_category():
    pass  # TODO: Implement logic to delete a category


@category_bp.route("/rename_category", methods=["POST"])
@jwt_required()
def rename_category():
    pass  # TODO: Implement logic to rename a category


@category_bp.route("/set_merchant/<by>", methods=["POST"])
@jwt_required()
def set_merchant(by="id"):
    """
    Set a merchant for a specific category.
    """
    merchant_name = request.form.get("merchant_name")
    target_category_id = request.form.get("target_category_id")
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

@category_bp.route("/get-defaults", methods=["GET"])
def get_defaults():
    """
    Retrieve default categories.
    """
    try:
        IGNORED_CATEGORIES = [-1]
        default_categories = Category.query.filter(Category.owner == None)
        default_categories_list = []

        for category in default_categories:
            if category.id in IGNORED_CATEGORIES:
                continue
            default_categories_list.append(category.serialize())

        return create_response("Fetch successful", 200, default_categories_list)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Default routes fetch failed, Error: {str(e)}")
        return create_response("Fetch failed", 500)
