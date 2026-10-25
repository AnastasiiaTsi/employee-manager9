from sqlalchemy import func, select
from sqlalchemy.orm import Session
from employee_manager.models import Employee, Department
from employee_manager.schemas import DepartmentStatistics

class EmployeeService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_department_statistics(self, department_id: int) -> DepartmentStatistics | None:
        dept = self.session.get(Department, department_id)
        if dept is None:
            return None
        statement = select(
            func.count(Employee.id),
            func.avg(Employee.salary),
            func.max(Employee.salary),
            func.sum(Employee.salary),
        ).where(Employee.department_id == department_id)
        count, avg, max_s, total = self.session.execute(statement).one()
        return DepartmentStatistics(
            department_id=department_id,
            employees_count=count or 0,
            average_salary=float(avg or 0.0),
            max_salary=float(max_s or 0.0),
            total_payroll=float(total or 0.0),
        )