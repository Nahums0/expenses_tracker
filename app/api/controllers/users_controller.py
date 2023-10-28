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
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

APP_NAME = "Users Controller"
users_bp = Blueprint("users", __name__, url_prefix="/api")


@users_bp.route("/login", methods=["POST"])
def login():
    """Endpoint to login a user."""
    data = request.get_json()
    email = data.get("email", "")
    password = data.get("password", "")

    log(APP_NAME, "INFO", f"Login request received for email: {email}, from IP: {request.remote_addr}")

    form = UserLoginForm(data=data)
    if not form.validate_on_submit():
        log(APP_NAME, "DEBUG", f"Form validation for login failed for user: {email}, errors: {form.errors}")
        return create_response(f"Form validation failed, errors: {form.errors}", 400)

    user = User.query.filter_by(email=email).first()
    if not user or not verify_password(password, user.password):
        log(APP_NAME, "DEBUG", f"Login failed for email: {email}")
        return create_response("Incorrect credentials", 400)

    access_token = create_access_token(identity=email)
    return create_response("Login successful", 200, {"access_token": access_token})


@users_bp.route("/get_user_data", methods=["POST"])
@jwt_required()
def get_user_data():
    """Endpoint to get user data."""
    email = get_jwt_identity()

    log(APP_NAME, "INFO", f"Request to get user data for email: {email}, from IP: {request.remote_addr}")

    user = User.query.filter_by(email=email).first()
    if not user:
        log(APP_NAME, "DEBUG", f"User data request failed for email: {email}")
        return create_response("User not found", 400)

    user_data = {"email": user.email}
    log(APP_NAME, "INFO", f"User data fetched successfully for email: {email}")
    return create_response("User data fetched successfully", 200, user_data)


@users_bp.route("/register", methods=["POST"])
def register():
    """Endpoint to register a new user."""
    data = request.get_json()
    email = data.get("email", "")
    invite_key = data.get("invite_key", "")

    log(APP_NAME, "INFO", f"Registration request received for email: {email}, from IP: {request.remote_addr}")

    form = RegistrationForm(data=data)
    if not form.validate_on_submit():
        log(APP_NAME, "DEBUG", f"Registration form validation failed for user: {email}, errors: {form.errors}")
        return create_response(f"Form validation failed, errors: {form.errors}", 400)

    if User.query.filter_by(email=email).first():
        return create_response("Email already registered", 400)

    if invite_key != INVITE_KEY:
        return create_response("Invalid invite key", 401)

    try:
        user = User(email=email, password=hash_password(data.get("password", "")))
        user_credentials = AppUserCredentials(
            userEmail=email,
            username=data.get("appUsername", ""),
            password=data.get("appPassword", ""),
            identityDocumentNumber=data.get("appIdentityDocumentNumber", "")
        )

        user.appUserCredentials = user_credentials

        db.session.add(user)
        db.session.commit()

        access_token = create_access_token(identity=email)
        log(APP_NAME, "INFO", f"User registered successfully for email: {email}")
        return create_response("Registration successful", 200, {"access_token": access_token})

    except Exception as e:
        log(APP_NAME, "ERROR", f"Registration failed for email: {email}, Error: {str(e)}")
        return create_response("Registration failed", 500)


@users_bp.route("/delete", methods=["POST"])
@jwt_required()
def delete_user():
    """Endpoint to delete a user and their associated data."""
    email = get_jwt_identity()

    log(APP_NAME, "INFO", f"User deletion request received for email: {email}, from IP: {request.remote_addr}")

    user = User.query.filter_by(email=email).first()
    if not user:
        log(APP_NAME, "DEBUG", f"User deletion failed for email: {email}")
        return create_response("User deletion failed", 400)

    try:
        related_data = [
            Category.query.filter(Category.owner == email).all(),
            Transaction.query.filter(Transaction.userEmail == email).all(),
            UserParsedCategory.query.filter(UserParsedCategory.userEmail == email).all(),
            UserCategoryData.query.filter(UserCategoryData.userEmail == email).all(),
            AppUserCredentials.query.filter(AppUserCredentials.userEmail == email).all(),
            [user]
        ]

        for records in related_data:
            for record in records:
                db.session.delete(record)

        db.session.commit()
        log(APP_NAME, "INFO", f"User deleted successfully: {email}")
        return create_response("Deletion successful", 200)

    except Exception as e:
        log(APP_NAME, "ERROR", f"User deletion failed for email: {email}, Error: {str(e)}")
        return create_response("Deletion failed", 500)
