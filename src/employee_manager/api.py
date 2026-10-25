from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session
from employee_manager.dependencies import get_session
from employee_manager.models import Employee
from employee_manager.repositories import EmployeeRepository
from employee_manager.schemas import (
    EmployeeCreate, EmployeeUpdate, EmployeeResponse, DepartmentStatistics
)
from employee_manager.services import EmployeeService
from employee_manager.external_api import fetch_statistics_batch

app = FastAPI(title="Employee Manager API", version="1.0.0")

@app.get("/employees", response_model=list[EmployeeResponse])
async def get_employees(
    department_id: int | None = None,
    session: Session = Depends(get_session),
) -> list[Employee]:
    repo = EmployeeRepository(session)
    if department_id is not None:
        return repo.find_by_department(department_id)
    return repo.get_all()

@app.get("/employees/{employee_id}", response_model=EmployeeResponse)
async def get_employee(employee_id: int, session: Session = Depends(get_session)):
    repo = EmployeeRepository(session)
    emp = repo.get_by_id(employee_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp

@app.post("/employees", response_model=EmployeeResponse, status_code=status.HTTP_201_CREATED)
async def create_employee(data: EmployeeCreate, session: Session = Depends(get_session)):
    repo = EmployeeRepository(session)
    emp = Employee(name=data.name, position=data.position, salary=data.salary, department_id=data.department_id)
    return repo.add(emp)

@app.patch("/employees/{employee_id}", response_model=EmployeeResponse)
async def update_employee(employee_id: int, data: EmployeeUpdate, session: Session = Depends(get_session)):
    repo = EmployeeRepository(session)
    emp = repo.get_by_id(employee_id)
    if emp is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    updates = data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(emp, field, value)
    session.commit()
    session.refresh(emp)
    return emp

@app.delete("/employees/{employee_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_employee(employee_id: int, session: Session = Depends(get_session)):
    repo = EmployeeRepository(session)
    if not repo.delete(employee_id):
        raise HTTPException(status_code=404, detail="Employee not found")

@app.get("/departments/{department_id}/employees", response_model=list[EmployeeResponse])
async def get_department_employees(department_id: int, session: Session = Depends(get_session)):
    repo = EmployeeRepository(session)
    return repo.find_by_department(department_id)

@app.get("/departments/{department_id}/statistics", response_model=DepartmentStatistics)
async def get_department_statistics(department_id: int, session: Session = Depends(get_session)):
    service = EmployeeService(session)
    stats = service.get_department_statistics(department_id)
    if stats is None:
        raise HTTPException(status_code=404, detail="Department not found")
    return stats

@app.post("/departments/batch-statistics", response_model=list[DepartmentStatistics])
async def batch_statistics(department_ids: list[int]):
    try:
        return await fetch_statistics_batch(department_ids)
    except Exception:
        raise HTTPException(status_code=504, detail="Batch operation timed out")