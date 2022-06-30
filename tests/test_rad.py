from src import rad, sep_rad, rad_to_float
import math

def test_rad():
    assert rad(16) == '4', rad(16)
    assert rad(8) == '2√2', rad(8)
    assert rad(20) == '2√5', rad(20)
    assert rad(17) == '√17', rad(17)

def test_sep_rad():
    assert sep_rad('√35') == ['', '√35'], sep_rad('√35')
    assert sep_rad('1√') == ['1', '√']
    assert sep_rad('534√401') == ['534', '√401']

def test_rad_to_float():
    assert rad_to_float('√5') == math.sqrt(5)
    assert rad_to_float('3√10') == 3 * math.sqrt(10)
    assert rad_to_float('8√1') == 8
    assert rad_to_float('2 / 8√2') == 2 / (8 * math.sqrt(2))

