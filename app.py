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

@app.route('/updatestudent/<int:id>', methods=['GET', 'POST'])
def update_student(id):
    db_connection = connect_to_database()
    # display existing data
    if request.method == 'GET':
        print('Display existing data')

        student_query = 'SELECT student_id, first_name, last_name, major, advisor_id, gpa FROM students WHERE student_id = %s' %(id)
        student_result = execute_query(db_connection, student_query).fetchone()
        

        if student_result == None:
            return "No such studen found"

        advisors_query = 'SELECT advisor_id, first_name, last_name FROM advisors'
        advisor_result = execute_query(db_connection, advisors_query).fetchall()

        # determines advisor to display in select drop down menu
        idx = 0
        for row in advisor_result:
            print(row[0])
            if row[0] == student_result[4]:
                print('success')
                break
            idx = idx + 1   
        
        return render_template('/updatestudent.html', student = student_result, advisors = advisor_result, adv_idx = idx)

    elif request.method == "POST":
        print('Post Request')
        first_name_input = request.form['first']
        last_name_input = request.form['last']
        major_input = request.form['major']
        advisor_id_input = request.form['advisor']
        gpa_input = request.form['gpa']
        query = 'UPDATE students  SET first_name = %s, last_name = %s, major = %s, advisor_id = %s, gpa = %s WHERE student_id = %s' 
        data = (first_name_input, last_name_input, major_input, advisor_id_input, gpa_input, id)
        execute_query(db_connection, query, data)
        return redirect('/students')        


@app.route('/deletestudent/<int:id>')
def delete_student(id):
    db_connection = connect_to_database()
    query = 'DELETE FROM students where student_id = %s' %(id)
    result = execute_query(db_connection, query)
    return redirect("/students")
         

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

# classes

@app.route('/classes')
def classes():
    print("Fetching class data")
    db_connection = connect_to_database()
    query = "SELECT classes.class_id, classes.class_name, classes.class_subject, instructors.first_name, instructors.last_name, classes.classroom_id FROM classes INNER JOIN instructors ON classes.instructor_id = instructors.instructor_id ORDER BY classes.class_id ASC;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('classes.html', rows=result)

@app.route('/addclass', methods=['POST','GET'])
def add_class():
        db_connection = connect_to_database()
        if request.method == 'GET':
           
            query_inst = 'SELECT instructor_id, first_name, last_name FROM instructors'
            query_class = 'SELECT classroom_id FROM classrooms'
            result_inst = execute_query(db_connection,query_inst).fetchall()
            result_class = execute_query(db_connection, query_class).fetchall()
            print(result_inst)
            print(result_class)
            return render_template('addclass.html', instructors = result_inst, classrooms = result_class)

        elif request.method == 'POST':
            print('Add new class')
            class_name_input = request.form['class']
            class_subject_input = request.form['subject']
            instructor_id_input = request.form['instructor']
            classroom_id_input = request.form['classroom']
            query = 'INSERT INTO classes (class_name, class_subject, instructor_id, classroom_id) VALUES (%s,%s,%s,%s)'
            data = (class_name_input, class_subject_input, instructor_id_input, classroom_id_input)
            execute_query(db_connection, query, data)
            return redirect('/classes') 

# classrooms

@app.route('/classrooms')
def classrooms():
    print("Fetching classroom data")
    db_connection = connect_to_database()
    query = "SELECT * FROM classrooms;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('classrooms.html', rows=result)

@app.route('/addclassroom', methods=['POST','GET'])
def add_classroom():
        db_connection = connect_to_database()
        if request.method == 'GET':
            return render_template('addclassroom.html')

        elif request.method == 'POST':
            print('Add new classroom')
            capacity_input = request.form['capacity']
            query = 'INSERT INTO classrooms (capacity) VALUES (%s)'
            data = (capacity_input)
            execute_query(db_connection, query, [data])
            return redirect('/classrooms') 

# classesstudents

@app.route('/classesstudents/<int:id>', methods=['GET', 'POST'])
def classesstudents(id):
    db_connection = connect_to_database()
    if request.method == "GET":
        print("Fetching classes_students data")
        query = "SELECT classes_students.student_id, students.first_name, students.last_name, classes_students.class_id, classes.class_name, \
                        classes.class_subject, instructors.first_name, instructors.last_name, classes.classroom_id, classes_students.grade FROM students \
                        JOIN classes_students ON classes_students.student_id = students.student_id \
                        JOIN classes ON classes_students.class_id = classes.class_id \
                        JOIN instructors on classes.instructor_id = instructors.instructor_id \
                        AND classes_students.student_id = %s" % (id)
       
        result = execute_query(db_connection, query).fetchall();
        
        classes_query = "SELECT * FROM classes;"
        classes_result = execute_query(db_connection, classes_query).fetchall();

        print(len(result))
        if len(result) >= 1:
            return render_template('classesstudents.html', rows=result, table=True, classes=classes_result)
        else:
            query = "SELECT students.student_id, students.first_name, students.last_name FROM students \
                        WHERE students.student_id = %s" % (id)
            result = execute_query(db_connection, query).fetchall();
            print(result)
            return render_template('classesstudents.html', rows=result, table=False, classes=classes_result)
    
    elif request.method == "POST":
        print("Adding class to student")
        class_id_input = request.form['class_id']
        query = 'INSERT into classes_students (student_id, class_id) VALUES (%s, %s)'
        data = (id, class_id_input)
        execute_query(db_connection, query, data)
        return redirect('/classesstudents/' + str(id))

@app.route('/updateclassesstudents/<int:st_id>/<int:cl_id>', methods=['GET', 'POST'])
def update_classes_student(st_id, cl_id):
    db_connection = connect_to_database()
    # display existing data
    if request.method == 'GET':
        print('Display existing data')
        
        query = 'SELECT * FROM classes_students WHERE student_id = %s AND class_id = %s'  
        data = (st_id, cl_id)
        result = execute_query(db_connection, query, data).fetchall()

        print(result)
        if result == None:
            return "No such class found"
        
        return render_template('/updateclassesstudents.html', student_id = st_id, class_id = cl_id)

    elif request.method == "POST":
        print('Post Request')
        grade_input = request.form['grade']
        
        query = 'UPDATE classes_students  SET grade = %s WHERE student_id = %s AND class_id = %s' 
        data = (grade_input,st_id, cl_id)
        execute_query(db_connection, query, data)
        return redirect("/classesstudents/" + str(st_id))       

@app.route('/deleteclassesstudents/<int:st_id>/<int:cl_id>')
def delete_classes_student(st_id, cl_id):
    db_connection = connect_to_database()
    query = 'DELETE FROM classes_students WHERE student_id = %s AND class_id = %s'  
    data = (st_id, cl_id)
    result = execute_query(db_connection, query, data)
    return redirect("/classesstudents/" + str(st_id))       

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7766))
    app.run(port = port, debug=True)


