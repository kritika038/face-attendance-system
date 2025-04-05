
# Face Recognition Attendance System 🧑‍💼📷

This is a Python + Flask-based Face Recognition Attendance System that allows you to:

- Register students with face images 🧑‍🎓
- Scan faces to mark attendance via webcam 🎥
- View attendance on a dashboard with date selection and search 📅🔍
- Store data in SQLite database 🗃️
- Export attendance to CSV or integrate with additional tools 🧾

---

## 📁 Folder Structure

```
face_attendance_system/
├── known_faces/            # Contains folders for each student with their face images
├── templates/              # HTML templates (index, dashboard)
│   ├── index.html
│   └── dashboard.html
├── static/css/             # CSS styling
├── students.db             # SQLite DB for student details
├── attendance.db           # SQLite DB for attendance logs
├── desktop_attendance.py   # Script for scanning and marking attendance
├── app.py                  # Flask web app
├── add_student.py          # Script to register a new student
├── init_db.py              # Script to initialize DBs
├── requirements.txt        # All Python dependencies
```

---

## 🚀 How to Run

### 1. Install Requirements
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Add a Student
```bash
python add_student.py
```

### 4. Run Attendance Scanner
```bash
python desktop_attendance.py
```

### 5. Run Flask Web App
```bash
python app.py
```

Visit 👉 `http://127.0.0.1:5000/dashboard` to see the attendance dashboard.

---

## 🔍 Features

- Live webcam-based face detection
- Marks attendance only once per student per day
- Supports searching by name or enrollment
- Calendar-based date filtering
- Shows **"No data found"** on weekends and non-attendance days
- Clean UI & extendable

---

## 🛠 Tech Stack

- Python
- OpenCV
- face_recognition (Dlib)
- Flask
- SQLite
- HTML/CSS

---

## 🧠 Future Improvements

- Admin login for security 🔐
- Export to Excel or PDF
- Real-time charts 📊
- Mobile responsiveness 📱

---

## 🧑‍💻 Author

**Kritika**  
GitHub: [kritika038](https://github.com/kritika038)

---

Feel free to fork, star ⭐ this repo, and contribute!

