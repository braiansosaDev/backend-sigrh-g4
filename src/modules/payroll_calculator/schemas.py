from datetime import date
from pydantic import BaseModel
from src.modules.concept.models.models import Concept
from src.modules.employee_hours.models.models import EmployeeHours
from src.modules.shift.models.models import Shift


class PayrollRequest(BaseModel):
    employee_id: int
    start_date: date
    end_date: date


class PayrollResponse(BaseModel):
    employee_hours: EmployeeHours
    concept: Concept
    shift: Shift
