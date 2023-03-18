from flask_restx import Namespace, Resource, fields
from functools import wraps
from ..utils.decorator import admin_required, user_type
from ..models.users import Student
from ..models.courses import Course
from ..utils import db
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt, verify_jwt_in_request


course_namespace = Namespace('course', description='Namespace for Courses')

course_model = course_namespace.model(
    'Course', {
        'id': fields.Integer(required=True, description='Course ID'),
        'name': fields.String(required=True, description='Course name'),
        'course_code': fields.String(required=True, description='Course code'),
        'course_units': fields.String(required=True, description='Course units', enum=['EXCELLENT', 'GOOD', 'CREDIT', 'PASS', 'FAIL']),
        'grade': fields.String(required=True, description='Course grade', enum=['A', 'B', 'C', 'D', 'E', 'F']),
        'description': fields.String(required=True, description='Course description'),
        'teacher': fields.String(required=True, description='Course teacher'),
        'students': fields.Integer(required=True, description='Course students')
    }
)

create_course_model = course_namespace.model(
    'CreateCourse', {
        'name': fields.String(required=True, description='Course name'),
        'course_code': fields.String(required=True, description='Course code'),
        'description': fields.String(required=True, description='Course description'),
        'teacher': fields.String(required=True, description='Course teacher')
    }
)

grade_model = course_namespace.model(
    'Grade', {
        'grade': fields.String(required=True, description='Course grade', enum=['A', 'B', 'C', 'D', 'E', 'F'])
    }
)

student_course_register_model = course_namespace.model(
    'StudentCourseRegister', {
        'course_id': fields.Integer(required=True, description='Course ID'),
        'student_id': fields.Integer(required=True, description='Student ID')
    }
)



@course_namespace.route('/course/<int:course_id>')
class CourseGetUpdateDelete(Resource):
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Get a course by id',
        params={'course_id': 'An ID for a Course'})
    @jwt_required()
    def get(self, course_id):
        """
        Get a course by id
        """
        course = Course.get_by_id(course_id)

        return course, HTTPStatus.OK

    @course_namespace.expect(course_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Update a course by id',
        params={'course_id': 'An ID for a Course'})
    @jwt_required()
    @admin_required()
    def put(self, course_id):
        """
        Update a course by id
        """
        course_to_update = Course.get_by_id(course_id)

        data = course_namespace.payload

        course_to_update.name = data['name']
        course_to_update.course_code = data['course_code']
        course_to_update.course_units = data['course_units']
        course_to_update.description = data['description']
        course_to_update.teacher = data['teacher']
        course_to_update.grade = data['grade']
        
        db.session.commit()

        return course_to_update, HTTPStatus.OK


    @course_namespace.doc(
        description='Delete a course by id',
        params={'course_id': 'An ID for a Course'})
    @jwt_required()
    @admin_required()
    def delete(self, course_id):
        """
        Delete a course by id
        """
        course_to_delete = Course.get_by_id(course_id)

        course_to_delete.delete()

        return {"message":"Deleted Successfully"}, HTTPStatus.NO_CONTENT



@course_namespace.route('/user/<int:student_id>/courses')
class StudentCourses(Resource):
    @course_namespace.doc(
        description='Get all courses registered for by a student by student id',
        params= {
            'student_id': 'An ID for a student'
        }
    )
    @jwt_required()
    def get(self, student_id):
        """
            Get all courses a student is registered for
        """
        student = Student.get_by_id(student_id)

        courses = student.courses
        ret = []

        for course in courses:
            course_ret = {}
            course_ret['id'] = course.id,
            course_ret['name'] = course.name,
            course_ret['course_code'] = course.course_code,
            course_ret['course_units'] = course.course_units,
            course_ret['description'] = course.description,
            course_ret['teacher'] = course.teacher,
            course_ret['grade'] = course.grade,

            ret.append(course_ret)

        return ret, HTTPStatus.OK



@course_namespace.route('/create')
class CreateCourse(Resource):
    @course_namespace.expect(create_course_model)
    @course_namespace.doc(
        description='Create a course')
    @jwt_required()
    def post(self):
        """
        Create a course
        """
        data = course_namespace.payload


        # Check if course already exists
        course = Course.query.filter_by(course_code=data['course_code']).first()

        if course:
            return {'message': 'Course already exists'}, HTTPStatus.BAD_REQUEST


        # Create course
        course_create = Course(
            name=data['name'],
            course_code=data['course_code'],
            description=data['description'],
            teacher=data['teacher']
        )

        course_create.save()

        course_return = {}
        course_return['id'] = course_create.id
        course_return['name'] = course_create.name
        course_return['course_code'] = course_create.course_code
        course_return['description'] = course_create.description
        course_return['teacher'] = course_create.teacher

        return course_return, HTTPStatus.CREATED


@course_namespace.route('/course')
class GetCourse(Resource):
    @course_namespace.marshal_list_with(course_model)
    @course_namespace.doc(description='Get all courses')
    @jwt_required()
    def get(self):
        """
        Get all courses
        """
        courses = Course.query.all()

        return courses, HTTPStatus.OK


@course_namespace.route('/course/<int:course_id>/grade')
class UpdateGrade(Resource):
    @course_namespace.expect(grade_model)
    @course_namespace.marshal_with(course_model)
    @course_namespace.doc(
        description='Update a Course\'s Grade',
        params={'course_id': 'An ID for a Course'})
    @jwt_required()
    @admin_required()
    def patch(self, course_id):
        """
        Update a Course's Grade
        """
        data = course_namespace.payload

        grade_to_update = Course.get_by_id(course_id)

        grade_to_update.gpa = data['grade']

        db.session.commit()

        return grade_to_update, HTTPStatus.OK


@course_namespace.route('/course/<int:course_id>/student')
class RegisterStudent(Resource):
    @course_namespace.expect(student_course_register_model)
    @course_namespace.doc(
        description='Register a student for a course',
        params={
            'course_id': 'An ID for a course',
            'student_id': 'An ID for a student'
        }
    )
    @jwt_required()
    def post(self, course_id):
        """
        Register a student for a course
        """
        data = course_namespace.payload

        student = Student.get_by_id(data['student_id'])
        course = Course.get_by_id(course_id)

        student.courses.append(course)

        db.session.commit()

        return {"message":"Registered Successfully"}, HTTPStatus.OK
