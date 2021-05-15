
import unittest

from mongoengine.connection import disconnect
from app import app
from flask import url_for
from mongoengine import connect
from flask import Flask

# from unittest import TestCase#, mock
# from api.api import api
# import requests_mock
import os

# NEWS_API_KEY = os.getenv('GOOGLE_NEWS_API_KEY')
DB_USERNAME = os.getenv('DB_USERNAME')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')
DB_NAME = os.getenv('DB_NAME')


class EtlTests(unittest.TestCase):

    def setUp(self):
        connect(DB_NAME, host=f'mongodb://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?authSource=admin')
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()
        print ('Setup OK\n\n')

    def test_index_status(self):
        request = self.client.get('/')
        self.assertEqual(200 , request.status_code)

    def test_index(self):
        request = self.client.get('/')
        print(request.data.decode())
        print(request.status_code)
        self.assertEqual(200 , request.status_code)

    def test_fake_status(self):
        request = self.client.get('/not_exist')
        self.assertEqual(404 , request.status_code)

    # def test_deputies(self):
    #     request = self.client.get('/api/all_news')
    #     print(request.data.decode())
    #     print(request.status_code)
    #     self.assertEqual(200 , request.status_code)

    def tearDown(self):
        self.context.pop()

if __name__=='__main__':
    unittest.main()