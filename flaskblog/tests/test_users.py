import os
import unittest
from flaskblog.tests.config import TestConfig
from flaskblog import create_app, db, bcrypt, mail
from flaskblog.models import User

app = create_app(TestConfig)
app.app_context().push()


class TestUsers(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()

        db.drop_all()
        db.create_all()

        self.assertEqual(app.debug, False)

    def tearDown(self):
        pass

    def register(self, username, email, password):
        return self.app.post('/register',
                             data={username: username,
                                   email: email, password: password},
                             follow_redirects=True)

    def login(self):
        pass

    def logout(self):
        pass

    def test_user_registration(self):
        self.app.get('/register', follow_redirects=True)
        r = self.register('John Smith', 'daigleo@gmail.com', 'MyPassword123')
        print('\n\nresponse data:')
        print(r.data)
        print('\n\n')
        self.assertIn(b'Your account has been created.', r.data, msg=r.data)


if __name__ == '__main__':
    # unittest.main()
    print(app.debug)
