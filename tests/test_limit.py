from src import limit, get_root, assign_return, close_enough, diff_quo, part_derivative
import math

def test_limit():
    for i in range(10):
        assert limit(lambda n: 2 * n + i, 0) == i
    assert limit(lambda n: 1 / n, float('inf')) == 0
    assert limit(lambda n: n, float('inf')) == float('inf')
    assert limit(lambda n: 1 / n, 0) == 0

def test_ar():
    lst = [ i for i in range(10) ]
    new_lst = assign_return(lst, 2, 10)
    assert new_lst[2] == 10
    assert lst[2] == 2, lst

def test_derivative():
    assert close_enough(diff_quo(lambda n: 2 * n + 4, 2), 2), diff_quo(lambda n: 2 * n + 4, 2)
    assert close_enough(diff_quo(lambda n: 3 * n ** 2, 3), 18)
    assert close_enough(part_derivative(lambda arr: 2 * arr[0] + 4, [2], 0), 2), part_derivative(lambda arr: 2 * arr[0] + 4, [2], 0)
    assert close_enough(part_derivative(lambda arr: 3 * arr[0] ** 2, [4], 0), 24)
    assert close_enough(part_derivative(lambda arr: 3 * arr[0] + 2 * arr[1], [1, 2], 1), 2)
    
def test_roots():
    assert math.fabs(get_root(lambda n: n ** 3, 2)) < 0.1, get_root(lambda n: n ** 3, 2)
    assert math.fabs(get_root(lambda n: (n - 2) ** 2, 1) - 2) < 0.1, get_root(lambda n: (n - 2) ** 2, 1)
