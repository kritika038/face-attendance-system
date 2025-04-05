import cv2
import os
import sqlite3

def add_student(enrollment, name):
    folder = f"known_faces/{enrollment}_{name}"
    os.makedirs(folder, exist_ok=True)

    conn = sqlite3.connect("students.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO students (enrollment, name) VALUES (?, ?)", (enrollment, name))
        conn.commit()
        print(f"📝 Added {enrollment}_{name} to database.")
    except sqlite3.IntegrityError:
        print("⚠️ Student already exists.")
    conn.close()

    cap = cv2.VideoCapture(0)
    count = 0
    print("📸 Press 'c' to capture face, 'q' to quit.")
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("Capture Face", frame)
        key = cv2.waitKey(1)
        if key == ord('c'):
            path = os.path.join(folder, f"{count}.jpg")
            cv2.imwrite(path, frame)
            print(f"✅ Saved {path}")
            count += 1
        elif key == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    enrollment = input("Enter enrollment: ").strip()
    name = input("Enter name: ").strip()
    if enrollment and name:
        add_student(enrollment, name)
