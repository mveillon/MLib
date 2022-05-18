from src import can_be_int

def test_can_be_int():
    assert can_be_int(2)
    assert can_be_int('2')
    assert not can_be_int('a')
    assert not can_be_int('')
    assert not can_be_int('1a')
    assert can_be_int(2.0)
    assert not can_be_int(2.1)
