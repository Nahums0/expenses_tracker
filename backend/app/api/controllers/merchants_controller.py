from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.database.models import Category, UserParsedCategory, db
from app.logger import log
from app.helper import create_response
from sqlalchemy import and_, or_

APP_NAME = "Merchants Controller"
merchants_bp = Blueprint('merchants', __name__, url_prefix="/api")

@merchants_bp.route('/set', methods=['POST'])
@jwt_required()
def set_merchant():
    """Endpoint to set a merchant for a user."""

    try:
        email = get_jwt_identity()

        # Validate JSON input
        if not request.is_json:
            log(APP_NAME, "ERROR", f"Merchant set failed for user: {email}, no json object received")
            return create_response("Invalid request body", 400)

        # Extract and validate data
        merchant_name, category_id = _extract_merchant_data(request.get_json())
        if not merchant_name or not category_id:
            log(APP_NAME, "ERROR", f"Merchant set failed for user: {email}, invalid arguments: {data}")
            return create_response("Invalid arguments", 400)

        # Check category validity
        if not _is_valid_category(category_id, email):
            log(APP_NAME, "ERROR", f"Merchant set failed for user: {email}, invalid category_id: {category_id}")
            return create_response("Invalid category_id", 400)

        # Add merchant
        _add_user_parsed_category(merchant_name, email, category_id)
        log(APP_NAME, "INFO", f"Merchant set successfully for user: {email}, category_id: {category_id}")
        return create_response("Merchant set successfully", 200)

    except Exception as e:
        log(APP_NAME, "ERROR", f"Merchant set failed, error: {str(e)}")
        return create_response("Merchant set failed", 500)


@merchants_bp.route('/delete', methods=['DELETE'])
@jwt_required()
def delete_merchant():
    """Endpoint to delete a merchant for a user."""

    try:
        email = get_jwt_identity()

        # Validate JSON input
        if not request.is_json:
            log(APP_NAME, "ERROR", f"Merchant deletion failed for user: {email}, no json object received")
            return create_response("Invalid request body", 400)

        # Extract merchant ID for deletion
        user_parsed_category_id = request.get_json().get("user_parsed_category_id", None)
        if not user_parsed_category_id:
            log(APP_NAME, "ERROR", f"Merchant deletion failed for user: {email}, missing user_parsed_category_id field")
            return create_response("Missing user_parsed_category_id", 400)

        # Validate existence and merchant ownership
        if not _is_merchant_owned_by_user(user_parsed_category_id, email):
            log(APP_NAME, "ERROR", f"Merchant deletion failed for user: {email}, either user_parsed_category_id doesn't exist or there's a merchant ownership issue")
            return create_response("Merchant ownership issue", 403)

        # Delete merchant
        _delete_merchant_mapping_from_db(user_parsed_category_id)
        log(APP_NAME, "INFO", f"Merchant deleted successfully, UserParsedCategory id: {user_parsed_category_id} for user: {email}")
        return create_response("Merchant deleted successfully", 200)

    except Exception as e:
        log(APP_NAME, "ERROR", f"Merchant deletion failed, error: {str(e)}")
        return create_response("Merchant deletion failed", 500)


def _is_merchant_owned_by_user(merchant_id, email):
    """Check if merchant belongs to the user."""

    merchant = UserParsedCategory.query.filter(
        and_(
            UserParsedCategory.id == merchant_id,
            or_(UserParsedCategory.userEmail == email, UserParsedCategory.userEmail == None),
        )
    ).first()
    return merchant is not None


def _delete_merchant_mapping_from_db(id):
    """Remove a merchant from the database."""

    merchant_to_delete = UserParsedCategory.query.filter(UserParsedCategory.id == id).first()
    db.session.delete(merchant_to_delete)
    db.session.commit()


def _extract_merchant_data(data):
    """Extract merchant data from provided JSON."""

    return data.get("name", None), data.get("category_id", None)


def _is_valid_category(category_id, email):
    """Validate if the category exists and belongs to the user."""

    category = Category.query.filter(Category.id == category_id).first()
    return category and (not category.owner or category.owner == email)


def _add_user_parsed_category(merchant_name, email, category_id):
    """Create or update UserParsedCategory for a merchant."""

    user_parsed_categories = UserParsedCategory.query.filter(
        UserParsedCategory.chargingBusiness == merchant_name,
        UserParsedCategory.userEmail == email
    ).all()

    if user_parsed_categories:
        for c in user_parsed_categories:
            c.targetCategoryId = category_id
    else:
        new_user_parsed_category = UserParsedCategory(chargingBusiness=merchant_name, userEmail=email, targetCategoryId=category_id)
        db.session.add(new_user_parsed_category)

    db.session.commit()
