from collections import defaultdict
from datetime import date, datetime, time, timedelta
from fastapi import HTTPException, status
from src.database.core import DatabaseSession
from src.modules.clock_events.models.models import ClockEvents
from src.modules.clock_events.schemas.schemas import ClockEventTypes
from src.modules.concept.models.models import Concept
from src.modules.employees.models.employee import Employee
from src.modules.employees.schemas.employee_models import EmployeeResponse
from src.modules.payroll_calculator.schemas import (
    ConceptSchema,
    EmployeeHoursSchema,
    PayrollPendingValidationResponse,
    PayrollRequest,
    PayrollResponse,
    ShiftSchema,
    PayrollPendingValidationRequest
)
from src.modules.employee_hours.models.models import EmployeeHours, RegisterType, payType
from sqlmodel import delete, select


def get_pending_validation_hours(
    db: DatabaseSession, request: PayrollPendingValidationRequest
) -> list[PayrollResponse]:
    if request.start_date and request.end_date and request.end_date < request.start_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="End date must be greater than start date",
        )

    query = select(EmployeeHours).where(EmployeeHours.payroll_status == "PENDING_VALIDATION")

    if request.employee_id:
        query = query.where(EmployeeHours.employee_id.in_(request.employee_id))

    if request.start_date:
        query = query.where(EmployeeHours.work_date >= request.start_date)
    if request.end_date:
        query = query.where(EmployeeHours.work_date <= request.end_date)

    employee_hours_list = db.exec(query).all()

    responses = []
    for eh in employee_hours_list:
        # Acá asumimos que las relaciones están disponibles vía foreign keys
        concept = db.get(Concept, eh.concept_id)
        employee = db.exec(
            select(Employee).where(Employee.id == eh.employee_id)
        ).one_or_none()

        if not employee or not employee.shift:
            continue  # o lanzá error si es crítico

        responses.append(PayrollPendingValidationResponse(
            employee=Employee.model_validate(employee),
            employee_hours=EmployeeHoursSchema.model_validate(eh),
            concept=ConceptSchema.model_validate(concept),
            shift=ShiftSchema.model_validate(employee.shift),
        ))
    return responses

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
        if employee.shift.type == "matutino":
            # 2) Para cada día hábil, procesar según tenga o no eventos
            process_morning_shift_hours(
                db, employee, date_range, events_by_day
            )
        elif employee.shift.type == "vespertino":
            process_afternoon_shift_hours(
                db, employee, date_range, events_by_day
            )
        else:
            process_night_shift_hours(
                db, employee, date_range, events_by_day
            )
            pass
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing hours: {str(e)}",
        )

def process_morning_shift_hours(
    db: DatabaseSession,
    employee: Employee,
    date_range: list[date],
    events_by_day: dict[date, list[ClockEvents]],
):
    for day in date_range:
        # Saltar sábados y domingos
        existing_employee_hours = db.exec(
        select(EmployeeHours)
        .where(
            EmployeeHours.employee_id == employee.id,
            EmployeeHours.work_date == day,
            EmployeeHours.payroll_status != 'archived'
        )).all()

        if existing_employee_hours:
            for eh in existing_employee_hours:
                db.delete(eh)
                db.commit()
                
        if day.weekday() in (5, 6):
            concept= check_concept(db, "Día no hábil.")
            create_employee_hours(
                db=db, 
                employee=employee, 
                concept=concept.id, 
                day=day, 
                daily_events_count=0, 
                first_check_in=None, 
                last_check_out=None, 
                payroll_status="not payable", 
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
            create_employee_hours(
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
            create_employee_hours(
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
            create_employee_hours(
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
            faltante_hours = int(8.0 - worked_hours_float)
            faltante_minutes = int((8.0 - worked_hours_float - faltante_hours) * 60)

            concept = check_concept(db, "Tiempo faltante")
            create_employee_hours(
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
            create_employee_hours(
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
            create_employee_hours(
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

def process_afternoon_shift_hours(
    db: DatabaseSession,
    employee: Employee,
    date_range: list[date],
    events_by_day: dict[date, list[ClockEvents]],
):
    for day in date_range:
        # Saltar sábados y domingos
        existing_employee_hours = db.exec(
        select(EmployeeHours)
        .where(
            EmployeeHours.employee_id == employee.id,
            EmployeeHours.work_date == day,
            EmployeeHours.payroll_status != 'archived'
        )).all()

        if existing_employee_hours:
            for eh in existing_employee_hours:
                db.delete(eh)
                db.commit()

        if day.weekday() in (5, 6):
            concept = check_concept(db, "Día no hábil.")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=0,
                first_check_in=None,
                last_check_out=None,
                payroll_status="not payable",
                notes="Día no hábil",
                sumary_time=None,
                extra_hours=None,
                register_type=RegisterType.DIA_NO_HABIL,
            )
            continue

        daily_events = events_by_day.get(day, [])
        next_day_events = events_by_day.get(day + timedelta(days=1), [])

        ins = [ev for ev in daily_events if ev.event_type == ClockEventTypes.IN]
        outs_today = [ev for ev in daily_events if ev.event_type == ClockEventTypes.OUT]
        outs_tomorrow = [ev for ev in next_day_events if ev.event_type == ClockEventTypes.OUT]
        outs = outs_today + outs_tomorrow

        if not ins:
            # No entrada
            concept = check_concept(db, "Ausente sin entrada registrada")
            create_employee_hours(
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

        if not outs:
            # No salida
            concept = check_concept(db, "Presente sin salida registrada")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=None,
                payroll_status="not payable",
                notes="El empleado registró entrada pero no salida.",
                sumary_time=None,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )
            continue

        outs_sorted = sorted(outs, key=lambda ev: ev.event_date)
        first_check_in_dt = datetime.combine(day, first_check)
        last_check_datetime = next(
            (ev.event_date for ev in outs_sorted if ev.event_date > first_check_in_dt),
            None
        )

        if not last_check_datetime:
            # No salida válida después del IN
            concept = check_concept(db, "Presente sin salida registrada")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=None,
                payroll_status="not payable",
                notes="El empleado registró entrada pero no salida.",
                sumary_time=None,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )
            continue

        last_check = last_check_datetime.time()

        check_in_dt = first_check_in_dt
        check_out_day = day if last_check_datetime.date() == day else day + timedelta(days=1)
        check_out_dt = datetime.combine(check_out_day, last_check)

        print(f"DEBUG -- Day: {day}, Check-in: {check_in_dt}, Check-out: {check_out_dt}")

        if check_out_dt <= check_in_dt:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Salida inválida: la salida ({check_out_dt}) es anterior o igual a la entrada ({check_in_dt})",
            )

        worked_duration = check_out_dt - check_in_dt
        total_seconds = int(worked_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) % 60
        seconds = total_seconds % 60

        if hours >= 24:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El empleado tiene {int(hours)}h trabajadas, excediendo el máximo permitido de 23h59m.",
            )

        summary_time = None
        if hours < 24:
            summary_time = time(hour=hours, minute=minutes, second=seconds)

        worked_hours_float = hours + (minutes / 60)

        lower_bound = 7.5  # 7h30m
        upper_bound = 8.5  # 8h30m

        if lower_bound <= worked_hours_float <= upper_bound:
            concept = check_concept(db, "Jornada laboral completa")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="payable",
                notes="El empleado completó su jornada laboral.",
                sumary_time=summary_time,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )
        elif worked_hours_float < lower_bound:
            faltante_hours = int(8.0 - worked_hours_float)
            faltante_minutes = int((8.0 - worked_hours_float - faltante_hours) * 60)
            concept = check_concept(db, "Tiempo faltante")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="not payable",
                notes=f"Le faltaron {faltante_hours}h {faltante_minutes}m para completar la jornada",
                sumary_time=summary_time,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )
        else:
            # Horas extra
            extra_seconds = total_seconds - (8 * 3600)
            extra_hours = extra_seconds // 3600
            extra_minutes = (extra_seconds % 3600) // 60

            if extra_hours >= 24:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"El empleado tiene {int(extra_hours)}h trabajadas, excediendo el máximo permitido de 23h59m.",
                )

            extra_time = time(hour=int(extra_hours), minute=int(extra_minutes), second=0)

            concept = check_concept(db, "Jornada laboral completa")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="payable",
                notes="El empleado completó su jornada laboral.",
                sumary_time=time(hour=8),
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )

            concept = check_concept(db, "Horas extra")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="pending validation",
                notes=f"El empleado realizó {int(extra_hours)}h {int(extra_minutes)}m extra",
                sumary_time=None,
                extra_hours=extra_time,
                register_type=RegisterType.PRESENCIA,
            )

def process_night_shift_hours(
    db: DatabaseSession,
    employee: Employee,
    date_range: list[date],
    events_by_day: dict[date, list[ClockEvents]],
):
    for day in date_range:
        # Saltar sábados y domingos (día de ingreso)
        existing_employee_hours = db.exec(
        select(EmployeeHours)
        .where(
            EmployeeHours.employee_id == employee.id,
            EmployeeHours.work_date == day,
            EmployeeHours.payroll_status != 'archived'
        )).all()

        if existing_employee_hours:
            for eh in existing_employee_hours:
                db.delete(eh)
                db.commit()

        if day.weekday() in (5, 6):
            concept = check_concept(db, "Día no hábil.")
            create_employee_hours(
                db=db, 
                employee=employee, 
                concept=concept.id, 
                day=day, 
                daily_events_count=0, 
                first_check_in=None, 
                last_check_out=None, 
                payroll_status="not payable", 
                notes="Día no hábil", 
                sumary_time=None, 
                extra_hours=None,
                register_type=RegisterType.DIA_NO_HABIL,
            )
            continue
        
        # Fichadas del día de ingreso
        daily_events = events_by_day.get(day, [])
        # Fichadas del día siguiente
        next_day_events = events_by_day.get(day + timedelta(days=1), [])
        
        # Juntar eventos de entrada (día actual) y salida (día siguiente)
        ins = [ev for ev in daily_events if ev.event_type == ClockEventTypes.IN]
        outs = [ev for ev in next_day_events if ev.event_type == ClockEventTypes.OUT]

        if not ins:
            # No entrada
            concept = check_concept(db, "Ausente sin entrada registrada")
            create_employee_hours(
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

        if not outs:
            # No salida
            concept = check_concept(db, "Presente sin salida registrada")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
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
        
        # Construir datetime combinando día y hora
        check_in_dt = datetime.combine(day, first_check)
        check_out_dt = datetime.combine(day + timedelta(days=1), last_check)

        worked_duration = check_out_dt - check_in_dt
        total_seconds = int(worked_duration.total_seconds())
        hours = total_seconds // 3600
        minutes = (total_seconds % 3600) % 3600 // 60
        seconds = total_seconds % 60

        summary_time = time(hour=hours % 24, minute=minutes, second=seconds) if hours < 24 else None
        worked_hours_float = hours + (minutes / 60)

        lower_bound = 7.5  # 7h30m
        upper_bound = 8.5  # 8h30m

        if lower_bound <= worked_hours_float <= upper_bound:
            concept = check_concept(db, "Jornada laboral completa")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="payable",
                notes="El empleado completó su jornada laboral.",
                sumary_time=summary_time,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )
        elif worked_hours_float < lower_bound:
            faltante_hours = int(8.0 - worked_hours_float)
            faltante_minutes = int((8.0 - worked_hours_float - faltante_hours) * 60)
            concept = check_concept(db, "Tiempo faltante")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="not payable",
                notes=f"Le faltaron {faltante_hours}h {faltante_minutes}m para completar la jornada",
                sumary_time=summary_time,
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )
        else:
            extra_hours = int(worked_hours_float - 8.0)
            extra_minutes = int((worked_hours_float - 8.0 - extra_hours) * 60)
            extra_time = time(hour=extra_hours, minute=extra_minutes, second=0)

            concept = check_concept(db, "Jornada laboral completa")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
                first_check_in=first_check,
                last_check_out=last_check,
                payroll_status="payable",
                notes="El empleado completó su jornada laboral.",
                sumary_time=time(hour=8),
                extra_hours=None,
                register_type=RegisterType.PRESENCIA,
            )

            concept = check_concept(db, "Horas extra")
            create_employee_hours(
                db=db,
                employee=employee,
                concept=concept.id,
                day=day,
                daily_events_count=len(daily_events) + len(next_day_events),
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

def create_employee_hours(
    db: DatabaseSession,
    employee: Employee,
    concept: int,
    day: date,
    daily_events_count: int,
    first_check_in: time | None,
    last_check_out: time | None,
    payroll_status: str,
    notes: str,
    sumary_time: time | None,
    extra_hours: time | None,
    register_type: RegisterType,
):
        
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
        payroll_status=payType(payroll_status),  # acá le pasas 'archived', 'payable', etc
        notes=notes,
    )

    db.add(employee_hours)
    db.commit()
    db.refresh(employee_hours)
