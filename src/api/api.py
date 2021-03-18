import json
from flask import Blueprint
from models import *
from operator import attrgetter

api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/deputies')
def index():
    full_json = {}
    cont = 0
    for deputy in Deputy.objects:
        temp_json = deputy.to_json(deputy)
        full_json[cont] = temp_json
        cont += 1

    return full_json

@api.route('/news')
def news():
    #Pegar as duas noticias mais recentes do nosso banco de dados
    all_news = News.objects
    
    #Ordenar a lista de acordo com a data.
    sorted_list = sorted(all_news, key=attrgetter('update_date'))
    news_1 = sorted_list[0].to_json(sorted_list[0])
    news_2 = sorted_list[1].to_json(sorted_list[1])
    json_full = {
        'news_01':news_1,
        'news_02':news_2
    }

    return json_full
