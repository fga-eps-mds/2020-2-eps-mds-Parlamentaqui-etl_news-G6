import unittest
# from unittest import TestCase#, mock
from flask import url_for
from app import app
import requests_mock
import os

NEWS_API_KEY = os.getenv('GOOGLE_NEWS_API_KEY')

class EtlTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_index(self):
        request = self.client.get(url_for('/'))
        self.assertEqual('ETL News' , request.data.decode())

    def test_index_status(self):
        request = self.client.get(url_for('/'))
        self.assertEqual(200 , request.status_code)

    def test_api_index(self):
        request = self.client.get(url_for('api./'))
        self.assertEqual(200 , request.status_code)

    def test_api_index(self):
        data_expected = 'Não foi encontrado nenhum deputado com id: 0001454'

        request = self.client.get(url_for('api.deputy/0001454'))
        self.assertEqual(data_expected , request.data.decode())

    def test_news_status(self):
        request = self.client.get(url_for('api.news'))
        self.assertEqual(200 , request.status_code)

    def test_clean_news_status(self):
        request = self.client.get(url_for('api.limpar_noticias'))
        self.assertEqual(200 , request.status_code)
    
    @requests_mock.Mocker()
    def test_update_news(self, request_mock):
        url = (f'https://newsapi.org/v2/everything?q=deputado OR deputada&language=pt&sortby=publishedAt&pageSize=100&apiKey={NEWS_API_KEY}')
        data = {
            "status": "ok",
            "totalResults": 4321,
            "articles": [
                {
                    "source": {
                        "id": null,
                        "name": "Terra.com.br"
                    },
                    "author": "Estadão Conteúdo",
                    "title": "Câmara aprova projeto que flexibiliza regras de licenciamento ambiental",
                    "description": "Frente Parlamentar Ambientalista e especialistas repudiam texto; ligado à ala da agropecuária do Legislativo, relator fala em texto 'equilibrado' e sem sem ...",
                    "url": "https://www.terra.com.br/noticias/ciencia/sustentabilidade/camara-aprova-projeto-que-flexibiliza-regras-de-licenciamento-ambiental,730883c65b2677337ef158208c1238bf8foz0mmo.html",
                    "urlToImage": "https://p2.trrsf.com/image/fget/cf/1200/628/middle/s1.trrsf.com/atm/3/core/_img/terra-logo-white-bg-v3.jpg",
                    "publishedAt": "2021-05-13T03:39:16Z",
                    "content": "BRASÍLIA - O projeto da nova Lei Geral do Licenciamento Ambiental foi aprovado na madrugada desta quinta-feira, 13, pelo plenário da Câmara dos Deputados. Com maioria na Casa, a bancada ruralista apr… [+8675 chars]"
                }
            ]
        }
        request_mock.get(url, json=data)
        request = self.client.get(url_for('api.atualizar_noticias'))
        self.assertEqual(200 , request.status_code)

    def tearDown(self):
        self.context.pop()

if __name__=='__main__':
    unittest.main()