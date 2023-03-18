import unittest
from api import create_app
from api.config.config import config_dict
from api.utils import db
from api.models.users import Admin
from werkzeug.security import generate_password_hash
from flask_jwt_extended import create_access_token, verify_jwt_in_request


class UserTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()


    def tearDown(self):
        db.drop_all()

        self.appctx.pop()

        self.app = None

        self.client = None


    #For testing the user creation
    def test_user_signup(self):
        data = {
            "first_name": "John",
            "last_name": "Doe",
            "username": "johndoe",
            "email": "jd@gmail.com",	
            "password": "password"
        }

        response = self.client.post('/auth/signup', json=data)

        user = Admin.query.filter_by(email='jd@gmail.com').first()

        assert user.username == 'johndoe'

        assert response.status_code == 201


    #For testing the user login
    def test_user_login(self):
        data = {
            "username": "johndoe",
            "password": "password"
        }

        response = self.client.post('/auth/login', json=data)

        assert response.status_code == 200


    #For testing the user logout
    def test_user_logout(self):
        token = create_access_token(identity='johndoe')

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = self.client.post('/auth/logout', headers=headers)

        assert response.status_code == 200

        assert response.json['message'] == 'Successfully logged out'



