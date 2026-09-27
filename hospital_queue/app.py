from flask import Flask, render_template
import sqlite3
from datetime import datetime

app = Flask(__name__)


def get_waiting_patients():

    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            queue.queue_id,
            queue.token_number,
            queue.priority,
            queue.arrival_time,
            queue.status,
            patients.name,
            patients.department
        FROM queue
        JOIN patients
        ON queue.patient_id = patients.patient_id
        WHERE queue.status = 'Waiting'
    """)

    patients = cursor.fetchall()

    conn.close()

    return patients


def calculate_waiting_time(arrival_time):

    try:
        arrival = datetime.fromisoformat(arrival_time)
        now = datetime.now()

        minutes = int(
            (now - arrival).total_seconds() / 60
        )

        return max(minutes, 0)

    except:
        return 0


def fair_queue_sort(patients):

    patient_list = []

    for patient in patients:

        patient_data = dict(patient)

        waiting_time = calculate_waiting_time(
            patient_data["arrival_time"]
        )

        patient_data["waiting_time"] = waiting_time

        patient_list.append(patient_data)

    # Priority:
    # 1 = Emergency
    # 2 = Urgent
    # 3 = Normal
    #
    # Same priority → longer waiting time first

    patient_list.sort(
        key=lambda x: (
            x["priority"],
            -x["waiting_time"],
            x["arrival_time"]
        )
    )

    return patient_list


@app.route("/")
def home():

    return render_template("register.html")


@app.route("/doctor")
def doctor_dashboard():

    patients = get_waiting_patients()

    patients = fair_queue_sort(patients)

    return render_template(
        "doctor_dashboard.html",
        patients=patients
    )


if __name__ == "__main__":
    app.run(debug=True)