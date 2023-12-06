from datetime import datetime, timedelta
import json
import requests
from app.database.models import Transaction
from lib.encryption.aes_encryptor import decrypt
from config import max_urls
import uuid

# Constants
LOGIN_URL = "https://www.max.co.il/api/login/login"
HEADERS = {
    "accept": "application/json, text/plain, */*",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "content-type": "application/json",
    "origin": "https://www.max.co.il",
    "referer": "https://www.max.co.il/",
    "sec-ch-ua": '"Chromium";v="117", "Not;A=Brand";v="8"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
}


def parse_date_string(date_string):
    """
    Parse a date string in the format 'YYYY-MM-DDTHH:MM:SS' to a datetime object.
    """
    date_format = "%Y-%m-%dT%H:%M:%S"

    if date_string:
        return datetime.strptime(date_string, date_format)
    return None


def parse_transaction_amount(transaction_amount):
    """
    Parse transaction amount with null value handling
    """
    if transaction_amount:
        return float(transaction_amount)
    return 0.0


def build_transactions_url(dates):
    """
    Build the URL for fetching transactions data.
    :param dates: Tuple containing start and end dates, or None.
    """

    # Set the date to the first of the current month
    current_month_first_date = (datetime.now().replace(day=1) + timedelta(days=32)).replace(day=1).strftime("%Y-%m-%d")

    # Initialize filter data with default values
    filter_data = {
        "userIndex": -1,
        "cardIndex": -1,
        "monthView": dates is None,
        "date": current_month_first_date,
        "dates": {"startDate": "0", "endDate": "0"},
        "bankAccount": {"bankAccountIndex": -1, "cards": None},
    }

    # If dates are provided, extract and format them
    if dates:
        start_date_str = dates[0].strftime("%d.%m.%y")
        end_date_str = dates[1].strftime("%d.%m.%y")
        filter_data["dates"] = {"startDate": start_date_str, "endDate": end_date_str}

    # Construct the URL
    transactions_fetch_url = f"{max_urls.TRANSACTIONS_API}?filterData={json.dumps(filter_data)}&firstCallCardIndex=-1null&v=V4.13-master-Simpsons.13.103"
    return transactions_fetch_url.replace(" ", "")


def login_user(user_credentials, decrypt_password=True):
    """
    Login the user and return the cookies if successful.
    """
    try:
        decrypted_password = decrypt(user_credentials["password"]) if decrypt_password else user_credentials["password"]
    except Exception as e:
        raise Exception(f"Error decrypting password for user: {user_credentials['username']}: {e}")

    # Update the credentials with the decrypted password
    updated_user_credentials = {
        "username": user_credentials["username"],
        "password": decrypted_password,
        "id": user_credentials["id"],
    }

    response = requests.post(LOGIN_URL, headers=HEADERS, json=updated_user_credentials)
    if response.status_code != 200:
        raise Exception(f"Login failed for user: {user_credentials['username']}, status_code: {response.status_code}")

    login_status = json.loads(response.text).get("Result", {}).get("LoginStatus")
    if login_status == 0:
        return response.cookies.get_dict()
    else:
        return None


def fetch_transactions_from_max(user_credentials: dict, dates: tuple, user_email: str) -> list:
    """
    Fetch transactions data for a user within a specified date range.
    """

    cookies_for_requests = login_user(user_credentials)
    if not cookies_for_requests:
        raise Exception(f"Failed to login for user: {user_email}, with the login email: {user_credentials['username']}")

    transactions_url = build_transactions_url(dates)
    response = requests.get(transactions_url, cookies=cookies_for_requests)
    transactions_data = json.loads(response.content.decode("utf-8"))

    if transactions_data["result"] is None:
        return []

    user_transactions = []
    for transaction in transactions_data["result"]["transactions"]:
        t = Transaction(
            id=f"{user_email}_{transaction['arn']}",
            arn=transaction["arn"],
            userEmail=user_email,
            categoryId=-1,
            transactionAmount=parse_transaction_amount(transaction["actualPaymentAmount"]),
            paymentDate=parse_date_string(transaction["paymentDate"]),
            purchaseDate=parse_date_string(transaction["purchaseDate"]),
            shortCardNumber=transaction["shortCardNumber"],
            merchantData={**transaction["merchantData"], "name": transaction["merchantName"]},
            originalCurrency=transaction["originalCurrency"],
            originalAmount=transaction["originalAmount"],
            isRecurring=False,
            isPending=False,
            authorizationNumber=transaction["dealData"]["authorizationNumber"],
        )
        if transaction["arn"] is None:
            t.id = f"{user_email}_{uuid.uuid4()}_pending"
            t.isPending = True

        user_transactions.append(t)

    return user_transactions
