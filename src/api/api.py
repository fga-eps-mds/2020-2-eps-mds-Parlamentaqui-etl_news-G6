from flask import Blueprint
from models import *

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/deputies')
def index():
    deputies = ''
    for deputy in Deputy.objects:
        deputies = deputies + ' ' + deputy.name

    return deputies
