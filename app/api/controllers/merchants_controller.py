from flask import Blueprint, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from app.database.models import UserParsedCategory, db

merchants_bp = Blueprint('merchants', __name__, url_prefix="/api")




@merchants_bp.route('/delete_merchant', methods=['DELETE'])
@jwt_required()
def delete_merchant():
    return #TODO: Implement -> delete a merchant
    merchant_id = request.args.get('merchant_id')
    authorization = request.headers.get('Authorization')
    # Your implementation here
    return {"message": "Merchant deleted successfully."}
