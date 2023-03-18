from flask import Flask
from flask_restx import Api
from .auth.views import auth_namespace
from .courses.views import course_namespace
from .users.views import user_namespace
from .config.config import config_dict
from .utils import db
from .models.users import Student, Admin
from .models.courses import Course
from flask_migrate import Migrate
from blocklist import BLOCKLIST
from flask_jwt_extended import JWTManager
from werkzeug.exceptions import NotFound, MethodNotAllowed, BadRequest, Unauthorized, Forbidden


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)

    db.init_app(app)

    jwt = JWTManager(app)

    @jwt.token_in_blocklist_loader
    def check_if_token_in_blocklist(jwt_header, jwt_payload):
        return jwt_payload['jti'] in BLOCKLIST

    migrate = Migrate(app, db, render_as_batch=True)

    authorizations = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter your JWT token in the header in the following way: ** Bearer &lt;JWT&gt; token to authorize **"
        }
    }

    api = Api(app, version='1.0',
    title='Student Management System API',
    description='A simple Student Management System REST API',
    authorizations=authorizations,
    security='Bearer Auth')

    api.add_namespace(auth_namespace)
    api.add_namespace(course_namespace)
    api.add_namespace(user_namespace)

    @app.errorhandler(NotFound)
    def handle_not_found(error):
        return {'error': 'Not found'}, 404

    @app.errorhandler(MethodNotAllowed)
    def handle_method_not_allowed(error):
        return {'error': 'Method not allowed'}, 405

    @app.errorhandler(BadRequest)
    def handle_bad_request(error):
        return {'error': 'Bad request'}, 400

    @app.errorhandler(Unauthorized)
    def handle_unauthorized(error):
        return {'error': 'Unauthorized'}, 401

    @app.errorhandler(Forbidden)
    def handle_forbidden(error):
        return {'error': 'Forbidden'}, 403

    @app.shell_context_processor
    def make_shell_context():
        return {'db': db,
                'Student': Student,
                'Course': Course,
                'Admin': Admin
                }
    
    return app