form flask import Blueprint, jsonify

mod = Blueprint('orders', __name__, url_prefix='/orders')

@mod.route('/')
def index():


@mod.route('/import')
def import_orders():


@mod.route('/<int:id>')
def show_order():

