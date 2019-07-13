from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField
from wtforms_components import TimeField


class LogFeeding(FlaskForm):
    events = [('start_feed', 'Start Feeding'), ('end_feed', 'End Feeding'), ('bottle', 'Bottle'),
              ('poop_time', 'Poop'), ('pee_time', 'Pee')]
    time = TimeField('Time:')
    type = RadioField('Event Type', choices=events)
    note = StringField('Notes:', description='Amount bottle fed, color of poop, etc.')
    submit = SubmitField()
