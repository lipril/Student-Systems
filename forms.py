from flask_wtf import FlaskForm
from wtforms import StringField, DateField, FloatField, SubmitField, FileField
from wtforms.validators import DataRequired

class AddStudentForm(FlaskForm):
    student_id = StringField('Student ID', validators=[DataRequired()])
    enrollment_date = DateField('Enrollment Date', validators=[DataRequired()])
    graduation_date = DateField('Graduation Date')
    class_name = StringField('Class', validators=[DataRequired()])
    department = StringField('Department', validators=[DataRequired()])
    face_image = FileField('Upload Face Image')
    submit = SubmitField('Add Student')

class AddSemesterForm(FlaskForm):
    semester_name = StringField('Semester Name', validators=[DataRequired()])
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    submit = SubmitField('Add Semester')

class AddCourseForm(FlaskForm):
    course_name = StringField('Course Name', validators=[DataRequired()])
    result = StringField('Result', validators=[DataRequired()])
    attendance = FloatField('Attendance (%)', validators=[DataRequired()])
    instructor = StringField('Instructor', validators=[DataRequired()])
    submit = SubmitField('Add Course')