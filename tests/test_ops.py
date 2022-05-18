from src import add_n, sub_n, mult_n, div_n, n_div, n_sub, floordiv_n, n_floordiv, exp_n, n_exp, chain
from src import sine, cosine, tangent, arctangent, arccosine, arcsine, identity, log_of_n, log_base_n
from src import lt_n, le_n, gt_n, ge_n, get_n, set_n_to_val, derivative, parse_expr
from src import f_plus_g, f_minus_g, f_times_g, f_divided_by_g, mx_plus_b, const, f_raised_to_g
from math import log, sin, cos, tan, asin, acos, atan, sqrt
import numpy as np
from .test_parser import _similar_func

_ITERS = 10
_TEST_STRS = False

def test_math_ops():
    for i in range(_ITERS):
        adder = add_n(i)
        assert _similar_func(adder, lambda x: x + i)
        assert _similar_func(adder.f_prime(), lambda x: 1)

    for i in range(_ITERS):
        subber0 = sub_n(i)
        subber1 = n_sub(i)
        assert _similar_func(subber0, lambda x: x - i)
        assert _similar_func(subber0.f_prime(), lambda x: 1)
        assert _similar_func(subber1, lambda x: i - x)
        assert _similar_func(subber1.f_prime(), lambda x: -1)

    for i in range(_ITERS):
        multer = mult_n(i)
        assert _similar_func(multer, lambda x: x * i)
        assert _similar_func(multer.f_prime(), lambda x: i)

    for i in range(1, _ITERS + 1):
        div0 = div_n(i)
        div1 = n_div(i)
        fdiv0 = floordiv_n(i)
        fdiv1 = n_floordiv(i)
        assert _similar_func(div0, lambda x: x / i)
        assert _similar_func(div0.f_prime(), lambda x: 1 / i)
        assert _similar_func(div1, lambda x: i / x)
        assert _similar_func(div1.f_prime(), lambda x: -i / x ** 2)
        assert _similar_func(fdiv0, lambda x: x // i), (str(fdiv0), i)
        assert _similar_func(fdiv0.f_prime(), lambda x: 0)
        assert _similar_func(fdiv1, lambda x: i // x)
        assert _similar_func(fdiv1.f_prime(), lambda x: 0)

    for i in range(1, _ITERS + 1):
        exp0 = exp_n(i)
        exp1 = n_exp(i)
        assert _similar_func(exp0, lambda x: x ** i)
        assert _similar_func(exp0.f_prime(), lambda x: i * x ** (i - 1))
        assert _similar_func(exp1, lambda x: i ** x)
        assert _similar_func(exp1.f_prime(), lambda x: i ** x * log(i))

    assert list(map(add_n(5), range(10))) == list(range(5, 15))

    root = exp_n(0.5)
    assert _similar_func(root, lambda x: x ** 0.5)
    assert _similar_func(root.f_prime(), lambda x: 1 / (2 * x ** 0.5))

    for i in range(2, _ITERS + 2):
        log0 = log_base_n(i)
        log1 = log_of_n(i)
        assert _similar_func(log0, lambda x: log(x, i))
        assert _similar_func(log0.f_prime(), lambda x: 1 / (x * log(i)))
        assert _similar_func(log1, lambda x: log(i, x))
        assert _similar_func(log1.f_prime(), lambda x: -log(i) / (x * (log(x) ** 2)))

def test_comp():
    for i in range(_ITERS):
        lt = lt_n(i)
        le = le_n(i)
        gt = gt_n(i)
        ge = ge_n(i)
        for j in range(_ITERS):
            assert lt(j) == (j < i)
            assert le(j) == (j <= i)
            assert gt(j) == (j > i)
            assert ge(j) == (j >= i)
            
def test_index():
    lst = list(range(_ITERS, 2 * _ITERS))
    for i in range(_ITERS):
        getter = get_n(i)
        assert getter(lst) == lst[i]

    for i in range(_ITERS):
        setter = set_n_to_val(i, 0)
        setter(lst)
        assert lst[i] == 0

def test_trig():
    base = [sin, cos, tan, asin, acos, atan]
    ops = [sine, cosine, tangent, arcsine, arccosine, arctangent]
    divs = [lambda x: cos(x), lambda x: -sin(x), lambda x: 1 + tan(x) ** 2,
            lambda x: 1 / sqrt(1 - x ** 2), lambda x: -1 / sqrt(1 - x ** 2), lambda x: 1 / (1 + x ** 2)]
    assert len(base) == len(ops)
    assert len(ops) == len(divs)
    domain = np.arange(-0.9, 1, 0.1)

    for i in range(len(base)):
        trig = ops[i]()
        assert _similar_func(trig, base[i], domain = domain), i
        assert _similar_func(trig.f_prime(), divs[i], domain = domain), i

def test_combos():
    for i in range(_ITERS):
        m = _ITERS - i
        c = chain(add_n(i), mult_n(m))
        assert _similar_func(c, lambda x: i + m * x)
        assert _similar_func(c.f_prime(), lambda x: m)

    c2 = chain(chain(exp_n(2), add_n(3)),
               chain(f_plus_g(identity(), log_base_n(2)),
                     f_times_g(const(4), identity())))
    assert _similar_func(c2, lambda x: (4 * x + log(x, 2) + 5) ** 2)
    assert _similar_func(c2.f_prime(), lambda x: 2 * (1 / (log(2) * x) + 4) * (log(x) / log(2) + 4 * x + 5))

    trig_plus = f_plus_g(sine(), cosine())
    assert _similar_func(trig_plus, lambda x: sin(x) + cos(x))
    assert _similar_func(trig_plus.f_prime(), lambda x: cos(x) - sin(x))

    trig_minus = f_minus_g(sine(), cosine())
    assert _similar_func(trig_minus, lambda x: sin(x) - cos(x))
    assert _similar_func(trig_minus.f_prime(), lambda x: cos(x) + sin(x))

    for i in range(_ITERS):
        polynomial = f_plus_g(chain(mult_n(i), exp_n(2)), mult_n(i))
        assert _similar_func(polynomial, lambda x: i * x ** 2 + i * x)
        assert _similar_func(polynomial.f_prime(), lambda x: 2 * i * x + i)

    trig_times = f_times_g(sine(), cosine())
    assert _similar_func(trig_times, lambda x: sin(x) * cos(x))
    assert _similar_func(trig_times.f_prime(), lambda x: cos(x) ** 2 - sin(x) ** 2)

    trig_div = f_divided_by_g(sine(), cosine())
    assert _similar_func(trig_div, lambda x: sin(x) / cos(x))
    assert _similar_func(trig_div.f_prime(), lambda x: 1 / cos(x) ** 2)

    for i in range(_ITERS):
        line = mx_plus_b(i, i * 2)
        assert _similar_func(line, lambda x: i * x + i * 2)
        assert _similar_func(line.f_prime(), lambda x: i)

    plus_mul = add_n(5) ** mult_n(3)
    assert _similar_func(plus_mul, lambda x: (x + 5) ** (3 * x))
    assert _similar_func(plus_mul.f_prime(), lambda x: ((x + 5) ** (3 * x)) * (3 * log(x + 5) + (3 * x) / (x + 5)))
    assert _similar_func(plus_mul.f_prime().f_prime(),
                         lambda x: ((x + 5) ** (3 * x)) * (3 * log(x + 5) + (3 * x) / (x + 5)) ** 2 +
                                   ((x + 5) ** (3 * x)) * (6 / (x + 5) - (3 * x) / ((x + 5) ** 2)))

    exp_log = const(2) ** log_base_n(3)
    assert _similar_func(exp_log, lambda x: 2 ** (log(x, 3)))
    assert _similar_func(exp_log.f_prime(), lambda x: (log(2) * 2 ** log(x, 3)) / (log(3) * x))
    assert _similar_func(exp_log.f_prime().f_prime(), lambda x: -(log(2) * (log(3) - log(2)) * 2 ** log(x, 3)) / 
                                                                 ((log(3) * x) ** 2))

    assert _similar_func(add_n(10)(mult_n(5)), lambda x: 5 * x + 10)

def test_simplify():
    assert isinstance(add_n(0), identity)
    assert isinstance(sub_n(0), identity)
    assert isinstance(mult_n(1), identity)
    assert isinstance(mult_n(0), const)
    assert mult_n(0).n == 0
    assert isinstance(exp_n(1), identity)
    assert isinstance(exp_n(0), const)
    assert exp_n(0).n == 1
    assert isinstance(div_n(1), identity)
    assert isinstance(n_div(0), const)
    assert n_div(0).n == 0
    assert isinstance(n_floordiv(0), const)
    assert n_floordiv(0).n == 0
    assert isinstance(n_exp(0), const)
    assert n_exp(0).n == 0
    assert isinstance(n_exp(1), const)
    assert n_exp(1).n == 1
    assert isinstance(log_of_n(1), const)
    assert log_of_n(1).n == 0
    assert isinstance(chain(add_n(2), const(3)), const)
    assert chain(add_n(2), const(3)).n == 5
    assert isinstance(chain(const(5), exp_n(10)), const)
    assert chain(const(5), exp_n(10)).n == 5
    assert isinstance(chain(identity(), n_floordiv(10)), n_floordiv)
    assert isinstance(f_plus_g(const(10), const(15)), const)
    assert f_plus_g(const(10), const(15)).n == 25
    assert isinstance(f_plus_g(log_base_n(2), const(0)), log_base_n)
    assert isinstance(f_plus_g(const(0), log_base_n(2)), log_base_n)
    assert isinstance(f_minus_g(const(10), const(15)), const)
    assert f_minus_g(const(10), const(15)).n == -5
    assert isinstance(f_minus_g(log_base_n(2), const(0)), log_base_n)
    assert isinstance(f_times_g(const(10), const(15)), const)
    assert f_times_g(const(10), const(15)).n == 150
    assert isinstance(f_times_g(log_base_n(2), const(0)), const)
    assert f_times_g(log_base_n(2), const(0)).n == 0
    assert isinstance(f_times_g(const(0), log_base_n(2)), const)
    assert f_times_g(const(0), log_base_n(2)).n == 0
    assert isinstance(f_times_g(const(1), n_exp(2)), n_exp)
    assert isinstance(f_times_g(n_exp(2), const(1)), n_exp)
    assert isinstance(f_divided_by_g(const(1), const(2)), const)
    assert f_divided_by_g(const(1), const(2)).n == 0.5
    assert isinstance(f_divided_by_g(const(10), const(1)), const)
    assert f_divided_by_g(const(10), const(1)).n == 10
    assert isinstance(f_divided_by_g(const(0), chain(add_n(10), sub_n(5))), const)
    assert f_divided_by_g(const(0), chain(add_n(10), sub_n(5))).n == 0
    assert isinstance(f_raised_to_g(const(0), n_exp(10)), const)
    assert f_raised_to_g(const(0), n_exp(10)).n == 0
    assert isinstance(f_raised_to_g(const(1), n_exp(10)), const)
    assert f_raised_to_g(const(1), n_exp(10)).n == 1
    assert isinstance(f_raised_to_g(n_exp(10), const(1)), n_exp)
    assert isinstance(f_raised_to_g(exp_n(2), const(0)), const)
    assert f_raised_to_g(exp_n(2), const(0)).n == 1
    assert isinstance(add_n(-10), sub_n)
    assert _similar_func(add_n(-10), lambda x: x - 10)
    assert isinstance(sub_n(-5), add_n)
    assert _similar_func(sub_n(-5), lambda x: x + 5)
    assert isinstance(div_n(1), identity)

def test_arithmetic():
    assert _similar_func(add_n(10) + mult_n(5), lambda x: x * 6 + 10)
    assert _similar_func(sub_n(3) * div_n(10), lambda x: (x - 3) * (x / 10))
    assert _similar_func(exp_n(2) - log_base_n(2), lambda x: (x ** 2) - log(x, 2))
    assert _similar_func(n_exp(3) / const(10), lambda x: (3 ** x) / 10)
    assert _similar_func(mult_n(2) + 5, lambda x: 2 * x + 5)
    assert _similar_func(add_n(10) - 5, lambda x: x + 5)
    assert _similar_func(sub_n(2) + 'x', lambda x: 2 * x - 2)
    assert _similar_func(add_n(10) + '3x + 4', lambda x: 4 * x + 14)

    funcs = [const, identity, add_n, sub_n, n_sub, mult_n, n_div, n_div]
    domain = np.arange(-2, 2, 0.3)
    for f in funcs:
        for g in funcs:
            for i in range(-_ITERS, _ITERS):
                if i != 0:
                    fx = f() if f == identity else f(i)
                    gx = g() if g == identity else g(i)

                    assert _similar_func(fx + gx, lambda x: fx(x) + gx(x), domain = domain)
                    assert _similar_func(fx - gx, lambda x: fx(x) - gx(x), domain = domain)
                    assert _similar_func(fx * gx, lambda x: fx(x) * gx(x), domain = domain)
                    assert _similar_func(fx / gx, lambda x: fx(x) / gx(x), domain = domain)
                    assert _similar_func(fx ** gx, lambda x: fx(x) ** gx(x), domain = domain)

                    if g != identity:
                        gx2 = g(-i)
                        assert _similar_func(fx + gx2, lambda x: fx(x) + gx2(x), domain = domain)
                        assert _similar_func(fx - gx2, lambda x: fx(x) - gx2(x), domain = domain)
                        assert _similar_func(fx * gx2, lambda x: fx(x) * gx2(x), domain = domain)
                        assert _similar_func(fx / gx2, lambda x: fx(x) / gx2(x), domain = domain)
                        assert _similar_func(fx ** gx2, lambda x: fx(x) ** gx2(x), domain = domain)

def test_arithmetic_simplify():
    assert isinstance(const(10) + const(5), const)
    assert (const(10) + const(5)).n == 15
    assert isinstance(const(10) - const(5), const)
    assert (const(10) - const(5)).n == 5
    assert isinstance(const(10) * const(5), const)
    assert (const(10) * const(5)).n == 50
    assert isinstance(const(10) / const(5), const)
    assert (const(10) / const(5)).n == 2
    assert isinstance(const(10) ** const(5), const)
    assert (const(10) ** const(5)).n == 10 ** 5
    assert isinstance(add_n(10) + const(15), add_n)
    assert (add_n(10) + const(15)).n == 25
    assert isinstance(const(15) + add_n(10), add_n)
    assert (const(15) + add_n(10)).n == 25
    assert isinstance(add_n(10) - const(5), add_n)
    assert (add_n(10) - const(4)).n == 6
    assert isinstance(add_n(10) - const(15), sub_n)
    assert (add_n(10) - const(15)).n == 5
    assert isinstance(const(10) - add_n(5), n_sub)
    assert (const(10) - add_n(5)).n == 5
    assert isinstance(sub_n(10) + const(5), sub_n)
    assert (sub_n(10) + const(4)).n == 6
    assert isinstance(sub_n(5) + const(10), add_n)
    assert (sub_n(4) + const(10)).n == 6
    assert isinstance(sub_n(5) - const(10), sub_n)
    assert (sub_n(5) - const(10)).n == 15
    assert isinstance(sub_n(10) - const(5), sub_n)
    assert (sub_n(10) - const(5)).n == 15
    assert isinstance(n_sub(10) + const(5), n_sub)
    assert (n_sub(10) + const(5)).n == 15
    assert isinstance(n_sub(10) - const(5), n_sub)
    assert (n_sub(10) - const(4)).n == 6
    assert isinstance(const(5) + n_sub(10), n_sub)
    assert (const(5) + n_sub(10)).n == 15
    assert isinstance(const(5) - n_sub(10), sub_n) 
    assert (const(4) - n_sub(10)).n == 6
    assert isinstance(const(10) - n_sub(5), add_n)
    assert (const(10) - n_sub(4)).n == 6
    assert isinstance(const(5) * mult_n(10), mult_n)
    assert (const(5) * mult_n(10)).n == 50
    assert isinstance(mult_n(10) * const(5), mult_n)
    assert (mult_n(10) * const(5)).n == 50
    assert isinstance(const(5) * n_div(10), n_div)
    assert (const(5) * n_div(10)).n == 50
    assert isinstance(const(5) / div_n(10), n_div)
    assert (const(5) / div_n(10)).n == 50
    assert isinstance(identity() + const(5), add_n)
    assert (identity() + const(5)).n == 5
    assert isinstance(identity() + identity(), mult_n)
    assert (identity() + identity()).n == 2
    assert isinstance(identity() - const(5), sub_n)
    assert (identity() - const(5)).n == 5
    assert isinstance(const(5) - identity(), n_sub)
    assert (const(5) - identity()).n == 5
    assert isinstance(identity() - identity(), const)
    assert (identity() - identity()).n == 0
    assert isinstance(identity() - add_n(5), const)
    assert (identity() - add_n(5)).n == -5
    assert isinstance(identity() - sub_n(5), const)
    assert (identity() - sub_n(5)).n == 5
    assert isinstance(identity() * identity(), exp_n)
    assert (identity() * identity()).n == 2
    assert isinstance(identity() * exp_n(2), exp_n)
    assert (identity() * exp_n(2)).n == 3
    assert isinstance(exp_n(2) * identity(), exp_n)
    assert (exp_n(2) * identity()).n == 3
    assert isinstance(identity() * n_div(2), const)
    assert (identity() * n_div(2)).n == 2
    assert isinstance(n_div(2) * identity(), const)
    assert (n_div(2) * identity()).n == 2
    assert isinstance(identity() / identity(), const)
    assert (identity() / identity()).n == 1
    assert isinstance(identity() / const(5), div_n)
    assert (identity() / const(5)).n == 5
    assert isinstance(const(5) / identity(), n_div)
    assert (const(5) / identity()).n == 5
    assert isinstance(identity() / mult_n(5), const)
    assert (identity() / mult_n(5)).n == 0.2
    assert isinstance(identity() / div_n(5), const)
    assert (identity() / div_n(5)).n == 5
    assert isinstance(add_n(5) - identity(), const)
    assert (add_n(5) - identity()).n == 5
    assert isinstance(sub_n(5) - identity(), const)
    assert (sub_n(5) - identity()).n == -5
    assert isinstance(identity() + n_sub(5), const)
    assert (identity() + n_sub(5)).n == 5
    assert isinstance(n_sub(5) + identity(), const)
    assert (n_sub(5) + identity()).n == 5
    assert isinstance(identity() + 'x', mult_n)
    assert (identity() + 'x').n == 2
    assert isinstance(f_plus_g(identity(), identity()), mult_n)
    assert isinstance(f_minus_g(add_n(5), identity()), const)
    assert isinstance(f_times_g(mult_n(5), n_div(10)), const)
    assert isinstance(f_divided_by_g(mult_n(5), identity()), const)

def test_strs():
    if _TEST_STRS:
        print('\n')
        print(str(mx_plus_b(5, 10)))
        print(mx_plus_b(10, 5).derivative())
        print(str(f_plus_g(add_n(5), exp_n(2))))
        print(f_plus_g(add_n(5), exp_n(2)).derivative())
        print('\n')
        print(derivative('3x + 4'))
        print(derivative('(x / 2) / x^2'))
        print('\n')
        print(parse_expr('(x / 2) / x^2').f_prime().derivative())
        
