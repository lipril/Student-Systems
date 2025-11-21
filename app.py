from flask import Flask, render_template, request, redirect, url_for, flash, session
from models import db, Student, Semester, Course
from forms import AddStudentForm, AddSemesterForm, AddCourseForm
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['UPLOAD_FOLDER'] = 'uploads/'
db.init_app(app)

# Ensure upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

with app.app_context():
    db.create_all()

# Admin login (hardcoded for demo; use proper auth in production)
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == 'password':  # Change this
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    students = Student.query.all()
    return render_template('admin_dashboard.html', students=students)

@app.route('/admin/add_student', methods=['GET', 'POST'])
def add_student():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    form = AddStudentForm()
    if form.validate_on_submit():
        file = form.face_image.data
        filename = None
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        student = Student(
            student_id=form.student_id.data,
            enrollment_date=form.enrollment_date.data,
            graduation_date=form.graduation_date.data,
            class_name=form.class_name.data,
            department=form.department.data,
            face_image_path=filename  # Kept for future use
        )
        db.session.add(student)
        db.session.commit()
        flash('Student added successfully')
        return redirect(url_for('admin_dashboard'))
    return render_template('add_student.html', form=form)

# Student login with ID only (face ID removed for deployability)
@app.route('/student/login', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        student_id = request.form.get('student_id')
        if student_id:
            student = Student.query.filter_by(student_id=student_id).first()
            if student:
                session['student_id'] = student.id
                return redirect(url_for('student_dashboard'))
            flash('Invalid Student ID')
    return render_template('student_login.html')

@app.route('/student/dashboard')
def student_dashboard():
    student_id = session.get('student_id')
    if not student_id:
        return redirect(url_for('student_login'))
    student = Student.query.get(student_id)
    semesters = Semester.query.filter_by(student_id=student_id).all()
    return render_template('student_dashboard.html', student=student, semesters=semesters)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))  # Use Render's PORT env var
    app.run(host='0.0.0.0', port=port, debug=False)  # Bind to 0.0.0.0 for Render
