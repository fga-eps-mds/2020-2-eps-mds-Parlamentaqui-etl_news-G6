import json
from flask import Blueprint, jsonify
from models import *
from operator import attrgetter

api = Blueprint('api', __name__, url_prefix='/api')

#Retornar um json com todos os jsons de deputados
@api.route('/deputies')
def index():
    full_json = {}
    cont = 0
    for deputy in Deputy.objects:
        temp_json = deputy.to_json(deputy)
        full_json[cont] = temp_json
        cont += 1

    return full_json

#Pegar as duas noticias mais recentes do nosso banco de dados
@api.route('/news')
def news():
    all_news = News.objects
    
    #Ordenar a lista de acordo com a data.
    sorted_list = sorted(all_news, key=attrgetter('update_date'))
    news_list = []
    news_list.append(sorted_list[0].to_json(sorted_list[0]))
    news_list.append(sorted_list[1].to_json(sorted_list[1]))

    return jsonify(news_list)
