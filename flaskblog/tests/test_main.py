import os
import unittest
from flaskblog.tests.config import TestConfig
from flaskblog import create_app, db, bcrypt, mail
from flaskblog.models import User

app = create_app(TestConfig)
app.app_context().push()


class TestMain(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        db.drop_all()

    def test_main_home(self):
        r = self.app.get('/home')
        self.assertEqual(r.status_code, 200)

        r = self.app.get('/')
        self.assertEqual(r.status_code, 200)

    def test_main_about(self):
        r = self.app.get('/about')
        self.assertEqual(r.status_code, 200)
        self.assertIn('About', r.data)


