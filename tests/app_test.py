import unittest
from mockupdb import go, MockupDB
from app import app
from flask_pymongo import PyMongo


class AppTestCase(unittest.TestCase):

    def setUp(self):

        self.server = MockupDB()
        self.server.run()

        app.testing = True
        # todo - this doesnt mock mongo!
        # https://blog.zhaw.ch/icclab/testing-pymongo-applications-with-mockupdb/
        app.config['MONGO_URI'] = self.server.uri
        self.app = app.test_client()

    def tearDown(self):
        self.server.stop()
        pass

    def test_helloWorld(self):
        response = self.app.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, b'Hello, World!')

    def test_ping(self):
        response = self.app.get('/ping')

        self.assertEqual(response.data, b'pong')

    def test_file(self):
        response = self.app.get('/file')

        self.assertIn(b'Simple python web app built with flask', response.data)

    def test_crime(self):
        response = self.app.get('/raleigh/crime')

        self.assertEqual(response.status_code, 200)

    def test_crimeWithQuery(self):
        response = self.app.get('/raleigh/crime?query=Drug')

        self.assertEqual(response.status_code, 200)

    def test_allData(self):
        response = self.app.get('/allData')

        self.assertEqual(response.status_code, 200)

    def test_getDataSource(self):
        response = self.app.get('/dataSource/5a8e411973bc771f44485ac1')

        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()
