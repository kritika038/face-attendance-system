from flask import Flask, render_template, request
import sqlite3
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# 📅 Define holidays (MM-DD format)
SPECIAL_HOLIDAYS = ['04-14', '12-25']  # Example: Ambedkar Jayanti, Christmas

# 🧠 Get list of known students from known_faces/ directory
def get_known_students():
    students = []
    for folder in os.listdir("known_faces"):
        if "_" in folder:
            enrollment, name = folder.split("_", 1)
            students.append({"enrollment": enrollment, "name": name})
    return students

# 🧮 Calculate total working days (excluding weekends & holidays)
def get_total_working_days(start_date, end_date):
    total_days = 0
    current = start_date
    while current <= end_date:
        if current.weekday() < 5 and current.strftime("%m-%d") not in SPECIAL_HOLIDAYS:
            total_days += 1
        current += timedelta(days=1)
    return total_days

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    conn = sqlite3.connect("attendance.db")
    c = conn.cursor()

    # 📅 Get selected date or use today
    date = request.args.get("date")
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    search_query = request.args.get("search", "").strip().lower()
    known_students = get_known_students()

    # 🔍 Get all attendance records
    c.execute("SELECT name, enrollment, date FROM attendance")
    attendance_data = c.fetchall()
    present_students = {(row[1], row[2]) for row in attendance_data}  # Set of (enrollment, date)

    # ✅ Prepare final student list with present/absent for selected date
    records = []
    for student in known_students:
        enrollment = student["enrollment"]
        name = student["name"]
        status = "Present" if (enrollment, date) in present_students else "Absent"

        # 📊 Calculate attendance %
        total_days = get_total_working_days(
            datetime.strptime("2025-04-01", "%Y-%m-%d"), datetime.now()
        )
        total_present = sum(
            1 for row in attendance_data if row[1] == enrollment
        )
        attendance_percent = (total_present / total_days) * 100 if total_days else 0
        attendance_percent = round(attendance_percent, 2)

        # 🔍 Apply search filter
        if search_query in enrollment.lower() or search_query in name.lower() or search_query == "":
            records.append({
                "enrollment": enrollment,
                "name": name,
                "status": status,
                "percentage": attendance_percent
            })

    # 📅 Handle holidays and empty records
    day = datetime.strptime(date, "%Y-%m-%d")
    is_weekend = day.weekday() >= 5
    is_special_holiday = day.strftime("%m-%d") in SPECIAL_HOLIDAYS

    no_data = False
    if all(r["status"] == "Absent" for r in records):
        if is_weekend:
            no_data = "Weekend/Holiday"
        elif is_special_holiday:
            no_data = "Special Holiday"
        elif not any((r["enrollment"], date) in present_students for r in records):
            no_data = "No Data Found"

    return render_template("dashboard.html", records=records, selected_date=date, no_data=no_data)

if __name__ == "__main__":
    print("✅ Flask app initialized")
    app.run(debug=True)
