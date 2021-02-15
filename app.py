from flask import Flask, render_template
import os
import database.db_connector as db
from database.db_connector import connect_to_database, execute_query

# Configuration

app = Flask(__name__)
db_connection = db.connect_to_database()

# Routes

@app.route('/')
def root():
    return render_template("main.j2")

@app.route('/students')
def students():
    print("Fetching student data")
    db_connection = connect_to_database()
    query = "SELECT * from students;"
    result = execute_query(db_connection, query).fetchall();
    print(result)
    return render_template('students.html', rows=result)

# Listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 7766))
    app.run(port = port, debug=True)


