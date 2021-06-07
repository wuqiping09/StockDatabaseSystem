from flask import Blueprint

transaction_bp = Blueprint('transaction', __name__, url_prefix = '/transaction',template_folder = 'templates')

from .views import *
