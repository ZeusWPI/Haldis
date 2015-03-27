from datetime import datetime, timedelta
from flask_wtf import Form
from wtforms import SelectField, DateTimeField, validators, SubmitField
from models import User, Location

__author__ = 'feliciaan'


class OrderForm(Form):
    courrier_id = SelectField('Courrier', coerce=int)
    location_id = SelectField('Location', coerce=int, validators=[validators.optional()])
    starttime = DateTimeField('Starttime', default=datetime.now)
    stoptime = DateTimeField('Stoptime')
    submit_button = SubmitField('Submit Form')

    def populate(self):
        self.courrier_id.choices = [(0, None)] + \
                                   [(u.id, u.username) for u in User.query.order_by('username')]
        self.location_id.choices = [(l.id, l.name)
                                    for l in Location.query.order_by('name')]
        if self.stoptime.data is None:
            self.stoptime.data = datetime.now() + timedelta(hours=1)


