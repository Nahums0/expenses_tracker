from datetime import datetime
import re
from sqlalchemy import and_, or_
from app.database.models import UserParsedCategory, UserCategory


def _extract_merchant_from_transaction(merchant_name):
    """Extracts the merchant's name from the unparsed merchant_name string"""

    merchant = re.split(r"[\*\(\)\[\]\{\}\<\>\#\&\%\$\@\!\?0-9]", merchant_name)[0].strip()
    return merchant


def _get_categories_from_chatgpt_response(chatgpt_response):
    """Extracts the list of categories from a ChatGPT response string."""

    chatgpt_response = chatgpt_response.replace("END OF OUTPUT", "").strip()
    return chatgpt_response.split("\n")


def _retrieve_cached_categories(user_email):
    """Retrieve UserParsedCategories (cached) for a given user."""
    parsed_categories = UserParsedCategory.query.filter(
        or_(UserParsedCategory.userEmail == user_email, UserParsedCategory.userEmail == None)
    ).all()
    return {category.chargingBusiness: category.targetCategoryId for category in parsed_categories}


def _get_user_categories_dict(user_email):
    """Get user categories as a dictionary."""
    user_categories = UserCategory.query.filter(
        and_(
            or_(UserCategory.owner == None, UserCategory.owner == user_email),
            UserCategory.categoryName != "Unparsed",
        )
    ).all()

    return {
        category.categoryName: {
            "id": category.id,
            "is_custom": (category.owner is not None),
            # is_custom: True for custom (user-specific) categories, False for global categories
        }
        for category in user_categories
    }


def _has_timed_out(start_time, duration):
    """Return True if timeout is reached"""
    return (datetime.now() - start_time).seconds >= duration


def _split_into_chunks(data_list, chunk_size):
    """Split the list into smaller chunks"""

    return [data_list[i : i + chunk_size] for i in range(0, len(data_list), chunk_size)]


def _serialize_transactions(transactions):
    return [t.serialize() for t in transactions]