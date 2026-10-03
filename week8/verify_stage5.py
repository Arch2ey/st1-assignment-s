# Stage 5 Lab - Part G verification.

from datetime import datetime

from smartcare.domain import (Appointment, AppointmentStatus,
                              InvalidStatusTransitionError, Patient, Practitioner)
from smartcare.persistence import InMemoryAppointmentRepository
from smartcare.services import AppointmentService

results = []


def check(label, condition):
    results.append(condition)
    print(f"[{'PASS' if condition else 'FAIL'}] {label}")


def raises(exc, fn, *args, **kwargs):
    try:
        fn(*args, **kwargs)
    except exc:
        return True
    except Exception:
        return False
    return False


repo = InMemoryAppointmentRepository()
service = AppointmentService(repo)
jane = Patient("P1", "Jane Citizen", "0400 000 000")
dr = Practitioner("PR1", "Dr Singh", "General Practice")
when = datetime(2026, 10, 5, 9, 0)

print("--- Booking through the service (replaces Patient.book_appointment) ---")
appt = service.book_appointment(jane, dr, when)
check("Booking returns a SCHEDULED appointment", appt.status is AppointmentStatus.SCHEDULED)
check("The appointment is linked to the practitioner", appt in dr.appointments)
check("The repository has the appointment", repo.get_by_id(appt.appointment_id) is appt)
check("A second booking at the same time is rejected (FR-02, now real)",
      raises(ValueError, service.book_appointment, jane, dr, when))
second_appt = service.book_appointment(jane, dr, datetime(2026, 10, 5, 10, 0))
check("A booking at a different time succeeds", isinstance(second_appt, Appointment))

print("--- Practitioner.appointments encapsulation (Part G change) ---")
check("appointments is a read-only tuple, not the internal list",
      isinstance(dr.appointments, tuple))
def try_append_to_appointments(practitioner, appointment):
    practitioner.appointments.append(appointment)  # tuple has no .append


check("Appending directly no longer reaches internal state",
      raises(AttributeError, try_append_to_appointments, dr, appt))
check("The only way in is add_appointment(), which type-checks its argument",
      raises(TypeError, dr.add_appointment, "not an appointment"))

print("--- Appointment behaviour is untouched from Stage 4 ---")
appt.cancel()
check("Cancel still works", appt.status is AppointmentStatus.CANCELLED)
check("Cancelling twice still raises InvalidStatusTransitionError",
      raises(InvalidStatusTransitionError, appt.cancel))
check("A cancelled slot is free again (has_conflict, now real)",
      not dr.has_conflict(when))

print(f"\n{sum(results)}/{len(results)} checks passed")

print("\n--- Injectable id generator (Part F->G modification) ---")
repo2 = InMemoryAppointmentRepository()
fixed_ids = iter(["FIXED-1", "FIXED-2"])
service2 = AppointmentService(repo2, id_generator=lambda: next(fixed_ids))
a1 = service2.book_appointment(jane, Practitioner("PR2", "Dr Lee", "Physiotherapy"), datetime(2026, 11, 1, 9, 0))
print(f"[{'PASS' if a1.appointment_id == 'FIXED-1' else 'FAIL'}] A test can inject a predictable id generator (got {a1.appointment_id!r})")
