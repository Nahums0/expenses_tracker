# Import necessary Flask modules and other dependencies
from flask import Blueprint, request
from app.database.models import Transaction, User, AppUserCredentials, UserCategorySpending, UserParsedCategory, UserCategory, db
from app.api.helpers import get_user_object
from app.credit_card_adapters.max_fetcher import login_user
from config.app import INVITE_KEY
from app.helper import RegistrationForm, create_response, hash_password, verify_password
from app.logger import log
from flask_jwt_extended import jwt_required, get_jwt_identity

APP_NAME = "Users Controller"

users_bp = Blueprint("users", __name__, url_prefix="/api")


@users_bp.route("/login", methods=["POST"])
def login():
    """Endpoint to login a user."""
    try:
        # Extract user data from the request
        data = request.get_json()
        email = data.get("email", "")
        password = data.get("password", "")

        # Log the login attempt
        log(APP_NAME, "INFO", f"Login request received for email: {email}, from IP: {request.remote_addr}")

        # Authenticate the user
        user = User.query.filter_by(email=email).first()
        if not user or not verify_password(password, user.password):
            # Log failed login
            log(APP_NAME, "DEBUG", f"Login failed for email: {email}")
            return create_response("Incorrect credentials", 400)

        # Prepare the response for successful login
        response_body = {"user": get_user_object(email)}

        return create_response("Login successful", 200, response_body)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Login failed for email: {email}, Error: {e}")
        return create_response("An error occurred during login.", 500)


@users_bp.route("/register", methods=["POST"])
def register():
    """Endpoint to register a new user."""
    try:
        # Extract registration data from the request
        data = request.get_json()
        email = data["email"]
        invite_key = data["inviteKey"]

        # Log the registration attempt
        log(APP_NAME, "INFO", f"Registration request received for email: {email}, from IP: {request.remote_addr}")

        # Validate the registration form
        form = RegistrationForm(data=data)
        if not form.validate_on_submit():
            log(APP_NAME, "DEBUG", f"Registration form validation failed for user: {email}, errors: {form.errors}")
            return create_response(f"Form validation failed", 400)

        # Check if the email is already registered
        if User.query.filter_by(email=email).first():
            log(APP_NAME, "DEBUG", f"Registration failed for user: {email}, user already registered")
            return create_response("Email already registered", 400)

        # Verify invite key
        if invite_key != INVITE_KEY:
            log(APP_NAME, "DEBUG", f"Registration form validation failed for user: {email}, invalid invite key")
            return create_response("Invalid invite key", 401)

        # Create a new user and associated credentials
        user = User(email=email, password=hash_password(data["password"]))

        # Save the new user to the database
        db.session.add(user)
        db.session.commit()

        # Prepare the response for successful login
        response_body = {"user": get_user_object(email)}

        log(APP_NAME, "INFO", f"User registered successfully for email: {email}")
        return create_response("Registration successful", 200, response_body)

    except Exception as e:
        # Roll back in case of exceptions and logging the error
        db.session.rollback()
        log(APP_NAME, "ERROR", f"Registration failed for email: {email}, Error: {e}")
        return create_response("Registration failed", 500)


@users_bp.route("/delete", methods=["POST"])
@jwt_required()
def delete_user():
    """Endpoint to delete a user and their associated data."""
    email = get_jwt_identity()
    log(APP_NAME, "INFO", f"User deletion request received for email: {email}, from IP: {request.remote_addr}")

    user = User.query.filter_by(email=email).first()
    if not user:
        # Log if the user does not exist
        log(APP_NAME, "DEBUG", f"User deletion failed for email: {email}")
        return create_response("User deletion failed", 400)

    try:
        # Collect all related data for deletion
        related_data = [
            UserCategorySpending.query.filter(UserCategorySpending.userEmail == email).all(),
            UserCategory.query.filter(UserCategory.owner == email).all(),
            Transaction.query.filter(Transaction.userEmail == email).all(),
            UserParsedCategory.query.filter(UserParsedCategory.userEmail == email).all(),
            AppUserCredentials.query.filter(AppUserCredentials.userEmail == email).all(),
            [user],
        ]

        # Delete the user and related data
        for records in related_data:
            for record in records:
                db.session.delete(record)

        db.session.commit()
        log(APP_NAME, "INFO", f"User deleted successfully: {email}")
        return create_response("Deletion successful", 200)

    except Exception as e:
        # Roll back in case of exceptions and logging the error
        db.session.rollback()
        log(APP_NAME, "ERROR", f"User deletion failed for email: {email}, Error: {e}")
        return create_response("Deletion failed", 500)


@users_bp.route("/setup-user", methods=["POST"])
@jwt_required()
def setup_user():
    """
    Endpoint for setting up a user profile beyond basic registration.
    Updates user details, categories, and credentials in the database.
    """
    email = get_jwt_identity()
    log(APP_NAME, "INFO", f"User setup request received for email: {email}, from IP: {request.remote_addr}")

    try:
        # Locate the user in the database
        user = User.query.filter_by(email=email).first()
        if not user:
            raise ValueError("User not found")

        # Check if the user has already completed the initial setup
        if user.initialSetupDone:
            log(APP_NAME, "DEBUG", f"User has been set up before")
            return create_response("User already passed initial setup", 409)

        # Extract setup data from the request
        data = request.get_json()
        monthly_budget = data.get("budget")
        categories = data.get("categories")
        full_name = data.get("fullName")
        currency = data.get("currency")
        cc_credentials = data.get("creditCardCredentials")

        # Update user fields
        user.fullName = full_name
        user.currency = currency
        user.monthlyBudget = monthly_budget

        # Create or update AppUserCredentials
        app_user_credentials = AppUserCredentials.query.filter_by(userEmail=email).first()
        if app_user_credentials:
            # Update existing credentials
            app_user_credentials.username = (cc_credentials["username"],)
            app_user_credentials.password = (cc_credentials["password"],)
            app_user_credentials.identityDocumentNumber = (cc_credentials["id"],)
        else:
            # Add new credentials
            new_credentials = AppUserCredentials(
                userEmail=email,
                username=cc_credentials["username"],
                password=cc_credentials["password"],
                identityDocumentNumber=cc_credentials["id"],
            )
            db.session.add(new_credentials)

        # Process categories
        user_categories = []
        for category in categories:
            user_categories.append(
                UserCategory(
                    owner=email,
                    monthlyBudget=category["budget"],
                    categoryName=category["categoryName"]
                )
            )

        user.initialSetupDone = True
        db.session.add_all(user_categories)
        db.session.commit()

        log(APP_NAME, "INFO", f"User setup finished successfully for email: {email}")
        return create_response("User setup successful", 200, {"user": get_user_object(email)})
    except Exception as e:
        db.session.rollback()
        log(APP_NAME, "ERROR", f"Error in user setup for email: {email}, error: {e}")
        return create_response("Setup failed", 500)


@users_bp.route("/test-cc-credentials", methods=["POST"])
@jwt_required()
def test_credit_card_credentials():
    """Endpoint for testing credit card credentials provided by the user"""
    email = get_jwt_identity()
    log(APP_NAME, "INFO", f"Credit card credential test request received for email: {email}, from IP: {request.remote_addr}")

    try:
        data = request.get_json()
        username = data["username"]
        password = data["password"]
        identity_document_number = data["id"]

        # Attempt to log in with the provided credentials
        login_result = login_user({"username": username, "password": password, "id": identity_document_number})
        if login_result:
            log(APP_NAME, "INFO", f"Credit card credentials validated for email: {email}")
            return create_response("Credentials are valid", 200)
        else:
            # Log and return in case of invalid credentials
            log(APP_NAME, "WARNING", f"Invalid credit card credentials for email: {email}")
            return create_response("Invalid credentials", 401)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error testing credit card credentials for email: {email}: {e}")
        return create_response("Internal server error", 500)


@users_bp.route("/get-user-data", methods=["GET"])
@jwt_required()
def get_user_data():
    """Endpoint for fetching user data"""

    email = get_jwt_identity()
    log(APP_NAME, "INFO", f"User data request received for email: {email}, from IP: {request.remote_addr}")

    try:
        user_object = get_user_object(email)
        log(APP_NAME, "INFO", f"Successfully fetched user data for email: {email}")
        return create_response("Successfully fetched user data", 200, user_object)
    except Exception as e:
        log(APP_NAME, "ERROR", f"Error fetching user data for email: {email}: {e}")
        return create_response("Internal server error", 500)

