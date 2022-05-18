from src import parse_expr, shunting_yard, find_tokens
import numpy as np
from math import log, sin, cos, tan, asin, acos, atan, e

def _similar_func(f, g, domain = np.arange(-5, 5, 0.5), silent = False):
    """Returns whether f and g have the same behavior over domain."""
    if isinstance(domain, np.ndarray):
        domain = domain.tolist()
    for x in domain:
        f_error = False
        try:
            f_res = f(x)
        except:
            f_error = True
        if f_error:
            try:
                g_res = g(x)
                if not silent: print(f'f errored at x = {x} but g did not')
                return False
            except:
                continue
        else:
            try:
                g_res = g(x)
            except:
                if not silent: print(f'g errored at x = {x} but f did not')
                return False
            if not np.isclose(f_res, g_res):
                if not silent: print(f'with x = {x}, f output: {f_res} != g output: {g_res}')
                return False

    return True

def test_shunting():
    assert shunting_yard('2x + 1') == ['2', 'x', '*', '1', '+']
    assert shunting_yard('2(x + 1)') == ['2', 'x', '1', '+', '*']
    assert shunting_yard('3x^2') == ['3', 'x', '2', '^', '*']
    assert shunting_yard('(3x)^2') == ['3', 'x', '*', '2', '^']
    assert shunting_yard('3 + 4 * (2 - 1)') == ['3', '4', '2', '1', '-', '*', '+']
    assert shunting_yard('50sin(202x)') == ['50', '202', 'x', '*', 'sin', '*']

def test_tokens():
    assert list(find_tokens('50x')) == ['50', '*', 'x']
    assert list(find_tokens('-1.0')) == ['-1', '*', '1.0']
    assert list(find_tokens('x - -1')) == ['x', '-', '-1', '*', '1']
    assert list(find_tokens('2x + 1')) == ['2', '*', 'x', '+', '1']
    assert list(find_tokens('2(x + 1)')) == ['2', '*', '(', 'x', '+', '1', ')']
    assert list(find_tokens('202(x + 1)')) == ['202', '*', '(', 'x', '+', '1', ')']
    assert list(find_tokens('202sin(50x)')) == ['202', '*', 'sin', '(', '50', '*', 'x', ')']
    assert list(find_tokens('50^log2(x)')) == ['50', '^', '2', 'log', '(', 'x', ')']
    assert list(find_tokens('(2 + x)(2 - x)')) == ['(', '2', '+', 'x', ')', '*', '(', '2', '-', 'x', ')']
    assert list(find_tokens('(3x)^2')) == ['(', '3', '*', 'x', ')', '^', '2']
    assert list(find_tokens('(x + 2) - (2x)')) == ['(', 'x', '+', '2', ')', '-', '(', '2', '*', 'x', ')']
    assert list(find_tokens('ln(x)')) == [str(e), 'log', '(', 'x', ')']

def test_parser():
    assert _similar_func(lambda x: x + 1, lambda x: x + 1)
    assert _similar_func(lambda x: 1 / x, lambda x: 1 / x)
    assert not _similar_func(lambda x: x, lambda x: x + 1, silent = True)
    assert not _similar_func(lambda x: 1, lambda x: 1 ** (1 / x), silent = True)
    assert not _similar_func(lambda x: 1 ** (1 / x), lambda x: 1, silent = True)
    assert _similar_func(parse_expr('2x + 1'), lambda x: 2 * x + 1)
    assert _similar_func(parse_expr('(2x) + 1'), lambda x: 2 * x + 1)
    assert _similar_func(parse_expr('2(x + 1)'), lambda x: 2 * (x + 1))
    assert _similar_func(parse_expr('x - -1'), lambda x: x + 1)
    assert _similar_func(parse_expr('(2 + x) / (x ^ 2)'), lambda x: (2 + x) / (x ** 2))
    assert _similar_func(parse_expr('(2 + x) / x ^ 2'), lambda x: (2 + x) / (x ** 2))
    assert _similar_func(parse_expr('5 + log2(2x + 2)'), lambda x: 5 + log(2 * x + 2, 2))
    assert _similar_func(parse_expr('1 + 2x'), lambda x: 1 + 2 * x)
    assert _similar_func(parse_expr('2log2(x)'), lambda x: 2 * log(x, 2))
    assert _similar_func(parse_expr('2ln(x)'), lambda x: 2 * log(x))
    assert _similar_func(parse_expr('x - (2 - sin(x))'), lambda x: x - 2 + sin(x))
    assert _similar_func(parse_expr('x - 2 - sin(x)'), lambda x: x - 2 - sin(x))
    funcs = {'sin' : sin,
             'cos' : cos,
             'tan' : tan,
             'asin' : asin,
             'acos' : acos,
             'atan' : atan}
    for f in funcs:
        assert _similar_func(parse_expr(f'5 + {f}(2x / 5)'), 
                             lambda x: 5 + funcs[f](2 * x / 5))

    to_derive = ['2x + 1', '2(x + 1)', 'sin(x) + cos(2x)', '2^log3(x)', '(x / 2) / x^2', 'x ^ ln(x)']
    there_and_back = lambda f: _similar_func(parse_expr(str(f)), f)
    for f in to_derive:
        parsed = parse_expr(f)
        assert there_and_back(parsed)
        assert there_and_back(parsed.f_prime()), f
        assert there_and_back(parsed.f_prime().f_prime()), f
