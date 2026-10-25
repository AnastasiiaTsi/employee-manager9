import pytest
from employee_manager.models import Employee
from employee_manager.repositories import DepartmentRepository, EmployeeRepository
from employee_manager.services import EmployeeService, transfer_employees

def test_add_employee(session):
    dept = DepartmentRepository(session).add("IT")
    repo = EmployeeRepository(session)
    emp = Employee(name="Anna", position="Dev", salary=25000, department_id=dept.id)
    saved = repo.add(emp)
    assert saved.id is not None
    assert saved.name == "Anna"

def test_update_salary(session):
    dept = DepartmentRepository(session).add("IT")
    repo = EmployeeRepository(session)
    emp = repo.add(Employee(name="Anna", position="Dev", salary=25000, department_id=dept.id))
    updated = repo.update_salary(emp.id, 30000)
    assert updated is not None
    assert updated.salary == 30000

def test_delete_employee(session):
    dept = DepartmentRepository(session).add("IT")
    repo = EmployeeRepository(session)
    emp = repo.add(Employee(name="Anna", position="Dev", salary=25000, department_id=dept.id))
    assert repo.delete(emp.id) is True
    assert repo.get_by_id(emp.id) is None

def test_salary_aggregates(session):
    dept = DepartmentRepository(session).add("IT")
    repo = EmployeeRepository(session)
    repo.add(Employee(name="A", position="Dev", salary=100, department_id=dept.id))
    repo.add(Employee(name="B", position="Dev", salary=200, department_id=dept.id))
    
    service = EmployeeService(session)
    stats = service.get_department_statistics(dept.id)
    assert stats is not None
    assert stats.average_salary == 150.0
    assert stats.max_salary == 200.0
    assert stats.total_payroll == 300.0

def test_transfer_rollback(session):
    dept1 = DepartmentRepository(session).add("IT")
    dept2 = DepartmentRepository(session).add("HR")
    repo = EmployeeRepository(session)
    emp = repo.add(Employee(name="A", position="Dev", salary=100, department_id=dept1.id))
    
    with pytest.raises(ValueError):
        transfer_employees(session, [emp.id, 999], dept2.id)
        
    session.refresh(emp)
    assert emp.department_id == dept1.id