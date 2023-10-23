from flask import Flask
from .controllers.users_controller import users_bp 
from .controllers.transactions_controller import transactions_bp 

def register_api_routes(app:Flask):
    app.register_blueprint(users_bp, url_prefix="/api/users") 
    app.register_blueprint(transactions_bp, url_prefix="/api/transactions") 

    return app