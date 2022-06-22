from src import rolling_average
import numpy as np

def test_rolling():
    x = np.full(100, 5)
    assert np.allclose(rolling_average(x), x)
    x = np.fromiter(range(100), count = 100, dtype = int)
    assert np.allclose(rolling_average(x, n_buckets = 1), x)
    y = np.array([0] + [ i + 0.5 for i in range(x.shape[0] - 1) ])
    assert np.allclose(rolling_average(x, n_buckets = 2), y)
