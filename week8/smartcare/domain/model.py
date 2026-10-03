# smartcare/domain/model.py

from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import List

def _require_text(value: str, label: str) -> str:
    # Basic validation
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be a non-empty string")
    return value.strip()

class Patient:
    # Supports FR-04, FR-05

    def __init__(self, patient_id: str, name: str, phone: str, reminders_opt_in: bool = False):
        self.__patient_id = _require_text(patient_id, "patient_id")
        self.__name = _require_text(name, "name")
        self.__phone = _require_text(phone, "phone")
        if not isinstance(reminders_opt_in, bool):
            raise ValueError("reminders_opt_in must be True or False")
        self.__reminders_opt_in = reminders_opt_in

    @property
    def patient_id(self) -> str:
        return self.__patient_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def phone(self) -> str:
        return self.__phone

    @property
    def reminders_opt_in(self) -> bool:
        return self.__reminders_opt_in

    def view_upcoming_appointments(self) -> list["Appointment"]:
        # FR-04: Patients can view their upcoming appointments
        raise NotImplementedError("This method should be implemented to view upcoming appointments")

    def opt_in_for_reminders(self, opt_in: bool = True) -> None:
        # FR-05: Patients can opt in for reminders
        if not isinstance(opt_in, bool):
            raise ValueError("opt_in must be True or False")
        self.__reminders_opt_in = opt_in

class Practitioner:
    # Supports FR-02, FR-03, and FR-06

    def __init__(self, practitioner_id: str, name: str, specialty: str):
        self.__practitioner_id = _require_text(practitioner_id, "practitioner_id")
        self.__name = _require_text(name, "name")
        self.__specialty = _require_text(specialty, "specialty")
        self.__appointments: list[Appointment] = []

    @property
    def practitioner_id(self) -> str:
        return self.__practitioner_id

    @property
    def name(self) -> str:
        return self.__name

    @property
    def specialty(self) -> str:
        return self.__specialty

    @property
    def appointments(self) -> tuple:
        # Read-only copy.
        return tuple(self.__appointments)

    def add_appointment(self, appointment: "Appointment") -> None:
        if not isinstance(appointment, Appointment):
            raise TypeError("appointment must be an instance of Appointment")
        self.__appointments.append(appointment)

    def get_schedule(self, view: str = "day") -> list["Appointment"]:
        # FR-03: Practitioners view their own schedule
        raise NotImplementedError("This method should be implemented to get the practitioner's schedule")

    def has_conflict(self, when: datetime) -> bool:
        # FR-02: True if a non-cancelled appointment already exists at this time.
        # Restored
        return any(a.when == when and a.status is not AppointmentStatus.CANCELLED
                   for a in self.__appointments)

    def update_status(self, appointment: "Appointment", status: "AppointmentStatus") -> None:
        raise NotImplementedError("This method should be implemented to update an appointment's status")


# Ai Implemented Appointments
class AppointmentStatus(Enum):
    SCHEDULED = "scheduled"
    RUNNING_LATE = "running late"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    NO_SHOW = "no_show"

class InvalidStatusTransitionError(Exception):
    # Raised when an appointment status change is not allowed
    pass

# Legal status changes. Cancelled, completed and no-show are final
_S = AppointmentStatus
_ALLOWED_TRANSITIONS = {
    _S.SCHEDULED: {_S.RUNNING_LATE, _S.CANCELLED, _S.COMPLETED, _S.NO_SHOW},
    _S.RUNNING_LATE: {_S.CANCELLED, _S.COMPLETED, _S.NO_SHOW},
    _S.CANCELLED: set(),
    _S.COMPLETED: set(),
    _S.NO_SHOW: set(),
}

class Appointment:
    # Supports FR-01, FR-06, FR-07, FR-08, FR-09
    def __init__(
            self, 
            appointment_id: str, 
            patient: Patient, 
            practitioner: Practitioner, 
            when: datetime, 
            status: AppointmentStatus = AppointmentStatus.SCHEDULED
        ):
            self.__appointment_id = appointment_id
            self._patient = patient
            self._practitioner = practitioner
            self._when = when
            self._status = status
            self.validate()

    @property
    def appointment_id(self) -> str:
        return self.__appointment_id

    @property
    def patient(self) -> Patient:
        return self._patient

    @property
    def practitioner(self) -> Practitioner:
        return self._practitioner

    @property
    def when(self) -> datetime:
        return self._when

    @property
    def status(self) -> AppointmentStatus:
        # Read-only: status can only change through the methods below
        return self._status

    def validate(self) -> None:
        # Reject an appointment missing patient, practitioner, or time (or with the wrong types)
        if (not isinstance(self._patient, Patient)
                or not isinstance(self._practitioner, Practitioner)
                or not isinstance(self._when, datetime)):
            raise ValueError("Appointment requires a patient, practitioner, and time")
        if not isinstance(self._status, AppointmentStatus):
            raise ValueError("status must be an AppointmentStatus")
        _require_text(self.__appointment_id, "appointment_id")

    def _change_status(self, new_status: AppointmentStatus) -> None:
        # The one place status changes, so the transition rules cannot be bypassed
        if new_status not in _ALLOWED_TRANSITIONS[self._status]:
            raise InvalidStatusTransitionError(
                f"cannot change status from {self._status.value} to {new_status.value}")
        self._status = new_status

    def cancel(self) -> None:
        # FR-09 Cancel an appointment (the object stays, so it remains part of the history)
        self._change_status(AppointmentStatus.CANCELLED)

    def reschedule(self, new_when: datetime) -> None:
        # FR-09 reschedule an existing appointment.
        raise NotImplementedError("This method should be implemented to reschedule existing appointments.")

    def record_outcome(self, outcome: str) -> None:
        # FR-08 record the appointment's outcome for history
        raise NotImplementedError("This method should be implemented to record the outcome of an appointment.")

    