from flask import Blueprint

balance_bp = Blueprint('balance', __name__, url_prefix = '/balance',template_folder = 'templates')

from .views import *
