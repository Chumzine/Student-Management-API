from flask_restx import Namespace, Resource, fields
from functools import wraps
from ..utils.decorator import admin_required, user_type
from ..models.users import Student, Admin
from ..models.courses import Course
from ..utils import db
from http import HTTPStatus
from werkzeug.security import generate_password_hash
from flask_jwt_extended import jwt_required, get_jwt, verify_jwt_in_request

user_namespace = Namespace('user', description='Namespace for Users')

student_model = user_namespace.model(
    'Student', {
        'id': fields.Integer(required=True, description='Student ID'),
        'username': fields.String(required=True, description='Username'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='Email address'),
        'admin': fields.Boolean(required=True, description='Admin'),
        'is_active': fields.Boolean(required=True, description='Shows that a user is active'),
        'courses': fields.List(fields.String, required=True, description='List of courses a student is registered in'),
        'gpa': fields.Float(required=True, description='Student GPA')
    }
)

student_update_model = user_namespace.model(
    'StudentUpdate', {
        'username': fields.String(required=True, description='Username'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='Email address'),
        'courses': fields.List(fields.String, required=True, description='List of courses a student is registered in'),
    }
)

create_student_model = user_namespace.model(
    'CreateStudent', {
        'username': fields.String(required=True, description='Username'),
        'first_name': fields.String(required=True, description='First name'),
        'last_name': fields.String(required=True, description='Last name'),
        'email': fields.String(required=True, description='Email address'),
        'password': fields.String(required=True, description='Password', load_only=True)
    }
)

gpa_model = user_namespace.model(
    'GPA', {
        'gpa': fields.Float(required=True, description='Student GPA')
    }
)



@user_namespace.route('/user')
class StudentGetCreate(Resource):
    @user_namespace.marshal_list_with(student_model)
    @user_namespace.doc(description='Get all students')
    @jwt_required()
    @admin_required()
    def get(self):
        """
        Get all students
        """
        students = Student.query.all()

        return students, HTTPStatus.OK



@user_namespace.route('/user/<int:student_id>')
class StudentGetUpdateDelete(Resource):
    @user_namespace.doc(description='Get a student by id',
        params={'student_id': 'An ID for a Student'}
        )
    @jwt_required()
    @admin_required()
    def get(self, student_id):
        """
        Get a student by id
        """
        #Check for student id
        if not student_id:
            return {"message":"Student ID is required"}, HTTPStatus.BAD_REQUEST


        #Retrieving a student
        student = Student.get_by_id(student_id)

        student_return = {}
        student_return['id'] = student.id
        student_return['username'] = student.username
        student_return['first_name'] = student.first_name
        student_return['last_name'] = student.last_name
        student_return['email'] = student.email
        student_return['courses'] = student.courses
        student_return['gpa'] = student.gpa

        return student_return, HTTPStatus.OK


    @user_namespace.doc(description='Update a student by id',
        params={'student_id': 'An ID for a Student'}
        )
    @user_namespace.expect(student_update_model)
    @jwt_required()
    def put(self, student_id):
        """
        Update a student by id
        """
        #Check for student id
        if not student_id:
            return {"message":"Student ID is required"}, HTTPStatus.BAD_REQUEST


        #Updating a student
        student_to_update = Student.get_by_id(student_id)

        data = user_namespace.payload

        student_to_update.first_name = data['first_name']
        student_to_update.last_name = data['last_name']
        student_to_update.username = data['username']
        student_to_update.email = data['email']
        student_to_update.courses = data['courses']
        
        db.session.commit()

        student_return = {}
        student_return['id'] = student_to_update.id
        student_return['username'] = student_to_update.username
        student_return['first_name'] = student_to_update.first_name
        student_return['last_name'] = student_to_update.last_name
        student_return['email'] = student_to_update.email
        student_return['courses'] = student_to_update.courses


        return student_return, HTTPStatus.OK


    @user_namespace.doc(description='Delete a student by id',
        params={'student_id': 'An ID for a Student'}
        )
    @jwt_required()
    @admin_required()
    def delete(self, student_id):
        """
        Delete a student by id
        """
        student_to_delete = Student.get_by_id(student_id)

        student_to_delete.delete()

        return {"message":"Deleted Successfully"}, HTTPStatus.NO_CONTENT



@user_namespace.route('/createstudent')
class CreateStudent(Resource):
    @user_namespace.expect(create_student_model)
    @user_namespace.doc(description='Create a student')
    @jwt_required()
    @admin_required()
    def post(self):
        """
        Create a student
        """
        data = user_namespace.payload


        #Check for existing student
        student = Student.query.filter_by(email=data['email']).first()

        if student:
            return {'message': 'Student already exists'}, HTTPStatus.BAD_REQUEST


        #Creating a student
        new_student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password'])
        )

        new_student.save()

        student_return = {}
        student_return['id'] = new_student.id
        student_return['first_name'] = new_student.first_name
        student_return['last_name'] = new_student.last_name
        student_return['username'] = new_student.username
        student_return['email'] = new_student.email


        return student_return, HTTPStatus.CREATED


@user_namespace.route('/user/<int:student_id>/gpa')
class UpdateGPA(Resource):
    @user_namespace.expect(gpa_model)
    @user_namespace.marshal_with(student_model)
    @user_namespace.doc(description='Update a student\'s GPA by id',
        params={'student_id': 'An ID for a Student'}
        )
    @jwt_required()
    @admin_required()
    def patch(self, student_id):
        """
        Update a student's GPA
        """
        data = user_namespace.payload

        gpa_to_update = Student.get_by_id(student_id)

        gpa_to_update.gpa = data['gpa']

        db.session.commit()

        return gpa_to_update, HTTPStatus.OK