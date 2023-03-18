from ..utils import db

class User(db.Model):
    __abstract__ = True
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.Text(100), nullable=False)
    admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=False)


class Admin(User):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f'<Admin {self.username}>'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class Student(User):
    __tablename__ = 'students'
    id = db.Column(db.Integer, primary_key=True)
    courses = db.relationship('Course', backref='students', lazy=True)
    gpa = db.Column(db.Float, nullable=False, default=0.0)

    def __repr__(self):
        return f'<Student {self.username}>'


    def save(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

