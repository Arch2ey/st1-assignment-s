# smartcare/presentation/cli.py

from datetime import datetime

from smartcare.domain import Patient, Practitioner
from smartcare.persistence import InMemoryAppointmentRepository
from smartcare.services import AppointmentService


def main() -> None:
    repository = InMemoryAppointmentRepository()
    service = AppointmentService(repository)

    p = Patient("P1", "Jane Citizen", "0400 000 000")
    doc = Practitioner("PR1", "Dr Singh", "General Practice")
    appt = service.book_appointment(p, doc, datetime(2026, 9, 20, 9, 0))
    print(f"Created {appt.appointment_id}: {p.name} with {doc.name} "
         f"at {appt.when} [{appt.status.value}]")


if __name__ == "__main__":
    main()