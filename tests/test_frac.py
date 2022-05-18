from src import frac, frac_to_float

def frac_to_float():
    assert frac_to_float('3 / 4') == 0.75
    assert frac_to_float('0 / 10') == 0
    assert frac_to_float('2 / 2') == 1
