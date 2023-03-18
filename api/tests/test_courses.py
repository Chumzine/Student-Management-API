import unittest
from api import create_app
from api.config.config import config_dict
from api.utils import db
from api.models.courses import Course
from flask_jwt_extended import create_access_token


class CourseTestCase(unittest.TestCase):
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


    #Setting up the test admin
    test_admin_setup = {
        "first_name": "John",
        "last_name": "Doe",
        "username": "johndoe",
        "email": "jd@gmail.com",	
        "password": "password"
    }



    #For testing the course creation
    def test_course_creation(self):
        course_data = {
            "name": "Python",
            "description": "Python is a programming language that lets you work more quickly and integrate your systems more effectively.",
            "course_code": "PYT001",
            "teacher": "John Doe"
        }

        token = create_access_token(identity='johndoe')

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = self.client.post('/course/create', json=course_data, headers=headers)

        course = Course.query.filter_by(name='Python').first()

        assert course.name == 'Python'

        assert response.status_code == 201

        course = Course.query.all()

        assert len(course) == 1


    #For testing the get course by id
    def test_course_get(self):
        course = Course(
            name='Python', 
            description='Python is a programming language that lets you work more quickly and integrate your systems more effectively.', 
            course_code="PYT-001",
            course_units="GOOD",
            teacher="John Doe"
        )

        course.save()

        token = create_access_token(identity='johndoe')

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = self.client.get('/course/course/1', headers=headers)

        assert response.status_code == 200



    #For testing the get all courses
    def test_get_all_courses(self):
        token = create_access_token(identity='johndoe')

        headers = {
            'Authorization': f'Bearer {token}'
        }

        response = self.client.get('/course/course', headers=headers)

        assert response.status_code == 200

        assert response.json == []



