from ..utils import db
from enum import Enum
from datetime import datetime

class CourseGrade(Enum):
    A = 5.0
    B = 4.0
    C = 3.0
    D = 2.0
    E = 1.0
    F = 0.0

class CourseUnits(Enum):
    EXCELLENT = 4.0
    GOOD = 3.0
    CREDIT = 2.0
    PASS = 1.0
    FAIL = 0.0

class Course(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    course_code = db.Column(db.String(100), nullable=False, unique=True)
    course_units = db.Column(db.Enum(CourseUnits), default=CourseUnits.FAIL)
    grade = db.Column(db.Enum(CourseGrade), default=CourseGrade.F)
    description = db.Column(db.String(200), nullable=False)
    teacher = db.Column(db.String(100), nullable=False)
    student = db.Column(db.Integer(), db.ForeignKey('students.id'))
    date_created = db.Column(db.DateTime(), default=datetime.now)

    def __repr__(self):
        return f'<Course {self.name}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()