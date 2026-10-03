# smartcare/persistence/in_memory_appointment_repository.py

from typing import Optional

from smartcare.domain import Appointment
from smartcare.repositories import AppointmentRepository

class InMemoryAppointmentRepository(AppointmentRepository):
    def __init__(self) -> None:
        self._appointments: dict[str, Appointment] = {}

    def add(self, appointment: Appointment) -> None:
        self._appointments[appointment.appointment_id] = appointment

    def get_by_id(self, appointment_id: str) -> Optional[Appointment]:
        return self._appointments.get(appointment_id)
