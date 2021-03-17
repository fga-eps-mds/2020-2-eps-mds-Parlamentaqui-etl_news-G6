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
    news_1_json = get_json_by_news_class(sorted_list[0])
    news_2_json = get_json_by_news_class(sorted_list[1])
    
    #lista com os dois json
    full_json = [news_1_json, news_2_json]
    #cria um json com a lista de jsons
    return json.dumps(full_json)

#Classe necessária pra transformar em json
#Link do tutorial: https://stackoverflow.com/questions/3768895/how-to-make-a-class-json-serializable
class JsonClass():
    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

#Retorna uma classe de News em um json
def get_json_by_news_class(news_class):
    #cria uma classe temporária dessa nova classe
    temp_class = JsonClass()

    #adiciona os atributos a serem serializados com o mesmo nome dos atributos da classe passada
    temp_class.id = news_class.id
    temp_class.deputy_id = news_class.deputy_id
    temp_class.link = news_class.link
    temp_class.photo = news_class.photo
    temp_class.title = news_class.title
    temp_class.abstract = news_class.abstract
    temp_class.deputy_name = news_class.deputy_name
    temp_class.update_date = f"{news_class.update_date}"
    temp_class.source = news_class.source

    #transforma essa temp_class para um json.
    return temp_class.toJSON()
