import random
import string
import pytest
from app.database.app import initialize_database
from main import create_app
import tests.users_controller as user_controller_tests

@pytest.fixture
def app_and_client():
    app = create_app(initialize_db=False)
    app.config['TESTING'] = True
    initialize_database(app)
    return app, app.test_client()

def test_user_controller(app_and_client):
    app, test_client = app_and_client

    # Generate a random user email for testing
    length = 5
    characters = string.ascii_letters + string.digits
    user_email = f"{''.join(random.choice(characters) for _ in range(length))}@gmail.com"

    # Test user registration
    user_controller_tests.test_successful_user_registration(app, test_client, user_email)

    # Attempt to register the same user again (expecting failure)
    with pytest.raises(AssertionError):
        user_controller_tests.test_successful_user_registration(app, test_client, user_email)

    # Test user data retrieval
    user_controller_tests.test_get_user_data_success(app, test_client, user_email)

    # Test user deletion
    user_controller_tests.test_user_deletion_success(app, test_client, user_email)

    # Attempt to retrieve user data after deletion (expecting failure)
    with pytest.raises(AssertionError):
        user_controller_tests.test_get_user_data_success(app, test_client, user_email)

if __name__ == '__main__':
    pytest.main()
