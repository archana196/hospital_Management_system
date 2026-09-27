import sqlite3

def create_database():
    conn = sqlite3.connect("database.db")
    cursor = conn.cursor()

    # Patient table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER,
            gender TEXT,
            phone TEXT,
            symptoms TEXT,
            department TEXT,
            registration_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Queue table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS queue (
            queue_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            token_number TEXT,
            priority INTEGER,
            arrival_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            status TEXT DEFAULT 'Waiting',
            waiting_time INTEGER,
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    # Doctor table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id INTEGER PRIMARY KEY AUTOINCREMENT,
            doctor_name TEXT,
            department TEXT,
            availability TEXT,
            average_consultation_time INTEGER
        )
    """)

    # Appointment table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments (
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            patient_id INTEGER,
            appointment_date TEXT,
            appointment_time TEXT,
            status TEXT DEFAULT 'Booked',
            FOREIGN KEY (patient_id) REFERENCES patients(patient_id)
        )
    """)

    conn.commit()
    conn.close()

    print("Database created successfully!")


if __name__ == "__main__":
    create_database()