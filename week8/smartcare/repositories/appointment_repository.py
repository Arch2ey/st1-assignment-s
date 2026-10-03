# smartcare/repositories/appointment_repository.py

from abc import ABC, abstractmethod
from typing import Optional

from smartcare.domain import Appointment


class AppointmentRepository(ABC):

    @abstractmethod
    def add(self, appointment: Appointment) -> None:
        """Persist a newly created appointment."""

    @abstractmethod
    def get_by_id(self, appointment_id: str) -> Optional[Appointment]:
        """Return the appointment with this id, or None if it doesn't exist."""
