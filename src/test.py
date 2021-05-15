
import unittest
from app import app
from mongoengine import connect
from flask import Flask
import requests_mock
import os


DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST_TEST')
DB_PORT = os.getenv('DB_PORT_TEST')
DB_NAME = os.getenv('DB_NAME_TEST')

NEWS_API_KEY = os.getenv('GOOGLE_NEWS_API_KEY')

class AppTests(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_index_status(self):
        request = self.client.get('/')
        self.assertEqual(200 , request.status_code)

    def test_index(self):
        request = self.client.get('/')
        self.assertEqual('ETL News' , request.data.decode())
        self.assertGreaterEqual(len(request.data.decode()),2)

    def test_fake_status(self):
        request = self.client.get('/not_exist')
        self.assertEqual(404 , request.status_code)

    def tearDown(self):
        self.context.pop()

class EtlApiTests(unittest.TestCase):

    connect(DB_NAME, host=f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin')
    
    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_deputies(self):
        request = self.client.get('/api/deputies')
        self.assertEqual(200 , request.status_code)
        self.assertGreaterEqual(len(request.data.decode()),10)

    def test_api_deputy_fail(self):
        data_expected = 'Não foi encontrado nenhum deputado com id: 0001454'

        request = self.client.get('/api/deputy/0001454')
        self.assertEqual(data_expected , request.data.decode())

    def test_api_deputy(self):
        data_expected = {
            "birth_date": "Sun, 07 Jun 2020 14:57:11 GMT",
            "death_date": "Mon, 13 Apr 2020 15:30:24 GMT",
            "email": "cibele@parlamentaqui.com",
            "facebook_username": "facecicidoifood",
            "federative_unity": "DF",
            "final_legislature_id": 1,
            "final_legislature_year": 2021,
            "full_name": "Cibele Goudinho",
            "id": 3,
            "initial_legislature_id": 1,
            "initial_legislature_year": 2021,
            "instagram_username": "instacicidoifood",
            "last_activity_date": "Mon, 25 May 2020 17:00:32 GMT",
            "name": "Cici do Ifood",
            "party": "IFOOD",
            "photo_url": "https://avatars.githubusercontent.com/u/58526599?v=4",
            "sex": "F",
            "twitter_username": "twittercicidoifood"
        }

        request = self.client.get('api/deputy/3')
        self.assertEqual(data_expected , request.data.decode())

    def test_news_status(self):
        request = self.client.get('/api/news')
        self.assertEqual(200 , request.status_code)

    def test_clean_news_status(self):
        request = self.client.get('/api/limpar_noticias')
        self.assertEqual(200 , request.status_code)
        self.assertEqual(0 , request.data.decode())

    def test_all_news_status(self):
        request = self.client.get('/api/all_news')
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
                        "id": None,
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
        request = self.client.get('/api/atualizar_noticias')
        self.assertEqual(200 , request.status_code)
    
    def tearDown(self):
        self.context.pop()

if __name__=='__main__':
    unittest.main()