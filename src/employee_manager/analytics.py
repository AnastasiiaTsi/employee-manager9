import random
from dataclasses import dataclass

@dataclass
class Employee:
    id: int
    department: str
    salary: float

def generate_employees(count: int) -> list[Employee]:
    departments = ["IT", "HR", "Finance", "Sales", "Marketing"]
    return [
        Employee(
            id=i, 
            department=random.choice(departments), 
            salary=random.uniform(15000, 50000)
        )
        for i in range(count)
    ]

def calculate_statistics_python(employees: list[Employee]) -> dict[str, float]:
    total_payroll = 0.0
    max_salary = 0.0
    count = len(employees)
    
    for emp in employees:
        total_payroll += emp.salary
        if emp.salary > max_salary:
            max_salary = emp.salary
            
    return {
        "total_payroll": total_payroll,
        "average_salary": total_payroll / count if count else 0.0,
        "max_salary": max_salary
    }

def process_employee_scores(employees: list[Employee]) -> list[float]:
    results = []
    for emp in employees:
        val = emp.salary
        for _ in range(100):
            val = (val ** 2) % 12345.67
        results.append(val)
    return results