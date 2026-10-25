from pydantic import BaseModel, Field

class EmployeeCreate(BaseModel):
    name: str = Field(min_length=2, max_length=100)
    position: str = Field(min_length=2, max_length=100)
    salary: float = Field(ge=0)
    department_id: int = Field(gt=0)

class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)
    position: str | None = Field(default=None, min_length=2, max_length=100)
    salary: float | None = Field(default=None, ge=0)
    department_id: int | None = Field(default=None, gt=0)

class EmployeeResponse(BaseModel):
    id: int
    name: str
    position: str
    salary: float
    department_id: int
    model_config = {"from_attributes": True}

class DepartmentStatistics(BaseModel):
    department_id: int
    employees_count: int
    average_salary: float
    max_salary: float
    total_payroll: float