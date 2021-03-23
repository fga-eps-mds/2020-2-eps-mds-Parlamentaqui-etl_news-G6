import json
import requests
from flask import Blueprint, jsonify
from datetime import datetime
from models import *
from operator import attrgetter

GOOGLE_NEWS_API_KEY = "7f0f4e99393a442fb01c8193efdb7aad"
api = Blueprint('api', __name__, url_prefix='/api')

#Retornar um json com todos os jsons de deputados
@api.route('/deputies')
def index():
    full_json = []
    for deputy in Deputy.objects:
        full_json.append(deputy.to_json(deputy))

    return jsonify(full_json)

#Pegar as duas noticias mais recentes do nosso banco de dados
@api.route('/news')
def news():
    all_news = News.objects
    
    #Ordenar a lista de acordo com a data.
    sorted_list = sorted(all_news, key=attrgetter('update_date'), reverse = True)
    news_list = []
    news_list.append(sorted_list[0].to_json(sorted_list[0]))
    news_list.append(sorted_list[1].to_json(sorted_list[1]))

    return jsonify(news_list)


#Atualizar as noticias do banco de dado de acordo com a API Google News
@api.route('/atualizar_noticias')
def atualizar_noticias():
    r = requests.get(f'https://newsapi.org/v2/everything?q=deputado OR deputada&language=pt&sortby=publishedAt&pageSize=100&apiKey={GOOGLE_NEWS_API_KEY}')
    all_news_json = r.json()["articles"]
    last_id = News.objects().order_by('id')[0].id
    
    for item in all_news_json:
        published_new_date = str(item["publishedAt"])
        published_new_date = published_new_date[0:10]
        news_date = datetime.strptime(published_new_date, "%Y-%m-%d") if len(str(item["publishedAt"])) > 4 else None

        for deputy in Deputy.objects:
            if (deputy.name in item["content"]) or (deputy.name in item["description"]) or (deputy.name in item["title"]):
                last_id = last_id + 1
                populate_news_1 = News(
                id=last_id,
                deputy_id=deputy.id,
                link=item["url"] if item["url"] is not None else None,
                photo=item["urlToImage"] if item["urlToImage"] is not None else None,
                title=item["title"] if item["title"] is not None else None,
                abstract=item["description"] if item["description"] is not None else None,
                deputy_name=deputy.name,
                update_date=news_date,
                source=item["source"]["name"]
                ).save()

    news_list = []
    for item in News.objects:
        news_list.append(item.to_json(item))

    return jsonify(news_list)
