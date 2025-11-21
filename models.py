from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    enrollment_date = db.Column(db.Date, nullable=False)
    graduation_date = db.Column(db.Date, nullable=True)
    class_name = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    face_image_path = db.Column(db.String(200), nullable=True)  # Path to uploaded face image

class Semester(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    semester_name = db.Column(db.String(50), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    courses = db.relationship('Course', backref='semester', lazy=True)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    semester_id = db.Column(db.Integer, db.ForeignKey('semester.id'), nullable=False)
    course_name = db.Column(db.String(100), nullable=False)
    result = db.Column(db.String(10), nullable=False)  # e.g., A, B, Pass
    attendance = db.Column(db.Float, nullable=False)  # e.g., 85.5%
    instructor = db.Column(db.String(100), nullable=False)