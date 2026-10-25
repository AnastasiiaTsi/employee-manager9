from sqlalchemy import select
from sqlalchemy.orm import Session
from employee_manager.models import Department, Employee

class DepartmentRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, name: str) -> Department:
        dept = Department(name=name)
        self.session.add(dept)
        self.session.commit()
        self.session.refresh(dept)
        return dept

    def get_by_id(self, dept_id: int) -> Department | None:
        return self.session.get(Department, dept_id)

    def get_all(self) -> list[Department]:
        return list(self.session.scalars(select(Department)))

class EmployeeRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, employee: Employee) -> Employee:
        self.session.add(employee)
        self.session.commit()
        self.session.refresh(employee)
        return employee

    def get_by_id(self, employee_id: int) -> Employee | None:
        return self.session.get(Employee, employee_id)

    def get_all(self) -> list[Employee]:
        return list(self.session.scalars(select(Employee)))

    def find_by_department(self, department_id: int) -> list[Employee]:
        statement = select(Employee).where(Employee.department_id == department_id)
        return list(self.session.scalars(statement))

    def delete(self, employee_id: int) -> bool:
        employee = self.get_by_id(employee_id)
        if employee is None:
            return False
        self.session.delete(employee)
        self.session.commit()
        return True