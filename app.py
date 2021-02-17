from flask import Flask, render_template, request, redirect
import os
import database.db_connector as db
from database.db_connector import connect_to_database, execute_query

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes

@app.route('/')
def root():
    return render_template("index.html")

# Students

@app.route('/students')
def students():
    print("Fetching student data")
    db_connection = connect_to_database()
    query = "SELECT students.student_id, students.first_name, students.last_name, students.major, advisors.first_name, advisors.last_name, students.gpa FROM students INNER JOIN advisors ON students.advisor_id = advisors.advisor_id;"
    result = execute_query(db_connection, query).fetchall();
    # print(result)
    return render_template('students.html', rows=result)

@app.route('/addstudent', methods=['POST','GET'])
def add_student():
        db_connection = connect_to_database()
        if request.method == 'GET':
         
            query = 'SELECT advisor_id, first_name, last_name FROM advisors'
            result = execute_query(db_connection,query).fetchall()
            print(result)
            return render_template('addstudent.html', advisors = result)

        elif request.method == 'POST':

            print('Add new student')
            first_name_input = request.form['first']
            last_name_input = request.form['last']
            major_input = request.form['major']
            advisor_id_input = request.form['advisor']
            gpa_input = request.form['gpa']
            query = 'INSERT INTO students (first_name, last_name, major, advisor_id, gpa) VALUES (%s,%s,%s,%s,%s)'
            data = (first_name_input, last_name_input, major_input, advisor_id_input, gpa_input)
            execute_query(db_connection, query, data)
            return redirect('/students')        

# Instructors

@app.route('/instructors')
def instructors():
    print("Fetching instructor data")
    db_connection = connect_to_database()
    query = "SELECT * FROM instructors;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('instructors.html', rows=result)

@app.route('/addinstructor', methods=['POST','GET'])
def add_instructor():
        db_connection = connect_to_database()
        if request.method == 'GET':
            return render_template('addinstructor.html')

        elif request.method == 'POST':

            print('Add new instructor')
            first_name_input = request.form['first']
            last_name_input = request.form['last']
            department_input = request.form['department']
            query = 'INSERT INTO instructors (first_name, last_name, department) VALUES (%s,%s,%s)'
            data = (first_name_input, last_name_input, department_input)
            execute_query(db_connection, query, data)
            return redirect('/instructors')   

# Advisors

@app.route('/advisors')
def advisors():
    print("Fetching advisor data")
    db_connection = connect_to_database()
    query = "SELECT * FROM advisors;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('advisors.html', rows=result)

@app.route('/addadvisor', methods=['POST','GET'])
def add_advisor():
        db_connection = connect_to_database()
        if request.method == 'GET':
            return render_template('addadvisor.html')

        elif request.method == 'POST':
            print('Add new advisor')
            first_name_input = request.form['first']
            last_name_input = request.form['last']
            query = 'INSERT INTO advisors (first_name, last_name) VALUES (%s,%s)'
            data = (first_name_input, last_name_input)
            execute_query(db_connection, query, data)
            return redirect('/advisors')   



# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7766))
    app.run(port = port, debug=True)


