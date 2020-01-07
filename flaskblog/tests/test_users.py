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
        db.create_all()
        self.assertEqual(app.debug, False)

    def tearDown(self):
        db.drop_all()

    def register(self, username, email, password, confirm_password):
        return self.app.post('/register',
                             data={'username': username,
                                   'email': email,
                                   'password': password,
                                   'confirm_password': confirm_password},
                             follow_redirects=True)

    def login(self, email, password):
        return self.app.post('/login',
                             data={'email': email, 'password': password},
                             follow_redirects=True)

    def test_users_register_form_displays(self):
        r = self.app.get('/register')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Join Today', r.data)
        self.assertIn(b'Username', r.data)
        self.assertIn(b'Email', r.data)
        self.assertIn(b'Password', r.data)
        self.assertIn(b'Confirm Password', r.data)

    def test_users_register_valid(self):
        self.app.get('/register', follow_redirects=True)
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Your account has been created.', r.data)

    def test_users_register_invalid_different_passwords(self):
        self.app.get('/register', follow_redirects=True)
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          '321drowssaPyM')
        self.assertIn(b'Field must be equal to password.', r.data)

    def test_users_register_invalid_duplicate_username(self):
        self.app.get('/register', follow_redirects=True)
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        r = self.register('John Smith', 'js@ophd.me', 'APassword123',
                          'APassword123')
        self.assertIn(b'That username already exists.', r.data)

    def test_users_register_invalid_duplicate_email(self):
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        r = self.register('James Brown', 'js@ophd.me', 'APassword123',
                          'APassword123')
        self.assertIn(b'That email is already being used.', r.data)

    def test_users_login_form_displays(self):
        r = self.app.get('/login')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Log In', r.data)
        self.assertIn(b'Email', r.data)
        self.assertIn(b'Password', r.data)
        self.assertIn(b'Remember Me', r.data)
        self.assertIn(b'Forgot password?', r.data)
        self.assertIn(b'Need an account?', r.data)
        self.assertIn(b'Sign Up', r.data)

    def test_users_login(self):
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        r = self.login('js@ophd.me', 'MyPassword123')
        self.assertEqual(r.status_code, 200)

    def test_users_login_invalid_email(self):
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        r = self.login('pj@ophd.me', 'MyPassword123')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Login unsuccessful. Please check email and password.',
                        r.data)

    def test_users_login_invalid_password(self):
        self.app.get('/register', follow_redirects=True)
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        r = self.login('js@ophd.me', '321drowssaPyM')
        self.assertIn(b'Login unsuccessful. Please check email and password.',
                        r.data)

    def test_users_logout(self):
        self.app.get('/register', follow_redirects=True)
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        r = self.login('daigleo@gmail.com', 'MyPassword123')
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(r.status_code, 200)
    
    def test_users_logout_not_logged_in(self):
        r = self.app.get('/logout', follow_redirects=True)
        self.assertEqual(r.status_code, 200)

    def test_users_account_form_displays(self):
        username = 'Tracy Borman'
        email = 'tb@ophd.me'
        password = 'test_password'
        self.app.get('/register', follow_redirects=True)
        r = self.register(username, email, password, password)
        self.assertEqual(r.status_code, 200)
        r = self.login(email, password)
        self.assertEqual(r.status_code, 200)

        r = self.app.get('/account')
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'<h2 class="account-heading">Tracy Borman</h2>', r.data)
        self.assertIn(b'<p class="text-secondary">tb@ophd.me</p>', r.data)
        self.assertIn(b'Account Information', r.data)
        self.assertIn(b'value="Tracy Borman"', r.data)
        self.assertIn(b'value="tb@ophd.me"', r.data)
    
    def test_users_account_no_login(self):
        r = self.app.get('/account', follow_redirects=True)
        self.assertIn(b'Please log in to access this page.', r.data)
        self.assertIn(b'Log In', r.data)
    
    def test_users_account_change_email(self):
        username = 'Tracy Borman'
        email = 'tb@ophd.me'
        password = 'test_password'
        r = self.register(username, email, password, password)
        self.assertEqual(r.status_code, 200)
        r = self.login(email, password)
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/account')
        self.assertEqual(r.status_code, 200)

        r = self.app.post('/account',
                     data={'username':'Tracy Borman', 'email': 'js@ophd.me'},
                     follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Your account has been updated.', r.data)
        self.assertIn(b'<p class="text-secondary">js@ophd.me</p>', r.data)
    
    def test_users_account_change_email_already_used(self):
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        username = 'Tracy Borman'
        email = 'tb@ophd.me'
        password = 'test_password'
        r = self.register(username, email, password, password)
        self.assertEqual(r.status_code, 200)
        r = self.login(email, password)
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/account')
        self.assertEqual(r.status_code, 200)

        r = self.app.post('/account', 
                    data={'username':'Tracy Borman', 'email': 'js@ophd.me'},
                    follow_redirects=True)
        self.assertIn(b'That email is already being used.', r.data)
    
    def test_users_account_change_username(self):
        username = 'Tracy Borman'
        email = 'tb@ophd.me'
        password = 'test_password'
        self.app.get('/register', follow_redirects=True)
        r = self.register(username, email, password, password)
        self.assertEqual(r.status_code, 200)
        r = self.login(email, password)
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/account')
        self.assertEqual(r.status_code, 200)

        r = self.app.post('/account',
                    data={'username': 'Tracy Smith', 'email':'tb@ophd.me'},
                    follow_redirects=True)
        self.assertEqual(r.status_code, 200)
        self.assertIn(b'Your account has been updated.', r.data)
        self.assertIn(b'<h2 class="account-heading">Tracy Smith</h2>', r.data)
    
    def test_users_account_change_username_already_used(self):
        r = self.register('John Smith', 'js@ophd.me', 'MyPassword123',
                          'MyPassword123')
        self.assertEqual(r.status_code, 200)
        username = 'Tracy Borman'
        email = 'tb@ophd.me'
        password = 'test_password'
        r = self.register(username, email, password, password)
        self.assertEqual(r.status_code, 200)
        r = self.login(email, password)
        self.assertEqual(r.status_code, 200)
        r = self.app.get('/account')
        self.assertEqual(r.status_code, 200)

        r = self.app.post('/account',
                    data={'username': 'John Smith', 'email':'tb@ophd.me'},
                    follow_redirects=True)
        self.assertIn(b'That username already exists.', r.data)
    
