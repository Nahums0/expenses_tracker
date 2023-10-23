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
    create_access_token,
    jwt_required, get_jwt_identity
)
from lib.jwt.jwt import jwt


APP_NAME = "Users Controller"
users_bp = Blueprint("users", __name__, url_prefix="/api")

@users_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        email = data.get("email")
        password = data.get("password")
        form = UserLoginForm(data=data)

        # Log the user get request
        log(APP_NAME, "INFO", f"A Login request received for email: {email}, from IP: {request.remote_addr}")

        # Check if the form data is valid
        if not form.validate_on_submit():
            # Handle form validation failure
            log(APP_NAME, "DEBUG", f"Form validation for login request had failed for user: {email}, form errors: {form.errors}")
            return create_response(f"Form validation failed, error_list: {form.errors}", 400)

        # Check if the user with the provided email exists
        user = User.query.filter_by(email=email).first()
        if user is None:
            log(APP_NAME, "DEBUG", f"Login request had failed due to nonexistent/deleted user({email})")
            return create_response(f"Incorrect credentials", 400) #Fix all error code and messages (just from create_response)

        # Check if provided password is correct
        correct_password = verify_password(password, user.password)
        if correct_password is False:
            log(APP_NAME, "DEBUG", f"Login request had failed due to incorrect password ({email})")
            return create_response(f"Incorrect credentials", 400)
        
        access_token = create_access_token(identity=email)
        return create_response('Succesful login', 200, {'access_token':access_token})

    except Exception as e:
        # Handle exceptions and log the error
        email = data.get("email") 
        log(APP_NAME, "ERROR", f"The login request failed for email: {email}, Error: {str(e)}")
        return create_response("The login request had failed", 500)


@users_bp.route("/get_user_data", methods=["POST"])
@jwt_required()
def get_user_data():
    email = get_jwt_identity()
    try:
        # Log the user get request
        log(APP_NAME, "INFO", f"A get_user_data request received for email: {email}, from IP: {request.remote_addr}")

        # Check if the user with the provided email exists
        user = User.query.filter_by(email=email).first()
        if user is None:
            # Handle get_user_data failure due to nonexistent/deleted user
            log(APP_NAME, "DEBUG", f"The get_user_data request had failed due to nonexistent/deleted user({email})")
            return create_response("User deletion failed", 400)

        user_data = {
            'email': user.email
        }
        # Log successful user deletion
        log(APP_NAME, "INFO", f"A get_user_data response completed successfully : {email}, from IP: {request.remote_addr}")
        return create_response("User get request completed successful", 200, user_data)

    except Exception as e:
        # Handle exceptions and log the error
        log(APP_NAME, "ERROR", f"A get_user_data request failed for email: {email}, Error: {str(e)}")
        return create_response("A get_user_data request had failed", 500)


# Route for user registration
@users_bp.route("/register", methods=["POST"])
def register():
    # Extract data from the JSON request
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    invite_key = data.get("invite_key")
    appUsername = data.get("appUsername")
    appPassword = data.get("appPassword")
    appIdentityDocumentNumber = data.get("appIdentityDocumentNumber")

    # Log the registration request
    log(APP_NAME, "INFO", f"Registration request received for email: {email}, from IP: {request.remote_addr}")

    # Create a form object based on the request data
    form = RegistrationForm(data=data)

    # Check if the form data is valid
    if not form.validate_on_submit():
        # Log form validation failure and return a response
        email = form.email.data
        password = form.password.data
        log(APP_NAME, "DEBUG", f"Form validation for user registration had failed for user: {email}, form errors: {form.errors}")
        return create_response(f"Form validation failed, error_list: {form.errors}", 400)

    # Check if the email is already registered in the database
    emailRegistered = User.query.filter_by(email=email).first()
    if emailRegistered is not None:
        # Return a response indicating that the email is already registered
        return create_response("Email already registered", 400)

    # Check if the invite key matches the expected value (INVITE_KEY)
    if invite_key != INVITE_KEY:
        # Return a response indicating an incorrect invite key
        return create_response("Wrong invite key", 401)

    try:
        # Hash the password 
        hashed_password = hash_password(password)

        # Create a new User object with the email and hashed password
        user_object = User(email=email, password=hashed_password)

        # Create a new UserCredentials object with the provided data
        user_credentials_object = AppUserCredentials(
            userEmail=email,
            username=appUsername,
            password=appPassword,
            identityDocumentNumber=appIdentityDocumentNumber
        )

        # Associate the User and UserCredentials objects
        user_object.appUserCredentials = user_credentials_object

        # Add the User object to the database session
        db.session.add(user_object)

        # Commit the changes to the database
        db.session.commit()

        # Generate an access_token
        access_token = create_access_token(identity=email)

        # Return a success response
        log(APP_NAME, "INFO", f"Registration successful for email: {email}, from IP: {request.remote_addr}")
        return create_response("Registration successful", 200, {'access_token':access_token})
    except Exception as e:
        # If an exception occurs during registration, log the error and return an error response
        email = data.get("email")
        log(APP_NAME, "ERROR", f"Registration process failed for email: {email}, Error: {str(e)}")
        return create_response("Registration process failed", 500)


# Route for user deletion
@users_bp.route("/delete", methods=["POST"])
@jwt_required()
def delete():
    try:
        email = get_jwt_identity()
        data = request.get_json()

        # Log the user deletion request
        log(APP_NAME, "INFO", f"User deletion request received for email: {email}, from IP: {request.remote_addr}")

        # Check if the user with the provided email exists
        user = User.query.filter_by(email=email).first()
        if user is None:
            # Handle user deletion failure due to nonexistent/deleted user
            log(APP_NAME, "DEBUG", f"User deletion had failed due to nonexistent/deleted user({email})")
            return create_response("User deletion failed", 400)

        # Define a list of rows to delete from related tables
        rows_to_delete = [
            Category.query.filter(Category.owner == email).all(),
            Transaction.query.filter(Transaction.userEmail == email).all(),
            UserParsedCategory.query.filter(UserParsedCategory.userEmail == email).all(),
            UserCategoryData.query.filter(UserCategoryData.userEmail == email).all(),
            AppUserCredentials.query.filter(AppUserCredentials.userEmail == email).all(),
            [user]
        ]

        # Delete the user and the dependecy rows
        for rows in rows_to_delete:
            for row in rows:
                db.session.delete(row)

        db.session.commit()

        # Log successful user deletion
        log(APP_NAME, "INFO", f"User successfully deleted: {email}, from IP: {request.remote_addr}")
        return create_response("Deletion successful", 200)

    except Exception as e:
        # Handle exceptions and log the error
        email = data.get("email") 
        log(APP_NAME, "ERROR", f"User deletion process failed for email: {email}, Error: {str(e)}")
        return create_response("Deletion process failed", 500)
