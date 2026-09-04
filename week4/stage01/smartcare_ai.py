appointments = {}

# Improvement fixed the duplicate booking gap
def book_appointment(patient_name, practitioner_name, appointment_time):
    if not patient_name:
        raise ValueError("Patient name cannot be empty")
    for appointment in appointments:
        if appointment["practitioner"] == practitioner_name and appointment["time"] == appointment_time:
            raise ValueError("This practitioner already has an appointment at that time")
    appointment = {
        "patient": patient_name,
        "practitioner": practitioner_name,
        "time": appointment_time
    }
    appointments.append(appointment)

def show_all_appointments():
    for appointment_id, details in appointments.items():
        print(f"{appointment_id}: {details['patient_name']} with {details['practitioner_name']} at {details['appointment_time']}")

book_appointment("Alice Smith", "Dr. John Doe", "2024-07-20 10:00 AM")
book_appointment("Bob Johnson", "Dr. Jane Roe", "2024-07-20 11:30 AM")
show_all_appointments()