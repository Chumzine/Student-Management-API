from flask import request
from ..utils.decorator import admin_required
from flask_restx import Namespace, Resource, fields
from ..models.users import Student, Admin
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
from blocklist import BLOCKLIST
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt


auth_namespace = Namespace('auth', description='Namespace for Authentication')

signup_model = auth_namespace.model(
    'Signup', {
        'username': fields.String(required=True, description='Username'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='Email address'),
        'password': fields.String(required=True, description='Password'),
        'admin': fields.Boolean(required=True, description='Admin')
    }
)

student_model = auth_namespace.model(
    'Student', {
        'username': fields.String(required=True, description='Username'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='Email address'),
        'password_hash': fields.String(required=True, description='Password'),
        'admin': fields.Boolean(required=True, description='Admin'),
        'is_active': fields.Boolean(required=True, description='Active')
    }
)

admin_model = auth_namespace.model(
    'Admin', {
        'username': fields.String(required=True, description='Username'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='Email address'),
        'password_hash': fields.String(required=True, description='Password'),
        'admin': fields.Boolean(required=True, description='Admin'),
        'is_active': fields.Boolean(required=True, description='Shows that a user is active')
    }
)

login_model = auth_namespace.model(
    'Login', {
        'username': fields.String(required=True, description='Username'),
        'password': fields.String(required=True, description='Password')
    }
)

@auth_namespace.route('/signup')
class SignUp(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(admin_model)
    @auth_namespace.doc(description='Register a user')
    def post(self):
        """
        Register a user
        """
        data = request.get_json()


        # Check if user already exists
        admin = Admin.query.filter_by(email=data.get('email')).first()

        if admin:
            return {'message': 'Admin already exists'}, HTTPStatus.BAD_REQUEST


        # Create a new user
        user = Admin(
            username = data.get('username'),
            first_name = data.get('first_name'),
            last_name = data.get('last_name'),
            email = data.get('email'),
            password_hash = generate_password_hash(data.get('password'))
            )
        
        user.save()

        return user, HTTPStatus.CREATED


@auth_namespace.route('/login')
class Login(Resource):
    @auth_namespace.expect(login_model)
    @auth_namespace.doc(description='Login a user by generating a JWT token')
    def post(self):
        """
        Login a user by generating a JWT token
        """
        data = request.get_json()

        username = data.get('username')
        password = data.get('password')

        user = Student.query.filter_by(username=username).first()
        if not user:
            user = Admin.query.filter_by(username=username).first()

        if (user is not None) and check_password_hash(user.password_hash, password):
            access_token = create_access_token(identity=user.username)
            refresh_token = create_refresh_token(identity=user.username)

            response = {
                'access_token': access_token,
                'refresh_token': refresh_token
            }

            return response, HTTPStatus.CREATED


@auth_namespace.route('/refresh')
class Refresh(Resource):
    @auth_namespace.doc(description='Refresh a user\'s JWT token')
    @jwt_required(refresh=True)
    def post(self):
        """
        Refresh a user's JWT token
        """
        current_user = get_jwt_identity()

        access_token = create_access_token(identity=current_user)

        return {'access_token': access_token}, HTTPStatus.OK        
    

@auth_namespace.route('/logout')
class Logout(Resource):
    @auth_namespace.doc(description='Logout a user by invalidating a JWT token')
    @jwt_required()
    def post(self):
        """
        Logout a user by invalidating a JWT token
        """
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)

        return {'message': 'Successfully logged out'}, HTTPStatus.OK