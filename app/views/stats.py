from flask import render_template

from fatmodels import FatLocation, FatOrder, FatOrderItem, FatUser, FatProduct
from app import app


@app.route('/stats/')
def stats():
    data = {
        'amount': {
            'orders': FatOrder.amount(),
            'locations': FatLocation.amount(),
            'users': FatUser.amount(),
            'orderitems': FatOrderItem.amount(),
            'products': FatProduct.amount(),
        }
    }
    return render_template('stats.html', data=data)
