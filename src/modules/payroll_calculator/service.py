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

    if employee.shift.type != "Nocturno":
        # 2) Para cada día hábil, procesar según tenga o no eventos
        process_daily_hours(
            employee, date_range, concepts_to_add, employee_hours_to_add, events_by_day
        )
    else:
        process_night_hours(
            employee, date_range, concepts_to_add, employee_hours_to_add, events_by_day
        )

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


def process_night_hours(
    employee: Employee,
    date_range: list[date],
    concepts_to_add: list[Concept],
    employee_hours_to_add: list[EmployeeHours],
    events_by_day: dict[date, list[ClockEvents]],
):
    for day in date_range:
        if day.weekday() == 6:  # domingo
            continue

        yesterday = day - timedelta(days=1)
        yesterday_events = sorted(
            events_by_day.get(yesterday, []), key=lambda ev: ev.event_date
        )
        today_events = sorted(events_by_day.get(day, []), key=lambda ev: ev.event_date)

        # Último evento del día anterior
        last_event_yesterday = yesterday_events[-1] if yesterday_events else None
        # Primer evento del día actual
        first_event_today = today_events[0] if today_events else None

        # CASO 1 – Ausencia total (no IN el día anterior y no OUT hoy)
        if (
            not last_event_yesterday
            or last_event_yesterday.event_type != ClockEventTypes.IN
        ) and not first_event_today:
            print(f"{day} → NO ME PRESENTÉ A LABURAR")

            concept = Concept(description="Ausencia en turno nocturno")
            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                register_type=RegisterType.AUSENCIA,
                notes="No se registró ni entrada ni salida del turno nocturno.",
                check_count=0,
                sumary_time=time(0, 0, 0),
                pay=False,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hour)

        # CASO 2 – Olvidó hacer salida (último evento ayer fue IN, pero hoy no hay OUT)
        elif (
            last_event_yesterday
            and last_event_yesterday.event_type == ClockEventTypes.IN
            and not any(ev.event_type == ClockEventTypes.OUT for ev in today_events)
        ):
            print(f"{day} → ME OLVIDÉ DE REGISTRAR SALIDA")

            concept = Concept(description="Presente sin salida")
            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                register_type=RegisterType.PRESENCIA,
                notes="Entrada registrada el día anterior pero falta salida.",
                check_count=1,
                sumary_time=time(0, 0, 0),
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hour)

        # CASO 3 – Doble entrada (IN ayer y primer evento hoy también es IN)
        elif (
            last_event_yesterday
            and last_event_yesterday.event_type == ClockEventTypes.IN
            and first_event_today
            and first_event_today.event_type == ClockEventTypes.IN
        ):
            print(f"{day} → ME OLVIDÉ DE SALIR Y VOLVÍ A ENTRAR")

            concept = Concept(description="Olvido de salida nocturna")
            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                register_type=RegisterType.PRESENCIA,
                notes="Entrada el día anterior y nueva entrada hoy, sin salida intermedia.",
                check_count=2,
                sumary_time=time(0, 0, 0),
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hour)

        # CASO 4 – IN ayer + OUT hoy → jornada válida
        elif (
            last_event_yesterday
            and last_event_yesterday.event_type == ClockEventTypes.IN
            and first_event_today
            and first_event_today.event_type == ClockEventTypes.OUT
        ):
            print(f"{day} → JORNADA COMPLETA CON ENTRADA Y SALIDA")

            check_in = last_event_yesterday.event_date
            check_out = first_event_today.event_date
            duration = check_out - check_in

            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            summary_time = time(hour=hours, minute=minutes, second=seconds)

            concept = Concept(description="Turno nocturno trabajado")
            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                register_type=RegisterType.PRESENCIA,
                notes="Turno nocturno completo.",
                check_count=2,
                sumary_time=summary_time,
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hour)


def calculate_interval_time(
    events_list: list[ClockEvents],
    concepts_to_add: list[Concept],
    employee_hours_to_add: list[EmployeeHours],
    employee: Employee,
    day: date,
):
    if len(events_list) < 3:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Not enough events to calculate interval time",
        )

    total_duration = timedelta()

    trimmed_events = events_list[1:-1]  # Excluye el primer y último evento

    i = 0
    while i < len(trimmed_events) - 1:
        current_event = trimmed_events[i]
        next_event = trimmed_events[i + 1]

        if (
            current_event.event_type == ClockEventTypes.OUT
            and next_event.event_type == ClockEventTypes.IN
        ):
            interval = next_event.event_date - current_event.event_date
            total_duration += interval
            i += 2  # saltamos al siguiente par
        else:
            i += 1  # si no es un par válido, seguimos buscando

    total_seconds = int(total_duration.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = total_seconds % 60

    # Creamos el schema de respuesta
    concept = Concept(description="Tiempo de intervalos")
    employee_hour = EmployeeHours(
        employee_id=employee.id,
        concept_id=concept.id,
        shift_id=employee.shift.id,
        check_count=len(events_list),
        notes="Tiempo de intervalos",
        register_type=RegisterType.PRESENCIA,
        first_check_in=None,
        last_check_out=None,
        sumary_time=time(hour=hours, minute=minutes, second=seconds),
        work_date=day,
        extra_hours=None,
        pay=False,
    )

    concepts_to_add.append(concept)
    employee_hours_to_add.append(employee_hour)


def process_daily_hours(
    employee: Employee,
    date_range: list[date],
    concepts_to_add: list[Concept],
    employee_hours_to_add: list[EmployeeHours],
    events_by_day: dict[date, list[ClockEvents]],
):
    for day in date_range:
        # saltar sábados y domingos
        if day.weekday() in (5, 6):
            continue

        daily_events = events_by_day.get(day, [])
        ins = [ev for ev in daily_events if ev.event_type == ClockEventTypes.IN]
        outs = [ev for ev in daily_events if ev.event_type == ClockEventTypes.OUT]

        # EL EMPLEADO NO REGISTRÓ UNA ENTRADA EN TODO EL DIA
        if not ins:
            # No hay registros de entrada, registrar ausencia
            log_employee_absence(
                employee,
                concepts_to_add,
                employee_hours_to_add,
                day,
                None,
                None,
                0,
            )
            continue
        first_check = min(ins, key=lambda ev: ev.event_date).event_date.time()

        # EL EMPLEADO NO REGISTRÓ SU SALIDA
        if len(ins) > len(outs):
            concept = Concept(description="Presente sin salida registrada")
            employee_hours = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                check_count=len(daily_events),
                notes="Horario de salida no registrado",
                register_type=RegisterType.PRESENCIA,
                first_check_in=first_check,
                last_check_out=None,
                sumary_time=time(
                    hour=int(employee.shift.working_hours), minute=0, second=0
                ),
                work_date=day,
                extra_hours=None,
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hours)

        last_check = max(outs, key=lambda ev: ev.event_date).event_date.time()

        # seleccionar los ins y los outs que no sean el primero y el último
        first_check_hour = datetime.combine(day, first_check).hour
        last_check_hour = datetime.combine(day, last_check).hour
        worked_hours_difference = last_check_hour - first_check_hour
        extra_hours = worked_hours_difference - employee.shift.working_hours

        # EL EMPLEADO HIZO HORAS EXTRA
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
                sumary_time=time(hour=worked_hours_difference, minute=0, second=0),
                work_date=day,
                extra_hours=time(hour=int(extra_hours), minute=0, second=0),
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hours)

        # EL EMPLEADO NO COMPLETÓ SU JORNADA LABORAL
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
                sumary_time=time(hour=worked_hours_difference, minute=0, second=0),
                work_date=day,
                extra_hours=time(hour=abs(int(extra_hours)), minute=0, second=0),
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hours)

        # EL EMPLEADO COMPLETÓ SU JORNADA LABORAL
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
                sumary_time=time(hour=worked_hours_difference, minute=0, second=0),
                work_date=day,
                extra_hours=time(hour=0, minute=0, second=0),
                pay=True,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hours)

        calculate_interval_time(
            daily_events, concepts_to_add, employee_hours_to_add, employee, day
        )


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
        sumary_time=None,
        work_date=work_date,
        extra_hours=None,
        pay=False,
    )
    concepts_to_add.append(concept)
    employee_hours_to_add.append(employee_hours)
