from app.database.models import User, AppUserCredentials

def test_successful_user_registration(app, test_client, user_email):
    """
    Test a successful user registration.
    """
    # Create valid user registration data
    user_data = {
        "email": user_email,
        "password": "12345678",
        "invite_key": "2973322023",
        "appUsername": "omer",
        "appPassword": "123456",
        "appIdentityDocumentNumber": "123456789",
    }

    # Send a POST request to the registration endpoint
    response = test_client.post("/api/users/register", json=user_data)

    # Check if the registration was successful (HTTP status code 200)
    assert response.status_code == 200

    # Check if the user and credentials were created in the database
    with app.app_context():
        user = User.query.filter_by(email=user_data["email"]).first()
        credentials = AppUserCredentials.query.filter_by(userEmail=user_data["email"]).first()
    assert user is not None
    assert credentials is not None

def test_user_registration_validation_failure(app, test_client):
    """
    Test user registration failure due to validation errors.
    """
    # Create user registration data with validation errors
    request_data = {
        "email": "invalid_email",  # Invalid email
        "password": "short",       # Password too short
        "invite_key": "invalid_key",
        "appUsername": "short",    # Username too short
        "appPassword": "short",    # Password too short
        "appIdentityDocumentNumber": "invalid_number",  # Invalid number
    }

    # Send a POST request to the registration endpoint
    response = test_client.post("/api/users/register", json=request_data)

    # Check if the registration failed due to validation (HTTP status code 400)
    assert response.status_code == 400

def test_user_deletion_success(app, test_client, user_email):
    """
    Test successful user deletion.
    """
    request_data = {
        "email": user_email
    }

    response = test_client.post("/api/users/delete", json=request_data)
    assert response.status_code == 200

def test_get_user_data_success(app, test_client, user_email):
    """
    Test successful user data retrieval.
    """
    request_data = {
        "email": user_email
    }

    response = test_client.post("/api/users/get_user_data", json=request_data)
    assert response.status_code == 200
