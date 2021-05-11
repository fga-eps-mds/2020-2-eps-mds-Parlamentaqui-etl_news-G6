from unittest import TestCase#, mock
from flask import url_for
from app import app

class EtlTests(TestCase):

    def setUp(self):
        self.app = app
        self.app.testing = True
        self.context = self.app.test_request_context()
        self.context.push()
        self.client = self.app.test_client()

    def test_index(self):
        request = self.client.get(url_for('index'))
        self.assertEqual('ETL News' , request.data.decode())

    def test_index(self):
        request = self.client.get(url_for('index'))
        
        self.assertEqual(200 , request.status_code)

    def tearDown(self):
        self.context.pop()