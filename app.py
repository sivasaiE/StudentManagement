from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import sqlite3

app = Flask(__name__)


def db_conn():
    conn = sqlite3.connect('Students.db')
    cursor = conn.cursor()
    cursor.execute('SELECT count(name) FROM sqlite_master WHERE type="table" AND name="STUDENTS";')
    value = cursor.fetchone()[0]
    if value:
        return (conn, cursor)
    else:
        cursor.execute('CREATE TABLE STUDENTS (id INTEGER PRIMARY KEY AUTOINCREMENT, NAME TEXT NOT NULL, GRADE TEXT NOT NULL, ADDRESS TEXT NOT NULL, PHONENO INT NOT NULL, AGE INT NOT NULL)')
        conn.commit()
        return (conn,cursor)
    

@app.route('/')
def welcome():
    return render_template("Welcomepage.html")


@app.route("/createStudent", methods=["GET", "POST"])
def createStudent():
    conn,cursor = db_conn()
    if request.method == "GET":
        return render_template("createStudent.html")
    elif request.method=="POST":
        name = request.form.get("name")
        age = request.form.get("age")
        grade = request.form.get("grade")
        phone_no = request.form.get("phone-no")
        address = request.form.get("address")
        cursor.execute("INSERT INTO Students (NAME,GRADE,ADDRESS,PHONENO, AGE) Values (?,?,?,?,?)",(name,grade,address,phone_no,age))
        conn.commit()
        return "new Student successfully created"
        
        
    return "Invalid Method"

@app.route("/viewStudent", methods=["GET", "POST"])
def viewStudent():
    if request.method == "GET":
        return render_template("viewStudent.html")
    elif request.method=="POST":
        conn,cursor = db_conn()
        name = request.form.get("name")
        phone_no = request.form.get("phone-no")
        age = request.form.get("age")
        try:
            cursor.execute('SELECT * FROM Students WHERE AGE = ? AND PHONENO = ? AND NAME = ?', (age, phone_no, name))
            result = cursor.fetchall()     
            if result:
                for row in result:
                    return f"{row} \nSuccessfully Viewed"
            else:
                return "No matching Students present"
        except sqlite3.Error as e:
            return "Invalid user details"

    return "Invalid Method"


@app.route("/deleteStudent", methods=["GET", "POST"])
def deleteStudent():
    if request.method == "GET":
        return render_template("deleteStudent.html")
    elif request.method=="POST":
        conn,cursor = db_conn()
        name = request.form.get("name")
        phone_no = request.form.get("phone-no")
        age = request.form.get("age")
        print(name, phone_no)
        try:
            cursor.execute('DELETE FROM Students WHERE NAME = ? and  AGE=? and PHONENO=?',(name,phone_no,age))
            if cursor.rowcount == 0 :
                return "No student present with this details"
            else:
                conn.commit()
                return "Student has been deleted Successsfully"
        except sqlite3.Error as e:
            return f"error as e"
    return "Invalid Method"




if __name__ == "__main__":
    app.run(debug=True, port=5000)