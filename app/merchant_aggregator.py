import re

from sqlalchemy import and_, or_
from app.database.models import Category, UserParsedCategory, db
from app.helper import get_prompt_template, query_chatgpt


def extract_merchant_name(transaction):
    # Extract everything before special characters or numbers
    merchant = re.split(r"[\*\(\)\[\]\{\}\<\>\#\&\%\$\@\!\?0-9]", transaction)[
        0
    ].strip()
    return merchant


def set_categories_for_user(transactions, user_email):
    parsed_categories_dict = {}
    unparsed_transactions = []

    previously_parsed_categories = UserParsedCategory.query.filter(
        or_(
            UserParsedCategory.userEmail == user_email,
            UserParsedCategory.userEmail == None,
        )
    ).all()
    
    # Create a dictionary of available categories, with the chargingBusiness as the key
    for category in previously_parsed_categories:
        parsed_categories_dict[category.chargingBusiness] = category.targetCategoryId 

    # Iterate through each transaction and try to match it to a category
    for transaction in transactions:
        merchant_name = extract_merchant_name(transaction.merchantData["name"])
        if merchant_name in parsed_categories_dict:
            transaction.categoryId = parsed_categories_dict[merchant_name]
        else:
            unparsed_transactions.append(transaction)
        
    user_categories = Category.query.filter(
        and_(
            or_(
                Category.owner == None,
                Category.owner == user_email
            ),
            Category.categoryName != "Unknown"
        )
    ).all()
    parse_merchants_for_user(unparsed_transactions, user_categories)

def parse_merchants_for_user(transactions, user_categories):
    user_categories_dict = {category.categoryName:category.id for category in user_categories}
    categories_string = ""

    for category in user_categories:
        categories_string += f"{category.categoryName},"

    transactions_string = ""
    for transaction in transactions:
        transactions_string += f'"{transaction.merchantData["name"]}"\n'

    prompt = get_prompt_template(categories_string, transactions_string)

    # Send prompt to chatgpt api
    chatgpt_response = query_chatgpt(prompt)
    chatgpt_response = chatgpt_response[chatgpt_response.find("Category for 1:"):]

    categories = chatgpt_response.split("\n")
    index = 0

    for category in categories:
        category_name = category.split(": ")[1].strip()
        category_id = user_categories_dict[category_name]
        transactions[index].categoryId = category_id
        index += 1


    print(chatgpt_response)


def set_categories_for_transactions(transactions_dict):
    for email, transactions_list in transactions_dict.items():
        parsed_category = set_categories_for_user(transactions_list, email)

        if parsed_category is not None:
            transactions_list.category_id = parsed_category
            continue
    
    return transactions_dict
