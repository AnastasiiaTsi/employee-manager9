from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from employee_manager.analytics import Employee, process_employee_scores

def process_scores_threads(employees: list[Employee], workers: int = 4) -> list[float]:
    with ThreadPoolExecutor(max_workers=workers) as executor:
        chunk_size = len(employees) // workers
        chunks = [employees[i:i + chunk_size] for i in range(0, len(employees), chunk_size)]
        results = executor.map(process_employee_scores, chunks)
        return [item for sublist in results for item in sublist]

def process_scores_processes(employees: list[Employee], workers: int = 4) -> list[float]:
    with ProcessPoolExecutor(max_workers=workers) as executor:
        chunk_size = len(employees) // workers
        chunks = [employees[i:i + chunk_size] for i in range(0, len(employees), chunk_size)]
        results = executor.map(process_employee_scores, chunks)
        return [item for sublist in results for item in sublist]