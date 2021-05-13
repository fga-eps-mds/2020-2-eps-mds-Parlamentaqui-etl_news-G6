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
        request = self.client.get(url_for('index'))
        self.assertEqual(200 , request.status_code)
        self.assertEqual('ETL News' , request.data.decode())

    def test_index(self):
        request = self.client.get(url_for('index'))
        self.assertEqual(200 , request.status_code)

    def test_api_index(self):
        request = self.client.get(url_for('api.index'))
        self.assertEqual(200 , request.status_code)

    def test_api_index(self):
        data_expected = 'Não foi encontrado nenhum deputado com id: 0001454'

        request = self.client.get(url_for('api.deputy/0001454',))
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
            'Codigo': '12345',
            'Cidade': 'Natal/RN',
            'Status': 'Saiu para entrega'
        }
        request = self.client.get(url_for('api.atualizar_noticias'))
        request_mock.get(url, json=data)
        self.assertEqual(self.correios.encomenda('PR12345BR'), data)


    def tearDown(self):
        self.context.pop()

if __name__=='__main__':
    unittest.main()