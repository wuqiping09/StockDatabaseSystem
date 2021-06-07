from flask import Blueprint

stock_bp = Blueprint('stock', __name__, url_prefix = '/stock', template_folder='templates')

from .views import *
