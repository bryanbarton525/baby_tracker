from flask_wtf import FlaskForm
from wtforms import SubmitField, RadioField, StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, EqualTo, DataRequired
from wtforms_components import TimeField


class LogFeeding(FlaskForm):
    events = [('start_feed', 'Start Feeding'), ('end_feed', 'End Feeding'), ('bottle', 'Bottle'),
              ('poop_time', 'Poop'), ('pee_time', 'Pee'), ('both', 'Pee and Poop')]
    time = TimeField('Time:')
    type = RadioField('Event Type', choices=events)
    note = StringField('Notes:', description='Amount bottle fed, color of poop, etc.')
    submit = SubmitField()


class Login(FlaskForm):
    submit = SubmitField()


class RegisterUser(FlaskForm):
    username = StringField('Username:', validators=[InputRequired(message='Please Enter A Username.')])
    password = PasswordField('New Password', validators=[InputRequired(message='Please Enter a Password'),
                                                         EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Repeat Password', validators=[InputRequired(message='Please Confirm Your Password.')])
    accept_tos = BooleanField('I accept the TOS', [DataRequired()])

