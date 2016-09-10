from flask import render_template

from fatmodels import FatLocation, FatOrder, FatOrderItem, FatUser
from app import app


@app.route('/stats/')
def stats():
    data = {
        'order_amount': FatOrder.amount(),
        'location_amount': FatLocation.amount(),
        'user_amount': FatUser.amount(),
        'orderitem_amount': FatOrderItem.amount()
    }
    return render_template('stats.html', data=data)
