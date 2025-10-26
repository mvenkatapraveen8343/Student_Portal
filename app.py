from flask import Flask, render_template, request, redirect, url_for
import pymysql

app = Flask(__name__)

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Praveen@8343',
    'database': 'student_portal',
    'cursorclass': pymysql.cursors.DictCursor
}

def get_db_connection():
    return pymysql.connect(**db_config)

def db_init():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS courses (
            id INT PRIMARY KEY AUTO_INCREMENT,
            course_name VARCHAR(100) NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INT PRIMARY KEY AUTO_INCREMENT,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) NOT NULL,
            course VARCHAR(50) NOT NULL
        )
    """)

    cursor.execute("SELECT COUNT(*) AS count FROM courses")
    count = cursor.fetchone()['count']
    if count == 0:
        cursor.executemany(
            "INSERT INTO courses (course_name) VALUES (%s)",
            [
                ('Python Full Stack',),
                ('Data Science',),
                ('Machine Learning',),
                ('Web Development',)
            ]
        )

    conn.commit()
    cursor.close()
    conn.close()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        course = request.form.get('course')

        cursor.execute(
            "INSERT INTO students (name, email, course) VALUES (%s, %s, %s)",
            (name, email, course)
        )
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('students'))

    cursor.execute("SELECT * FROM courses ORDER BY id ASC")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('register.html', courses=courses)

@app.route('/students')
def students():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students ORDER BY id ASC")
    students = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('students.html', students=students)

@app.route('/courses')
def courses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses ORDER BY id ASC")
    courses = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        course_name = request.form.get('course_name')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO courses (course_name) VALUES (%s)", (course_name,))
        conn.commit()
        cursor.close()
        conn.close()

        return render_template('add_course.html', message="Course Added Successfully!", msg_type="success")

    return render_template('add_course.html')

if __name__ == '__main__':
    db_init()
    app.run(debug=True)
