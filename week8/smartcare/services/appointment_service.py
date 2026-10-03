# smartcare/services/appointment_service.py

from datetime import datetime
from itertools import count
from typing import Callable, Optional

from smartcare.domain import Appointment, Patient, Practitioner
from smartcare.repositories import AppointmentRepository


def _default_id_generator() -> Callable[[], str]:
    # Assumption: nothing in v0.2 says how appointment_id is generated
    # A simple counter is the smallest thing that produces a unique id; 
    # confirm the real scheme with the client before this goes further.
    counter = count(1)
    return lambda: f"A{next(counter)}"


class AppointmentService:
    """Coordinates the booking workflow (FR-01), which needs Patient,
    Practitioner and Appointment together - moved off Patient in Part D.
    """

    def __init__(self, repository: AppointmentRepository,
                id_generator: Optional[Callable[[], str]] = None) -> None:
        self._repository = repository
        # Part F's AI review flagged the original module-level counter as a
        # hidden-state testability problem (IDs kept climbing across
        # unrelated tests in the same process). Modified in Part G: the
        # generator is now a constructor parameter with the same counter as
        # its default, so a test can inject a predictable one instead.
        self._next_id = id_generator or _default_id_generator()

    def book_appointment(self, patient: Patient, practitioner: Practitioner,
                         when: datetime) -> Appointment:
        if practitioner.has_conflict(when):
            raise ValueError("practitioner already has an appointment at that time")
        appointment = Appointment(self._next_id(), patient, practitioner, when)
        practitioner.add_appointment(appointment)
        self._repository.add(appointment)
        return appointment
