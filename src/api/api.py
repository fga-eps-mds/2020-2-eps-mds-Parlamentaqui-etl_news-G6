import os
import json
import requests
from flask import Blueprint, jsonify
from datetime import datetime
from models import *
from operator import attrgetter

NEWS_API_KEY = os.getenv('GOOGLE_NEWS_API_KEY')
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
    all_news = []
    cont = 0

    for news in News.objects:
        all_news.append(news.to_json(news))
        cont +=1

    print("\n", cont, "\n")

    return jsonify(all_news)

    # all_news = News.objects
    
    # #Ordenar a lista de acordo com a data.
    # sorted_list = sorted(all_news, key=attrgetter('update_date'), reverse = True)
    # news_list = []
    # news_list.append(sorted_list[0].to_json(sorted_list[0]))
    # news_list.append(sorted_list[1].to_json(sorted_list[1]))

    # return jsonify(news_list)

#Atualizar as noticias do banco de dado de acordo com a API Google News
@api.route('/limpar_noticias')
def limpar_noticias():
    News.objects.all().delete()
    return str(len(News.objects))


#Atualizar as noticias do banco de dado de acordo com a API Google News
@api.route('/atualizar_noticias')
def atualizar_noticias():
    #criar o resquest para pegar todas as noticiar relacionadas a deputado(a) e montar um json
    r = requests.get(f'https://newsapi.org/v2/everything?q=deputado OR deputada&language=pt&sortby=publishedAt&pageSize=100&apiKey={NEWS_API_KEY}')
    
    print("\n", r.json()['totalResults'],"\n")
    
    all_news_json = r.json()["articles"]

    return jsonify(all_news_json)

    #pegar qual foi o ultimo id no banco
    last_id = 0

    if len(News.objects) == 0:
        last_id = 0
    else:
        last_id = News.objects().order_by('id')[0].id

    #criar uma lista com todos os objetos para nao usar o QueryType
    all_news_list = []
    for item in News.objects:
        all_news_list.append(item)
    
    #para cada json na lista de todos os jsons, iterar para saber se é uma noticia de algum deputado em questão.
    for item in all_news_json:
        published_new_date = str(item["publishedAt"])
        published_new_date = published_new_date[0:10]
        news_date = datetime.strptime(published_new_date, "%Y-%m-%d") if len(str(item["publishedAt"])) > 4 else None

        #acessar cada deputado para bverificar se o nome dele está em algum item do json da noticia
        for deputy in Deputy.objects:
            if (deputy.name in item["content"]) or (deputy.name in item["description"]) or (deputy.name in item["title"]):
                
                #caso a noticia ja exista no banco de dados, apenas ignorá-la
                need_insertion = True
                for news_item in all_news_list:
                    if (news_item.deputy_id is deputy.id) and (news_item.title is item["title"]) and (news_item.update_date is news_date):
                        need_insertion = False 
                        break
                if not need_insertion:
                    continue

                #a noticia nao se encontra no banco de dados e o deputado foi verificado, portanto adicionar essa noticia
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

    #cria uma nova lista com todos os objetos criados de noticia para transformá-lo em uma lista de json
    news_list = []
    for item in News.objects:
        news_list.append(item.to_json(item))

    return jsonify(news_list)

@api.route('/<deputy_id>')
def encontra_noticias_deputado(deputy_id):
    deputy_news = []
    
    for item in News.objects:
        if int(item.deputy_id) == int(deputy_id):
            deputy_news.append(item.to_json(item))

    return jsonify(deputy_news)