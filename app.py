from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Sample data storage (no database)
tutors = {
    "john": {
        "name": "John Doe",
        "subjects": "Mathematics, Physics",
        "schedule": ["Mon 10:00 AM", "Wed 2:00 PM"],
        "students": ["emma"]
    },
    "sarah": {
        "name": "Sarah Smith",
        "subjects": "English, History",
        "schedule": ["Tue 11:00 AM", "Thu 3:00 PM"],
        "students": ["mike"]
    }
}

students = {
    "emma": {
        "name": "Emma Wilson",
        "progress": [
            {"date": "2023-10-01", "topic": "Algebra Basics", "score": "85%"},
            {"date": "2023-10-08", "topic": "Trigonometry", "score": "78%"}
        ]
    },
    "mike": {
        "name": "Mike Johnson",
        "progress": [
            {"date": "2023-10-02", "topic": "Shakespeare", "score": "92%"}
        ]
    }
}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/tutor/<tutor_id>')
def tutor_dashboard(tutor_id):
    tutor = tutors.get(tutor_id)
    if tutor:
        return render_template('tutor_dashboard.html', 
                            tutor=tutor,
                            student_list={k: students[k] for k in tutor['students']})
    return redirect(url_for('home'))

@app.route('/student/<student_id>')
def student_dashboard(student_id):
    student = students.get(student_id)
    if student:
        return render_template('student_dashboard.html', student=student)
    return redirect(url_for('home'))

@app.route('/class/<tutor_id>')
def class_session(tutor_id):
    tutor = tutors.get(tutor_id)
    if tutor:
        return render_template('class.html', tutor=tutor)
    return redirect(url_for('home'))

@app.route('/add_schedule/<tutor_id>', methods=['POST'])
def add_schedule(tutor_id):
    tutor = tutors.get(tutor_id)
    if tutor and request.method == 'POST':
        new_slot = request.form.get('time_slot')
        if new_slot:
            tutor['schedule'].append(new_slot)
    return redirect(url_for('tutor_dashboard', tutor_id=tutor_id))

@app.route('/add_progress/<student_id>', methods=['POST'])
def add_progress(student_id):
    student = students.get(student_id)
    if student and request.method == 'POST':
        new_entry = {
            "date": request.form.get('date'),
            "topic": request.form.get('topic'),
            "score": request.form.get('score')
        }
        student['progress'].append(new_entry)
    return redirect(url_for('student_dashboard', student_id=student_id))

if __name__ == '__main__':
    app.run(debug=True)