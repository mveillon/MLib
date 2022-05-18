from src import factors, slow_fac
from timeit import default_timer as timer
import numpy as np
import matplotlib.pyplot as plt

ENABLED = False

def test_slow_fac():
    for i in range(-1_000, 1_000):
        assert slow_fac(i) == factors(i)

def test_factors():
    assert factors(3) == {1, 3}, factors(3)
    assert factors(2) == {1, 2}, factors(2)
    assert factors(0) == set(), factors(0)
    assert factors(24) == {1, 2, 3, 4, 6, 8, 12, 24}, factors(24)
    assert factors(8) == {1, 2, 4, 8}, factors(8)
    assert factors(1) == {1}, factors(1)
    assert factors(17) == {1, 17}, factors(17)
    assert factors(-2) == {1, 2}, factors(-2)
    assert factors(-24) == {1, 2, 3, 4, 6, 8, 12, 24}, factors(-24)
    assert factors(-17) == {1, 17}, factors(-17)

def factoring_speeds():
    if ENABLED:
        to_factor = 10 ** 100 + 0xffff << 10
        r = lambda n: round(n / 60, 3)
        print(f'Starting factorization of {to_factor}...')
        start = timer()
        slows = slow_fac(to_factor)   
        print(f'slow method took {r(timer() - start)}')
        middle = timer()
        fasts = factors(to_factor)
        print(f'fast method took {r(timer() - middle())}')
        assert slows == fasts
        
        xs = np.array(range(100_000_000, 100_050_000, 2))
        slow_times = []
        fast_times = []
        for x in xs:
            start = timer()
            slows = slow_fac(x)
            slow_times.append(timer() - start)
            middle = timer()
            fasts = factors(x)
            fast_times.append(timer() - middle)
            assert fasts == slows

        plt.clf()
        plt.plot(xs, slow_times, label = 'Without dividing')
        plt.plot(xs, fast_times, label = 'With dividing')
        plt.legend()
        plt.title('Comparing times of factoring algorithms')
        plt.xlabel('Input integer')
        plt.ylabel('Factoring time (seconds)')
        plt.show()
        slow_mean = sum(slow_times) / xs.shape[0]
        fast_mean = sum(fast_times) / xs.shape[0]
        avg_diff = slow_mean - fast_mean
        print(avg_diff, slow_mean, fast_mean)
        print(avg_diff / slow_mean, avg_diff / fast_mean)
