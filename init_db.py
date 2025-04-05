import sqlite3

# Initialize students database
conn1 = sqlite3.connect('students.db')
c1 = conn1.cursor()
c1.execute('''
    CREATE TABLE IF NOT EXISTS students (
        enrollment TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
''')
conn1.commit()
conn1.close()

# Initialize attendance database
conn2 = sqlite3.connect('attendance.db')
c2 = conn2.cursor()
c2.execute('''
    CREATE TABLE IF NOT EXISTS attendance (
        enrollment TEXT,
        name TEXT,
        date TEXT,
        time TEXT,
        PRIMARY KEY (enrollment, date)
    )
''')
conn2.commit()
conn2.close()

print("✅ Databases initialized.")
