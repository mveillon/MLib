from src import frange
import numpy as np

def test_frange():
    f = list(frange(10))
    assert np.allclose(f, list(range(10))), f
    f = list(frange(0, 1, 0.1))
    assert np.allclose(f, [ i / 10 for i in range(10) ]), f
    f = list(frange(-5, 5, 0.5))
    assert np.allclose(f, [ i / 2 for i in range(-10, 10) ]), f

    for i in range(1, 10):
        assert len(frange(i)) == i

    assert len(frange(0, 1, 0.1)) == 10
    assert len(frange(-5, 5, 0.5)) == 20
