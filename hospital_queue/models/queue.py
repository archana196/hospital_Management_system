from datetime import datetime


def calculate_waiting_time(arrival_time):
    """
    Calculate how many minutes a patient has been waiting.
    """

    arrival = datetime.fromisoformat(arrival_time)
    now = datetime.now()

    waiting_minutes = int((now - arrival).total_seconds() / 60)

    return max(waiting_minutes, 0)


def get_next_patient(patients):
    """
    Select the next patient using:
    1. Priority
    2. Waiting time
    3. Arrival time
    """

    if not patients:
        return None

    # Calculate waiting time
    for patient in patients:
        patient["waiting_time"] = calculate_waiting_time(
            patient["arrival_time"]
        )

    # Sort:
    # Priority 1 = Emergency
    # Priority 2 = Urgent
    # Priority 3 = Normal
    #
    # Within same priority:
    # Longer waiting patient first
    # If same waiting time, earlier arrival first

    patients.sort(
        key=lambda x: (
            x["priority"],
            -x["waiting_time"],
            x["arrival_time"]
        )
    )

    return patients[0]