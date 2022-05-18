from src import Fraction, close_enough, gcd, lcm, divide

CHECK_STRS = False

def test_divide():
    frac = Fraction
    assert divide(1, 2) == frac(1, 2)
    assert divide(2, 2) == 1
    assert divide(4, 2) == 2
    assert divide(24, 1) == 24
    assert divide(24, 5) == frac(24, 5)
    assert divide(3, 12) == frac(1, 4)

def test_frac():
    frac = Fraction
    f = frac(1, 2)
    assert f == frac(1, 2)
    assert f == frac(2, 4)
    assert f != frac(1, 3)
    f2 = frac(2, 3)
    assert f2 == frac(4, 6)
    assert f2 != frac(3, 2)
    assert f + frac(2, 2) == frac(3, 2)
    assert f + 1 == frac(3, 2)
    assert 1 + f == frac(3, 2)
    assert f + 0.5 == 1.0
    assert f + f2 == frac(7, 6)
    assert f + f == 1
    assert f + 3 * f == 2
    assert f - frac(2, 2) == frac(-1, 2)
    assert f - 1 == frac(-1, 2)
    assert 1 - f == f
    assert f - 0.5 == 0.0
    assert f - f2 == frac(-1, 6)
    assert f - f == 0
    assert f - 3 * f == -1
    assert f * 2 == 1
    assert 2 * f == 1
    assert f * frac(1, 2) == frac(1, 4)
    assert f * 0.5 == 0.25
    assert f * f2 == frac(1, 3)
    assert f / 2 == frac(1, 4)
    assert 2 / f == 4
    assert f / 0.5 == 1.0
    assert f / f2 == frac(3, 4)
    assert int(f) == 0
    assert f / f == 1
    assert int(f2) == 0
    assert int(frac(3, 2)) == 1
    assert float(f) == 0.5
    assert close_enough(float(f2), 0.6666666)
    assert f == 0.5
    assert not f == 0.51
    assert not f == 1
    assert not f == 0
    assert 0.5 == f
    assert not 1 == f
    assert '1' in str(f)
    assert '2' in str(f)
    assert '2' in str(f2)
    assert '3' in str(f2)
    assert f < f2
    assert f < 1
    assert f != f2
    assert f != 0
    assert f != 1
    assert f2 > f
    assert 1 > f
    assert f > 0
    assert f <= f2
    assert f2 >= f
    assert f <= Fraction(1, 2)
    assert f2 <= Fraction(2, 3)
    assert f >= Fraction(1, 2)
    assert f2 >= Fraction(2, 3)
    assert not f < f
    assert not f > f
    assert not f2 < f2
    assert not f2 > f2
    assert not f > 1
    assert not f < 0
    assert Fraction(2, 1) == 2
    assert Fraction(6, 3) == 2
    assert isinstance(Fraction(6, 3), int)
    assert not isinstance(Fraction(7, 3), int)

def test_strs():
    if CHECK_STRS:
        frac = Fraction
        f = frac(1, 2)
        f2 = frac(2, 3)
        print()
        print(str(f))
        print(str(f2))
        print(str(frac(12, 1)))
        print(str(frac(1, 12)))
        print(str(frac(10000, 3)))
        print(str(frac(3, 10000)))

def test_gcd():
    assert gcd(2, 2) == 2
    assert gcd(2, 4) == 2
    assert gcd(3, 6) == 3
    assert gcd(24, 36) == 12
    assert gcd(40, 50) == 10
    assert gcd(4, 2) == 2
    assert gcd(6, 3) == 3
    assert gcd(36, 24) == 12
    assert gcd(50, 40) == 10
    for i in range(1, 20):
        for j in range(1, 20):
            assert gcd(i, j) == gcd(j, i)

def test_lcm():
    assert lcm(1, 2) == 2
    assert lcm(4, 3) == 12
    assert lcm(3, 4) == 12
    assert lcm(2, 1) == 2
    assert lcm(6, 9) == 18
    assert lcm(9, 6) == 18
    for i in range(1, 20):
        for j in range(1, 20):
            assert lcm(i, j) == lcm(j, i)
