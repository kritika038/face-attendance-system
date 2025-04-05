import cv2
import os
import face_recognition
import numpy as np
import sqlite3
from datetime import datetime

# Load known faces
print("🔍 Loading known faces...")
known_face_encodings = []
known_face_names = []
known_face_enrollments = []

for folder in os.listdir("known_faces"):
    if "_" not in folder:
        continue
    enrollment, name = folder.split("_", 1)
    folder_path = os.path.join("known_faces", folder)
    for filename in os.listdir(folder_path):
        img_path = os.path.join(folder_path, filename)
        img = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(img)
        if encodings:
            known_face_encodings.append(encodings[0])
            known_face_names.append(name)
            known_face_enrollments.append(enrollment)

print(f"✅ Loaded {len(known_face_encodings)} face(s).")

# Connect to attendance database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

def mark_attendance(name, enrollment):
    now = datetime.now()
    date = now.strftime("%Y-%m-%d")
    time = now.strftime("%H:%M:%S")

    c.execute("SELECT * FROM attendance WHERE name=? AND enrollment=? AND date=?", (name, enrollment, date))
    result = c.fetchone()
    if not result:
        c.execute("INSERT INTO attendance (name, enrollment, date, time) VALUES (?, ?, ?, ?)", (name, enrollment, date, time))
        conn.commit()
        return True
    return False

# Start webcam
cap = cv2.VideoCapture(0)
print("📷 Scanning...")

recognized = False
message = ""
name_display = ""

while True:
    ret, frame = cap.read()
    if not ret:
        break

    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)
    rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small_frame)
    face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
        best_match_index = np.argmin(face_distances)

        if matches[best_match_index]:
            name = known_face_names[best_match_index]
            enrollment = known_face_enrollments[best_match_index]

            recorded = mark_attendance(name, enrollment)
            name_display = f"{enrollment}_{name}"
            message = "Attendance Recorded ✅" if recorded else "Already Recorded"
            recognized = True

            top, right, bottom, left = [v * 4 for v in face_location]
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
            cv2.putText(frame, name_display, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 255, 255), 2)
            cv2.putText(frame, message, (left, bottom + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

            break  # Only one face handled per run

    cv2.imshow("Desktop Attendance", frame)
    cv2.waitKey(1000)  # wait a bit to see message

    if recognized:
        break

cap.release()
cv2.destroyAllWindows()
print(f"✅ {message} for {name_display}")
