import numpy as np
from employee_manager.analytics import Employee

def calculate_statistics_numpy(employees: list[Employee]) -> dict[str, float]:
    salaries = np.array([emp.salary for emp in employees], dtype=np.float64)
    
    return {
        "total_payroll": float(salaries.sum()),
        "average_salary": float(salaries.mean()),
        "max_salary": float(salaries.max())
    }