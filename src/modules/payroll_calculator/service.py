from collections import defaultdict
from datetime import date, datetime, time
from fastapi import HTTPException, status
from src.database.core import DatabaseSession
from src.modules.clock_events.models.models import ClockEvents
from src.modules.clock_events.schemas.schemas import ClockEventTypes
from src.modules.concept.models.models import Concept
from src.modules.employees.models.employee import Employee
from src.modules.payroll_calculator.schemas import PayrollRequest, PayrollResponse
from src.modules.employee_hours.models.models import EmployeeHours, RegisterType
from sqlmodel import select


def get_employee_by_id(db: DatabaseSession, employee_id: int) -> Employee:
    employee = db.exec(select(Employee).where(Employee.id == employee_id)).one_or_none()
    if not employee:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"The employee {employee_id} was not found",
        )
    return employee


def filter_and_sort_clock_events(
    clock_events: list[ClockEvents], start_date: date, end_date: date
) -> list[ClockEvents]:
    # 1) Convertimos los límites a datetime (si queremos incluir TODO el rango del día):
    start_dt = datetime.combine(start_date, time.min)  # 00:00:00
    end_dt = datetime.combine(end_date, time.max)  # 23:59:59.999999

    # 2) Filtramos y 3) devolvemos la lista ya ordenada:
    return sorted(
        (ev for ev in clock_events if start_dt <= ev.event_date <= end_dt),
        key=lambda ev: ev.event_date,
    )


def calculate_salary(
    db: DatabaseSession, request: PayrollRequest
) -> list[PayrollResponse]:
    employee = get_employee_by_id(db, request.employee_id)
    sorted_events = filter_and_sort_clock_events(
        employee.clock_events, request.start_date, request.end_date
    )
    response: list[PayrollResponse] = []
    concepts_to_add: list[Concept] = []
    employee_hours_to_add: list[EmployeeHours] = []

    events_by_day: dict[date, list[ClockEvents]] = defaultdict(list)

    for event in sorted_events:
        event_date = date(
            event.event_date.year, event.event_date.month, event.event_date.day
        )
        events_by_day[event_date].append(event)

    for day, events in events_by_day.items():
        work_date = day
        first_check_in = min(
            time(
                event.event_date.hour,
                event.event_date.minute,
                event.event_date.second,
                event.event_date.microsecond,
            )
            for event in events
            if event.event_type == ClockEventTypes.IN
        )
        last_check_out = max(
            time(
                event.event_date.hour,
                event.event_date.minute,
                event.event_date.second,
                event.event_date.microsecond,
            )
            for event in events
            if event.event_type == ClockEventTypes.OUT
        )
        # Cantidad de eventos totales en el dia, tanto entrada como salida
        check_count = len(events)

        # 1. El empleado no hizo ni check_in ni check_out

        # 2. El empleado hizo check_in pero no check_out

        # 2.1 El empleado trabaja en turno nocturno

        # 2.1.1 El empleado hizo horas extras

        # 2.1.2 El empleado no hizo horas extras

        # 2.2 El empleado se olvidó de hacer check_out -> En las 'notes' de su Concept, colocar "Presente pero sin salida registrada"

        # 3. El empleado faltó al trabajo

        # 4. El empleado hizo check_in y check_out

        # 4.1 El empleado hizo horas extras

        # 4.2 El empleado no hizo horas extras
        first_check_in_dt = datetime.combine(work_date, first_check_in)
        last_check_out_dt = datetime.combine(work_date, last_check_out)
        time_worked_delta = last_check_out_dt - first_check_in_dt
        # Convertimos timedelta a time (ignorando días, solo horas:min:seg)
        total_seconds = int(time_worked_delta.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60
        microseconds = time_worked_delta.microseconds
        time_worked = time(
            hour=hours, minute=minutes, second=seconds, microsecond=microseconds
        )
        hourly_wage = (
            float(employee.salary) / employee.shift.working_days
        ) / employee.shift.working_hours
        daily_salary = hourly_wage * hours
        notes = "El empleado completó su jornada laboral"

        concept = Concept(description="Jornada laboral completa")

        employee_hours = EmployeeHours(
            employee_id=employee.id,
            concept_id=concept.id,
            shift_id=employee.shift.id,
            check_count=check_count,
            notes=notes,
            register_type=RegisterType.PRESENCIA,
            first_check_in=first_check_in,
            last_check_out=last_check_out,
            time_worked=time_worked,
            work_date=work_date,
            daily_salary=daily_salary,
            pay=True,
        )

        payroll_response = PayrollResponse(
            employee_hours=employee_hours,
            concept=concept,
            shift=employee.shift,
        )
        concepts_to_add.append(concept)
        employee_hours_to_add.append(employee_hours)
        response.append(payroll_response)

    db.add_all(concepts_to_add)
    db.commit()
    for concept in concepts_to_add:
        db.refresh(concept)

    for eh, concept in zip(employee_hours_to_add, concepts_to_add):
        if concept.id is not None:
            eh.concept_id = concept.id

    db.add_all(employee_hours_to_add)
    db.commit()
    for eh in employee_hours_to_add:
        db.refresh(eh)
    return response
