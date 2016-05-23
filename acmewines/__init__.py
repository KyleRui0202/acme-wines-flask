from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('config')

db = SQLAlchemy(app)

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

from acmewines.views import orders
app.register_blueprint(orders.mod)


