import os
import binascii


class Secret(object):

    SECRET_KEY = os.environ.get('SECRET_KEY') or binascii.hexlify(os.urandom(24))
