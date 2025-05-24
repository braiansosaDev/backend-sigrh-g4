from collections import defaultdict
from datetime import date, datetime, time, timedelta
from fastapi import HTTPException, status
from src.database.core import DatabaseSession
from src.modules.clock_events.models.models import ClockEvents
from src.modules.clock_events.schemas.schemas import ClockEventTypes
from src.modules.concept.models.models import Concept
from src.modules.employees.models.employee import Employee
from src.modules.payroll_calculator.schemas import (
    ConceptSchema,
    EmployeeHoursSchema,
    PayrollRequest,
    PayrollResponse,
    ShiftSchema,
)
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


def get_date_range(start_date: date, end_date: date) -> list[date]:
    # Determina el orden correcto de las fechas
    start = min(start_date, end_date)
    end = max(start_date, end_date)

    # Calcula la cantidad de días entre las fechas
    delta_days = (end - start).days

    # Genera la lista de fechas
    return [start + timedelta(days=i) for i in range(delta_days + 1)]


def calculate_salary(
    db: DatabaseSession, request: PayrollRequest
) -> list[PayrollResponse]:
    employee = get_employee_by_id(db, request.employee_id)
    sorted_events = filter_and_sort_clock_events(
        employee.clock_events, request.start_date, request.end_date
    )

    date_range = get_date_range(request.start_date, request.end_date)
    response: list[PayrollResponse] = []
    concepts_to_add: list[Concept] = []
    employee_hours_to_add: list[EmployeeHours] = []

    events_by_day: dict[date, list[ClockEvents]] = defaultdict(list)

    # 1) Agrupar eventos por día
    for event in sorted_events:
        event_day = date(
            event.event_date.year, event.event_date.month, event.event_date.day
        )
        events_by_day[event_day].append(event)

    # 2) Para cada día hábil, procesar según tenga o no eventos
    for day in date_range:
        # saltar sábados y domingos
        if day.weekday() in (5, 6):
            continue

        daily_events = events_by_day.get(day, [])
        if not daily_events:
            log_employee_absence(
                employee, concepts_to_add, employee_hours_to_add, day, None, None, 0
            )
            continue

        # No hubo eventos → marcar como ausente

        # for day in date_range:
        #     if day.weekday() in (5, 6):
        #         continue
        #     for event in sorted_events:
        #         event_date = date(
        #             event.event_date.year, event.event_date.month, event.event_date.day
        #         )
        #         if event_date == day:
        #             events_by_day[day].append(event)
        #             break
        #     add_missing_event(
        #         employee, concepts_to_add, employee_hours_to_add, day, None, None, 0
        #     )

        # for day in date_range:
        #     flag = True
        #     if day.weekday() in (5, 6):
        #         continue
        #     for event in sorted_events:
        #         event_date = date(
        #             event.event_date.year, event.event_date.month, event.event_date.day
        #         )
        #         if event_date != day:
        #             flag = flag and True
        #             break
        #         flag = flag and False
        #     if flag:
        #         add_missing_event(
        #             employee, concepts_to_add, employee_hours_to_add, day, None, None, 0
        #         )

        ins = [ev for ev in daily_events if ev.event_type == ClockEventTypes.IN]
        outs = [ev for ev in daily_events if ev.event_type == ClockEventTypes.OUT]

        first_check = min(ins, key=lambda ev: ev.event_date).event_date.time()
        last_check = max(outs, key=lambda ev: ev.event_date).event_date.time()
        first_check_hour = datetime.combine(day, first_check).hour
        last_check_hour = datetime.combine(day, last_check).hour
        worked_hours_difference = last_check_hour - first_check_hour
        extra_hours = worked_hours_difference - employee.shift.working_hours

        if extra_hours > 0:
            concept = Concept(description="Horas extra")
            employee_hours = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                check_count=len(daily_events),
                notes=f"El empleado completó su jornada laboral y realizó {worked_hours_difference - employee.shift.working_hours} horas extra",
                register_type=RegisterType.PRESENCIA,
                first_check_in=first_check,
                last_check_out=last_check,
                time_worked=time(hour=worked_hours_difference, minute=0, second=0),
                work_date=day,
                extra_hours=time(hour=int(extra_hours), minute=0, second=0),
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hours)

        elif extra_hours < 0:
            concept = Concept(description="Horas faltantes")
            employee_hours = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                check_count=len(daily_events),
                notes=f"El empleado no completó su jornada laboral, le faltaron {abs(extra_hours)} horas",
                register_type=RegisterType.PRESENCIA,
                first_check_in=first_check,
                last_check_out=last_check,
                time_worked=time(hour=worked_hours_difference, minute=0, second=0),
                work_date=day,
                extra_hours=time(hour=abs(int(extra_hours)), minute=0, second=0),
                pay=False,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hours)

        else:
            concept = Concept(description="Jornada laboral completa")
            employee_hours = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                check_count=len(daily_events),
                notes="El empleado completó su jornada laboral",
                register_type=RegisterType.PRESENCIA,
                first_check_in=first_check,
                last_check_out=last_check,
                time_worked=time(hour=worked_hours_difference, minute=0, second=0),
                work_date=day,
                extra_hours=time(hour=0, minute=0, second=0),
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hours)

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

    for eh, concept in zip(employee_hours_to_add, concepts_to_add):
        payroll_response = PayrollResponse(
            employee_hours=EmployeeHoursSchema.model_validate(eh),
            concept=ConceptSchema.model_validate(concept),
            shift=ShiftSchema.model_validate(employee.shift),
        )
        response.append(payroll_response)

    return response


def log_employee_absence(
    employee: Employee,
    concepts_to_add: list[Concept],
    employee_hours_to_add: list[EmployeeHours],
    work_date: date,
    first_check: time | None,
    last_check: time | None,
    check_count: int,
):
    concept = Concept(description="Ausencia injustificada")
    employee_hours = EmployeeHours(
        employee_id=employee.id,
        concept_id=concept.id,
        shift_id=employee.shift.id,
        check_count=check_count,
        notes="El empleado no registró su entrada ni salida",
        register_type=RegisterType.AUSENCIA,
        first_check_in=first_check,
        last_check_out=last_check,
        time_worked=None,
        work_date=work_date,
        extra_hours=None,
        pay=False,
    )
    concepts_to_add.append(concept)
    employee_hours_to_add.append(employee_hours)
