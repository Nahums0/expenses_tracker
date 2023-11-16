from datetime import datetime
import json
import requests
from app.database.models import Transaction
from config import max_urls

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
    return datetime.strptime(date_string, date_format)


def build_transactions_url(start_date, end_date):
    """
    Build the URL for fetching transactions data based on start and end dates.
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


def login_user(user_credentials):
    """
    Login the user and return the cookies if successful.
    """
    response = requests.post(LOGIN_URL, headers=HEADERS, json=user_credentials)
    if response.status_code != 200:
        raise Exception(f"Login failed for user: {user_credentials['username']}, status_code: {response.status_code}")

    login_status = json.loads(response.text).get('Result', {}).get('LoginStatus')
    if login_status == 0:
        return response.cookies.get_dict()
    else:
        return None


def fetch_transactions_from_max(user_credentials: dict, start_date: datetime, end_date: datetime, user_email:str) -> list:
    """
    Fetch transactions data for a user within a specified date range.
    """

    cookies_for_requests = login_user(user_credentials)
    if not cookies_for_requests:
        raise Exception(f"Failed to login for user: {user_email}, with the login email: {user_credentials['username']}")

    transactions_url = build_transactions_url(start_date, end_date)
    response = requests.get(transactions_url, cookies=cookies_for_requests)
    transactions_data = json.loads(response.content.decode("utf-8"))

    if transactions_data["result"] is None:
        return []

    parsed_transactions = [
        Transaction(
            id=f"{user_email}_{transaction['arn']}",
            arn=transaction["arn"],
            userEmail=user_email,
            categoryId=-1,
            transactionAmount=float(transaction["actualPaymentAmount"]),
            paymentDate=parse_date_string(transaction["paymentDate"]),
            purchaseDate=parse_date_string(transaction["purchaseDate"]),
            shortCardNumber=transaction["shortCardNumber"],
            merchantData={**transaction["merchantData"], "name": transaction["merchantName"]},
            originalCurrency=transaction["originalCurrency"],
            originalAmount=transaction["originalAmount"],
            isRecurring=False
        )
        for transaction in transactions_data["result"]["transactions"]
    ]

    parsed_transactions = sorted(parsed_transactions, key=lambda item: item.purchaseDate)
    return parsed_transactions
