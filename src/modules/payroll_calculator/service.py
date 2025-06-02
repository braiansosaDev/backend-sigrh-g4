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
from sqlmodel import and_, delete, select


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


def get_hours_by_date_range(
    db: DatabaseSession, request: PayrollRequest
) -> list[PayrollResponse]:
    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be greater than start date",
        )
    employee = get_employee_by_id(db, request.employee_id)
    filtered_hours = filter_and_sort_hours(
        employee.employee_hours, request.start_date, request.end_date
    )
    return [
        PayrollResponse(
            employee_hours=EmployeeHoursSchema.model_validate(eh),
            concept=ConceptSchema.model_validate(eh.concept),  # type: ignore
            shift=ShiftSchema.model_validate(employee.shift),
        )
        for eh in filtered_hours
    ]


def filter_and_sort_hours(
    employee_hours: list[EmployeeHours], start_date: date, end_date: date
):
    # Compara solo fechas, no datetime
    return sorted(
        (eh for eh in employee_hours if start_date <= eh.work_date <= end_date),
        key=lambda eh: eh.work_date,
    )


def calculate_hours(db: DatabaseSession, request: PayrollRequest):
    if request.end_date < request.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be greater than start date",
        )
    employee = get_employee_by_id(db, request.employee_id)
    
    sorted_events: list[ClockEvents] = []

    date_range = get_date_range(request.start_date, request.end_date)
    sorted_events = filter_and_sort_clock_events(
        employee.clock_events,
        request.start_date,
        request.end_date,
    )
    
    events_by_day: dict[date, list[ClockEvents]] = defaultdict(list)

    # 1) Agrupar eventos por día
    for event in sorted_events:
        event_day = date(
            event.event_date.year, event.event_date.month, event.event_date.day
        )
        events_by_day[event_day].append(event)
    try:   
        if employee.shift.type != "Nocturno":
            # 2) Para cada día hábil, procesar según tenga o no eventos
            process_daily_hours(
                db, employee, date_range, events_by_day
            )
        else:
            process_night_hours(
                db, employee, date_range, events_by_day
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing hours: {str(e)}",
        )


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

        # CASO 1.1 – No hubo IN el día anterior, y hoy solo hay un IN suelto → ausencia
        if (
            not any(ev.event_type == ClockEventTypes.IN for ev in yesterday_events)
            and first_event_today
            and first_event_today.event_type == ClockEventTypes.IN
            and not any(ev.event_type == ClockEventTypes.OUT for ev in today_events)
        ):
            concept = Concept(
                description="Ausencia en turno nocturno (entrada inválida)"
            )
            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                register_type=RegisterType.AUSENCIA,
                notes="Entrada aislada sin continuidad de turno nocturno.",
                check_count=1,
                sumary_time=time(0, 0, 0),
                pay=False,
            )
            concepts_to_add.append(concept)
            employee_hours_to_add.append(employee_hour)
            continue  # cortamos aquí para no entrar en los casos normales

        # CASO 2 – Olvidó hacer salida (último evento ayer fue IN, pero hoy no hay OUT)
        elif (
            last_event_yesterday
            and last_event_yesterday.event_type == ClockEventTypes.IN
            and not any(ev.event_type == ClockEventTypes.OUT for ev in today_events)
        ):
            concept = Concept(description="Presente sin salida")
            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                first_check_in=last_event_yesterday.event_date.time(),
                register_type=RegisterType.PRESENCIA,
                notes="Entrada registrada el día anterior pero falta salida.",
                check_count=1,
                sumary_time=time(int(employee.shift.working_hours), 0, 0),
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
            concept = Concept(description="Olvido de salida nocturna")
            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                register_type=RegisterType.PRESENCIA,
                first_check_in=last_event_yesterday.event_date.time(),
                notes="Entrada el día anterior y nueva entrada hoy, sin salida intermedia.",
                check_count=2,
                sumary_time=time(int(employee.shift.working_hours), 0, 0),
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
            check_in = last_event_yesterday.event_date
            check_out = first_event_today.event_date
            duration = check_out - check_in

            total_seconds = int(duration.total_seconds())
            hours = total_seconds // 3600
            minutes = (total_seconds % 3600) // 60
            seconds = total_seconds % 60

            summary_time = time(hour=hours, minute=minutes, second=seconds)

            # Comparar con la jornada laboral esperada
            worked_hours = hours + (minutes / 60)
            expected_hours = employee.shift.working_hours
            extra_hours_float = worked_hours - expected_hours

            # Cálculo de extra o faltante
            if extra_hours_float > 0:
                extra_h = int(extra_hours_float)
                extra_m = int((extra_hours_float - extra_h) * 60)
                extra_time = time(hour=extra_h, minute=extra_m, second=0)

                concept = Concept(description="Turno nocturno con horas extra")
                notes = f"Turno completo con {extra_h}h {extra_m}m extra."
            elif extra_hours_float < 0:
                faltante_h = int(abs(extra_hours_float))
                faltante_m = int((abs(extra_hours_float) - faltante_h) * 60)
                extra_time = time(hour=faltante_h, minute=faltante_m, second=0)

                concept = Concept(description="Turno nocturno incompleto")
                notes = f"Turno incompleto. Faltaron {faltante_h}h {faltante_m}m."
            else:
                extra_time = time(0, 0, 0)
                concept = Concept(description="Turno nocturno completo")
                notes = "Turno completo según jornada esperada."

            employee_hour = EmployeeHours(
                employee_id=employee.id,
                concept_id=concept.id,
                shift_id=employee.shift.id,
                work_date=day,
                register_type=RegisterType.PRESENCIA,
                first_check_in=last_event_yesterday.event_date.time(),
                last_check_out=first_event_today.event_date.time(),
                notes=notes,
                check_count=2,
                sumary_time=summary_time,
                extra_hours=extra_time,
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
    db: DatabaseSession,
    employee: Employee,
    date_range: list[date],
    events_by_day: dict[date, list[ClockEvents]],
):
    for day in date_range:
        # Saltar sábados y domingos
        if day.weekday() in (5, 6):
            concept= check_concept(db, "Día no hábil.")
            create_employee_hours_if_not_exists(
                db=db, 
                employee=employee, 
                concept=concept.id, 
                day=day, 
                daily_events_count=0, 
                first_check_in=None, 
                last_check_out=None, 
                payroll_status="archived", 
                notes="Día no hábil", 
                sumary_time=None, 
                extra_hours=None,
                register_type=RegisterType.DIA_NO_HABIL,
            )
            continue

        daily_events = events_by_day.get(day, [])
        ins = [ev for ev in daily_events if ev.event_type == ClockEventTypes.IN]
        outs = [ev for ev in daily_events if ev.event_type == ClockEventTypes.OUT]

        # EL EMPLEADO NO REGISTRÓ UNA ENTRADA EN TODO EL DÍA
        if not ins:
            concept = check_concept(db, "Ausente sin entrada registrada")
            create_employee_hours_if_not_exists(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=0,
                first_check_in=None,
                last_check_out=None,
                payroll_status="not payable",
                notes="El empleado no registró entrada en el día.",
                sumary_time=None,
                extra_hours=None,
                register_type=RegisterType.AUSENCIA,
            )    
            continue

        first_check = min(ins, key=lambda ev: ev.event_date).event_date.time()

        # EL EMPLEADO NO REGISTRÓ SU SALIDA
        if len(ins) > len(outs):
            concept = check_concept(db, "Presente sin salida registrada")
            create_employee_hours_if_not_exists(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events),
                first_check_in=first_check,
                last_check_out=None,
                payroll_status="not payable",
                notes="El empleado registró entrada pero no salida.",
                sumary_time=None,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )
            continue

        last_check = max(outs, key=lambda ev: ev.event_date).event_date.time()

        check_in_dt = datetime.combine(day, first_check)
        check_out_dt = datetime.combine(day, last_check)

        # Cálculo de tiempo trabajado
        worked_duration = check_out_dt - check_in_dt
        total_seconds = int(worked_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) % 3600 // 60
        seconds = total_seconds % 60

        #  Duración de la jornada como time
        summary_time = time(hour=hours % 24, minute=minutes, second=seconds) if hours < 24 else None

        #  Cálculo en formato decimal para validar rango
        worked_hours_float = hours + (minutes / 60)

        #  Lógica de validación según rango 7:30 - 8:30
        lower_bound = 7.5  # 7h30m
        upper_bound = 8.5  # 8h30m

        if lower_bound <= worked_hours_float <= upper_bound:
            # JORNADA COMPLETA
            concept= check_concept(db, "Jornada laboral completa")
            create_employee_hours_if_not_exists(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="payable",
                notes="El empleado completó su jornada laboral.",
                sumary_time=summary_time,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )

        elif worked_hours_float < lower_bound:
            # HORAS FALTANTES
            faltante_hours = int(lower_bound - worked_hours_float)
            faltante_minutes = int((lower_bound - worked_hours_float - faltante_hours) * 60)

            concept = check_concept(db, "Tiempo faltante")
            create_employee_hours_if_not_exists(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="not payable",
                notes=f"Le faltaron {faltante_hours}h {faltante_minutes}m para completar la jornada",
                sumary_time=summary_time,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )

        else:
            # HORAS EXTRA
            extra_hours = int(worked_hours_float - 8.0)
            extra_minutes = int((worked_hours_float - 8.0 - extra_hours) * 60)
            extra_time = time(hour=extra_hours, minute=extra_minutes, second=0)

            concept = check_concept(db, "Jornada laboral completa")
            create_employee_hours_if_not_exists(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="payable",
                notes=f"El empleado completó su jornada laboral.",
                sumary_time=time(hour=8),
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )

            concept = check_concept(db, "Horas extra")
            create_employee_hours_if_not_exists(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="pending validation",
                notes=f"El empleado realizó {extra_hours}h {extra_minutes}m extra",
                sumary_time=None,
                extra_hours=extra_time,
                register_type=RegisterType.PRESENCIA,
            )

def check_concept(db: DatabaseSession, concept_description: str) -> Concept:
    # Buscar si existe
    concept = db.exec(
        select(Concept).where(Concept.description == concept_description)
    ).one_or_none()
    
    # Si no existe, crear
    if not concept:
        new_concept = Concept(description=concept_description)
        db.add(new_concept)
        db.commit()
        db.refresh(new_concept)  # Refresca para tener el ID generado
        return new_concept

    return concept

def create_employee_hours_if_not_exists(
    db: DatabaseSession,
    employee: Employee,
    concept: id,
    day: date,
    daily_events_count: int | None,
    first_check_in: time | None,
    last_check_out: time | None,
    payroll_status: str,
    notes: str,
    sumary_time: time | None,
    extra_hours: time | None,
    register_type: RegisterType,
):
    # Buscar si existe
    # existing_employee_hours = db.exec(
    #     select(EmployeeHours)
    #     .where(
    #         EmployeeHours.employee_id == employee.id,
    #         EmployeeHours.work_date == day,
    #         EmployeeHours.payroll_status == "archived"
    #     )
    # ).one_or_none()
    existing_employee_hours = db.exec(
        select(EmployeeHours)
        .where(
            EmployeeHours.employee_id == employee.id,
            EmployeeHours.work_date == day,
        )
    ).one_or_none()

    if existing_employee_hours:
        return existing_employee_hours

    # Crear nuevo
    employee_hours = EmployeeHours(
        employee_id=employee.id,
        concept_id=concept,
        shift_id=employee.shift.id,
        check_count=daily_events_count,
        work_date=day,
        register_type=register_type,
        first_check_in=first_check_in,
        last_check_out=last_check_out,
        sumary_time=sumary_time,
        extra_hours=extra_hours,
        payroll_status=payroll_status,  # acá le pasas 'archived', 'payable', etc
        notes=notes,
    )

    db.add(employee_hours)
    db.commit()
    db.refresh(employee_hours)
