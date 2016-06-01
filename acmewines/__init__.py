"""
    acmewines
    ~~~~~~~~~

    Acme Wines is a mock wine ordering application
    using the micro-framework Flask
"""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize the app
app = Flask(__name__)

# Configure the app
app.config.from_object('config')

# Initialize a SQLAlchemy object and integrate it to the app
db = SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

from acmewines.views import orders
app.register_blueprint(orders.mod)


