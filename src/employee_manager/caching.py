from functools import lru_cache
from employee_manager.analytics import Employee

@lru_cache(maxsize=128)
def get_department_statistics(employees_tuple: tuple, department: str) -> float:
    total = 0.0
    count = 0
    for emp in employees_tuple:
        if emp.department == department:
            total += emp.salary
            count += 1
    return total / count if count else 0.0

def invalidate_cache() -> None:
    get_department_statistics.cache_clear()