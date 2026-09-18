# Python Skeleton for SmartCare v0.3

# Structural Skeleton Only (attributes, methods)
# No business logic implemented - Methods are empty and return None or default values

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional

class Patient:
    # Supports FR-01, FR-04, FR-05

    def __init__(self, patient_id: str, name: str, phone: str, reminders_opt_in: bool = False):
        self.patient_id = patient_id
        self.name = name
        self.phone = phone
        self.reminders_opt_in = reminders_opt_in

    def book_appointment(self, practitioner: "Practitioner", when: datetime) -> "Appointment":
        # FR-01: Book an appointment with a chosen practitioner
        raise NotImplementedError("This method should be implemented to book an appointment.")

    def view_upcoming_appointments(self) -> List["Appointment"]:
        # FR-04: Patients view their own    upcoming appointments
        raise NotImplementedError("This method should be implemented to view upcoming appointments.")

    def opt_in_for_reminders(self, opt_in: bool = True) -> None:
        # FR-05: Patients opt-in for reminders
        self.reminders_opt_in = opt_in

class Practitioner:
    # Supports FR-02, FR-03, FR-06

    def __init__(self, practitioner_id: str, name: str):
        self.practitioner_id = practitioner_id
        self.name = name
        self.appointments: list[Appointment] = []

    def get_schedule(self, view: str = "day") -> list["Appointment"]:
        # FR-03: Practitioners view their own schedule
        raise NotImplementedError("This method should be implemented to get the practitioner's schedule.")

    def has_conflict(self, appointment: "Appointment", status: str) -> None:
        # FR-06: Manually update live appointment status (e.g. running late, cancelled, etc.)
        raise NotImplementedError("This method should be implemented to check for appointment conflicts.")

class Appointment:
    # Supports FR-01, FR-06, FR-07, FR-08, FR-09

    VALID_STATUSES = {"scheduled", "running late", "cancelled", "completed", "no_show"}

    def __init__(
            self, 
            appointment_id: str, 
            patient: Patient, 
            practitioner: Practitioner, 
            when: datetime, 
            status: str = "scheduled"
        ):
            self.appointment_id = appointment_id
            self.patient = patient
            self.practitioner = practitioner
            self.when = when
            self.status = status
            self.validate()

    def validate(self) -> None:
        # Reject an appointment missing patient, practitioner, or time.
        if not self.patient or not self.practitioner or not self.when:
            raise ValueError("Appointment requires a patient, practitioner, and time")

    def cancel(self) -> None:
        # FR-09 Cancel an appointemnt
        raise NotImplementedError("This method should be implemented to cancel existing appoitnments.")

    def reschedule(self, new_when: datetime) -> None:
        # FR-09 reschedule an existing appointment.
        raise NotImplementedError("This method should be implemented to reschdule canceled appointments.")

    def record_outcome(self, outcome: str) -> None:
        # FR-08 record the appointment's outcome for history
        raise NotImplementedError("This method should be implemented to record the outcome of an appointments history")


if __name__ == "__main__":
    # Mininal smoke test of the skeleton shape only
    p = Patient("P1", "Jane Citizen", "0400 000 000")
    doc = Practitioner("PR1", "Dr Singh")
    appt = Appointment("A1", p, doc, datetime(2026, 9, 20, 9, 0))
    print(f"Created {appt.appointment_id}: {p.name} with {doc.name} at {appt.when} [{appt.status}]")