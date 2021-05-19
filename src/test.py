
import unittest

from pymongo.common import partition_node
from app import app
from mongoengine import connect, disconnect
from flask import Flask
# import requests_mock
import os


DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
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

    # connect('prlmntq_db_test', host=f'mongodb://prlmntq_adm:prlmntq_pwd@prlmntq_db:27018/prlmntq_db?authSource=admin')
    # disconnect(alias='prlmntq_db')

    @classmethod
    def setUpClass(cls):
       disconnect()
       connect('prlmntq_db_test', host='mongomock://localhost')

    @classmethod
    def tearDownClass(cls):
       disconnect()

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_deputies(self):
        request = self.client.get('/api/deputies')
        self.assertEqual(200 , request.status_code)
        # self.assertGreaterEqual(len(request.data.decode()),10)

    def test_api_deputy_status(self):
        request = self.client.get('/api/deputy/3')
        self.assertEqual(200 , request.status_code)

    def test_api_deputy(self):
        data_expected = '{}\n'

        request = self.client.get('api/deputy/3')
        self.assertEqual(data_expected , request.data.decode())

    def test_news_status(self):
        request = self.client.get('/api/news')
        self.assertEqual(200 , request.status_code)

    def test_clean_news_status(self):
        request = self.client.get('/api/limpar_noticias')
        self.assertEqual(200 , request.status_code)
        self.assertEqual('0' , request.data.decode())

    def test_all_news_status(self):
        request = self.client.get('/api/all_news')
        self.assertEqual(200 , request.status_code)

    def test_get_news_by_id_status(self):
        request = self.client.get('/api/get_news_by_id/3')
        self.assertEqual(200 , request.status_code)

    def tearDown(self):
        self.context.pop()


if __name__=='__main__':
    unittest.main()