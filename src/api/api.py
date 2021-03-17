import json
from flask import Blueprint
from models import *
from operator import attrgetter

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/deputies')
def index():
    deputies = ''
    for deputy in Deputy.objects:
        deputies = deputies + ' ' + deputy.name

    return deputies

@api.route('/news')
def news():
    #Pegar as duas noticias mais recentes do nosso banco de dados
    all_news = News.objects
    
    #Ordenar a lista de acordo com a data.
    sorted_list = sorted(all_news, key=attrgetter('update_date'))

    #criar o json dessas noticias
    # news_1_json = magic(sorted_list[0])
    # news_2_json = magic(sorted_list[1])
    
    return sorted_list[0].abstract