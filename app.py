from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Database connection
def get_db():
    return sqlite3.connect("attendance.db")

# Home page
@app.route("/")
def index():
    return render_template("index.html")

# Add student
@app.route("/add", methods=["GET", "POST"])
def add_student():
    if request.method == "POST":
        roll = request.form["roll"]
        name = request.form["name"]

        conn = get_db()
        cur = conn.cursor()
        cur.execute("INSERT INTO students VALUES (?, ?)", (roll, name))
        conn.commit()
        conn.close()

        return redirect("/")
    return render_template("add_student.html")

# Mark attendance
@app.route("/mark", methods=["GET", "POST"])
def mark_attendance():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM students")
    students = cur.fetchall()

    if request.method == "POST":
        roll = request.form["roll"]
        status = request.form["status"]

        cur.execute("INSERT INTO attendance VALUES (?, ?)", (roll, status))
        conn.commit()
        conn.close()
        return redirect("/")

    conn.close()
    return render_template("mark_attendance.html", students=students)

# View attendance
@app.route("/view")
def view_attendance():
    conn = get_db()
    cur = conn.cursor()
    cur.execute("""
        SELECT students.roll, students.name, attendance.status
        FROM students
        JOIN attendance ON students.roll = attendance.roll
    """)
    data = cur.fetchall()
    conn.close()
    return render_template("view_attendance.html", data=data)

# Create tables and run app
if __name__ == "__main__":
    conn = get_db()
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS students (roll TEXT, name TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS attendance (roll TEXT, status TEXT)")
    conn.commit()
    conn.close()

    app.run(debug=True)
