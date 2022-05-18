from src import close_enough

def test_close_enough():
    assert close_enough(1, 1)
    assert close_enough(1, 1.000000000001)
    assert close_enough(3.999999999999, 4)
    assert not close_enough(4, 4.1)
    assert not close_enough(2, 1.8)
    assert close_enough(-2, -2)
    assert close_enough(-2.00000000001, -2)
    assert close_enough(-1.99999999999, -2)
    assert close_enough(0, 0.000001)
    assert close_enough(-0.00000001, 0)
    assert close_enough(0.000000000000000001, 0)
    assert close_enough(500000, 499999.9999)
    assert not close_enough(500000, 500001)
