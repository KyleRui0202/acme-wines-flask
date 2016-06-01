from flask import Blueprint, request, jsonify

from acmewines.models import Order
from acmewines.tasks import OrderFilterTask

mod = Blueprint('orders', __name__, url_prefix='/orders')

@mod.route('/')
def index():
    url_params = request.args
    order_filter_task = OrderFilterTask(url_params)
    effect_filters = order_filter_task.effect_filter_params
    filtered_orders = [order.toDict() for order in order_filter_task.run()]
    return jsonify(effect_filters = order_filter_task.effect_filter_params, 
        num_of_orders = len(filtered_orders),
        results = filtered_orders)

@mod.route('/import')
def import_orders():
    pass

@mod.route('/<int:id>')
def show_order(id):
    retrieved_order = Order.query.get(id)
    if retrieved_order:
        return jsonify(retrieved_order.toDict())
    else:
        return jsonify({'not_found': 'The order of id=' + str(id) +\
            ' does not exist'})
