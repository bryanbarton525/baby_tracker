from flask import Flask
from web_gui.secret import Secret
from waitress import serve
from datetime import datetime

site = Flask(__name__)
site.config.from_object(Secret)


# function to convert military time format to standard AM PM time.
def format_datetime(value):
    if value is not None:
        value = str(value)
        time_format = '%I:%M:%S %p'
        convert_time = datetime.strptime(value, '%H:%M:%S')
        converted_value = datetime.strftime(convert_time, time_format)
        return converted_value
    else:
        return value


# Add function to jinja filters
site.jinja_env.filters['datetime'] = format_datetime

from web_gui import routes

serve(site, listen='0.0.0.0:8080')
