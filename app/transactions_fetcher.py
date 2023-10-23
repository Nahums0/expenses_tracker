from datetime import datetime
import json
import requests
from app.logger import log
from config import max_urls

app = None
APP_NAME = "Transactions Scraper"


def parse_date_string(date_string):
    """
    Parse a date string in the format 'YYYY-MM-DDTHH:MM:SS' to a datetime object.

    Args:
        date_string (str): Date string to be parsed.

    Returns:
        datetime.datetime: Parsed datetime object, or None if parsing fails.
    """
    try:
        date_format = "%Y-%m-%dT%H:%M:%S"
        date_obj = datetime.strptime(date_string, date_format)
        return date_obj
    except ValueError:
        return None


def build_transactions_url(start_date, end_date):
    """
    Build the URL for fetching transactions data based on start and end dates.

    Args:
        start_date (datetime.datetime): Start date for the transaction query.
        end_date (datetime.datetime): End date for the transaction query.

    Returns:
        str: Constructed transactions URL.
    """
    start_date_str = start_date.strftime("%d.%m.%y")
    end_date_str = end_date.strftime("%d.%m.%y")

    filter_data = {
        "userIndex": -1,
        "cardIndex": -1,
        "monthView": False,
        "date": "2023-09-26",
        "dates": {"startDate": start_date_str, "endDate": end_date_str},
        "bankAccount": {"bankAccountIndex": -1, "cards": None},
    }

    transactions_fetch_url = f"{max_urls.TRANSACTIONS_API}?filterData={json.dumps(filter_data)}&firstCallCardIndex=-1null&v=V4.13-master-Simpsons.13.103"
    return transactions_fetch_url.replace(" ", "")


def fetch_transactions(user_credentials: dict, start_date: datetime, end_date: datetime) -> list:
    """
    Fetch transactions data for a user within a specified date range.

    Args:
        user_credentials (dict): User credentials including username, password, and id.
        start_date (datetime.datetime): Start date for the transaction query.
        end_date (datetime.datetime): End date for the transaction query.
    """

    try:
        log(APP_NAME, 'INFO', f"Fetching transactions for user: {user_credentials['username']}")
        # Define the login URL
        login_url = "https://www.max.co.il/api/login/login"

        # Define the request headers
        headers = {
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

        # Define the login payload as JSON
        login_payload = {
            "username": user_credentials["username"],
            "password": user_credentials["password"],
            "id": user_credentials["id"],
        }

        # Make the POST request to perform the login
        response = requests.post(login_url, headers=headers, json=login_payload)
        response_data = json.loads(response.text)
        login_status = response_data.get('Result', None)

        # Check if login was successful
        if response.status_code == 200 and login_status is not None and login_status['LoginStatus'] == 0:
            log(APP_NAME, 'DEBUG', f"Successfully logged into user: {user_credentials['username']}")
        else:
            log(APP_NAME, 'ERROR', f"Failed to fetch transactions for user: {user_credentials['username']}, status_code: {response.status_code}, login status: {login_status}")
            raise Exception()

        log(APP_NAME, 'DEBUG', f"Fetching transactions data for user: {user_credentials['username']}")
        # Access the cookies from the response for later use in requests
        cookies_for_requests = response.cookies.get_dict()

        transactions_url = build_transactions_url(start_date, end_date)
        response = requests.get(transactions_url, cookies=cookies_for_requests)

        transactions = json.loads(response.content.decode("utf-8"))

        parsed_transactions = []

        for transaction in transactions["result"]["transactions"]:
            transaction_data = {
                "arn": transaction["arn"],
                "transaction_amount": float(transaction["actualPaymentAmount"]),
                "payment_date": parse_date_string(transaction["paymentDate"]),
                "purchase_date": parse_date_string(transaction["purchaseDate"]),
                "short_card_number": transaction["shortCardNumber"],
                "merchant_data": transaction["merchantData"],
                "category_id": transaction["categoryId"],
                "original_payment": {
                    "currency": transaction["originalCurrency"],
                    "amount": transaction["originalAmount"],
                },
            }
            transaction_data["merchant_data"]["name"] = transaction["merchantName"]
            parsed_transactions.append(transaction_data)

        parsed_transactions = sorted(
            parsed_transactions, key=lambda item: item["purchase_date"]
        )
        return parsed_transactions
    except Exception as e:
        error_message = ""
        if e.args:
            error_message = f"error: {e}"

        log(APP_NAME, 'ERROR', f"Reached an error while fetching transactions for user: {user_credentials.get('username')} {error_message}")
        return None