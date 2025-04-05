import sqlite3

# Connect to the database
conn = sqlite3.connect("attendance.db")
c = conn.cursor()

# Delete attendance for Khushi on today's date (or all dates)
student_name = "Khushi"  # Use the correct case
# c.execute("DELETE FROM attendance WHERE name = ?", (student_name,))  # Delete all entries
c.execute("DELETE FROM attendance WHERE name = ? AND date = date('now')", (student_name,))

conn.commit()
conn.close()
print(f"✅ Deleted today's attendance for {student_name}.")
