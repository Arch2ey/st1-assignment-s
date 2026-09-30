# Stage 4 Lab - Part F manual behaviour checks
from datetime import datetime

from smartcare_v04 import (Appointment, AppointmentStatus, InvalidStatusTransitionError,
                              Patient, Practitioner)

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


when = datetime(2026, 10, 5, 9, 0)

print("--- F1: create valid objects ---")
jane = Patient("P1", "Jane Citizen", "0400 000 000")
dr = Practitioner("PR1", "Dr Singh", "General Practice")
appt = Appointment("A1", jane, dr, when)
check("Patient created with the values given", jane.name == "Jane Citizen" and jane.reminders_opt_in is False)
check("Practitioner created with id, name and specialty", dr.specialty == "General Practice")
check("Appointment starts SCHEDULED", appt.status is AppointmentStatus.SCHEDULED)

print("--- F2: invalid input ---")
check("Blank patient name rejected", raises(ValueError, Patient, "P2", "   ", "0400 000 000"))
check("Missing patient id rejected", raises(ValueError, Patient, "", "Sam", "0400 000 000"))
check("Non-text phone rejected", raises(ValueError, Patient, "P2", "Sam", 12345))
check("Blank specialty rejected", raises(ValueError, Practitioner, "PR2", "Dr Lee", ""))
check("Appointment without a patient rejected", raises(ValueError, Appointment, "A2", None, dr, when))
check("Appointment with a text time rejected", raises(ValueError, Appointment, "A2", jane, dr, "tomorrow"))
check("Appointment with a made-up status rejected", raises(ValueError, Appointment, "A2", jane, dr, when, "cancelled"))
check("status cannot be assigned directly", raises(AttributeError, setattr, appt, "status", AppointmentStatus.COMPLETED))

print("--- F3: cancel a scheduled appointment ---")
appt.cancel()
check("Status is now CANCELLED", appt.status is AppointmentStatus.CANCELLED)
check("The cancelled appointment still exists as an object", appt.patient is jane and appt.when == when)

print("--- F4: illegal repeated transition ---")
check("Cancelling again raises InvalidStatusTransitionError", raises(InvalidStatusTransitionError, appt.cancel))
check("Status is unchanged after the illegal attempt", appt.status is AppointmentStatus.CANCELLED)

print(f"\n{sum(results)}/{len(results)} checks passed")
