from app.database.models import UserCategory, db

def db_seed():
    # Define default categories
    default_categories = [
        {"id": -1, "categoryName": "Unparsed"},
        {"id": 0, "categoryName": "General"},
        {"id": 1, "categoryName": "Bills"},
        {"id": 2, "categoryName": "Rent"},
        {"id": 3, "categoryName": "Transportation"},
        {"id": 4, "categoryName": "Groceries"},
        {"id": 5, "categoryName": "Leisure"},
        {"id": 6, "categoryName": "Health"},
        {"id": 7, "categoryName": "Debt Repayment"},
        {"id": 8, "categoryName": "Education"},
        {"id": 9, "categoryName": "Personal Care"},
        {"id": 10, "categoryName": "Home Maintenance"},
        {"id": 11, "categoryName": "Shopping"},
        {"id": 12, "categoryName": "Gas"},
        {"id": 13, "categoryName": "Entertainment & Media"},
        {"id": 14, "categoryName": "Dining"}
    ]

    # Fetch existing categories from the database by their names and turn them into a set
    existing_category_names = {category.categoryName for category in UserCategory.query.all()}
    changes_made = False

    for category in default_categories:
        if category["categoryName"] not in existing_category_names:
            new_category = Category(id=category["id"], categoryName=category["categoryName"], owner=None)
            db.session.add(new_category)
            changes_made = True

    # Commit changes to the database if new categories were added
    if changes_made:
        db.session.commit()
