import pytest
from employee_manager.analytics import generate_employees, calculate_statistics_python, process_employee_scores
from employee_manager.numpy_analytics import calculate_statistics_numpy
from employee_manager.parallel import process_scores_processes, process_scores_threads

@pytest.fixture
def sample_data():
    return generate_employees(1000)

def test_numpy_statistics(sample_data):
    py_res = calculate_statistics_python(sample_data)
    np_res = calculate_statistics_numpy(sample_data)
    assert np_res["average_salary"] == pytest.approx(py_res["average_salary"])
    assert np_res["max_salary"] == pytest.approx(py_res["max_salary"])
    assert np_res["total_payroll"] == pytest.approx(py_res["total_payroll"])

def test_process_pool_results(sample_data):
    seq_res = process_employee_scores(sample_data)
    proc_res = process_scores_processes(sample_data, workers=2)
    assert len(seq_res) == len(proc_res)
    for a, b in zip(seq_res, proc_res):
        assert a == pytest.approx(b)

def test_thread_pool_results(sample_data):
    seq_res = process_employee_scores(sample_data)
    thr_res = process_scores_threads(sample_data, workers=2)
    assert len(seq_res) == len(thr_res)
    for a, b in zip(seq_res, thr_res):
        assert a == pytest.approx(b)