import cProfile
import pstats
import tracemalloc
from employee_manager.analytics import generate_employees, calculate_statistics_python

def run_profile() -> None:
    employees = generate_employees(100_000)
    
    profiler = cProfile.Profile()
    profiler.enable()
    calculate_statistics_python(employees)
    profiler.disable()
    
    stats = pstats.Stats(profiler).sort_stats('cumulative')
    stats.print_stats(5)
    
    tracemalloc.start()
    calculate_statistics_python(employees)
    current, peak = tracemalloc.get_traced_memory()
    print(f"\nPeak memory usage: {peak / 1024 / 1024:.2f} MB")
    tracemalloc.stop()

if __name__ == "__main__":
    run_profile()