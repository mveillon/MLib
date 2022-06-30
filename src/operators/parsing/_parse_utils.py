from __future__ import annotations
from typing import Any, Deque, Union, TYPE_CHECKING, Dict, Type, Set
if TYPE_CHECKING:
    from ..base_arithmetic import ArithmeticOpBase

from .token_types import Token, Exponent, Divide, Times, Minus, Plus, _BinOp, _Trig
from .token_types import Sin, Cos, Tan, ArcSin, ArcCos, ArcTan, Log
from ..arithmetic import const, identity, _single_arg
from ..combos import TwoFunctionsBase, f_divided_by_g, f_minus_g, f_plus_g, f_raised_to_g, f_times_g
from ..trig_functions import sine, cosine, tangent, arccosine, arcsine, arctangent

number = Union[int, float]

_FLOAT_CHARS: Set[str] = set(map(str, range(10))) | set('-.')
_OP_CHARS: Set[str] = set('+-*^/')
_FUNC_STRS: Set[str] = {'sin', 'cos', 'tan', 'asin', 'acos', 'atan', 'log', 'ln'}

_FUNC_COMBOS: Dict[Type[Token], Type[TwoFunctionsBase]] = {
    Plus : f_plus_g,
    Minus : f_minus_g,
    Times : f_times_g,
    Divide : f_divided_by_g,
    Exponent : f_raised_to_g
}

_TRIG_MAP: Dict[Type[Token], Type[_single_arg]] = {
    Sin : sine,
    Cos : cosine,
    Tan : tangent,
    ArcSin : arcsine,
    ArcCos : arccosine,
    ArcTan : arctangent
}

PRIORITIES: Dict[str, int] = {
    '^' : 0,
    '/' : 1,
    '*' : 2,
    '-' : 3,
    '+' : 4
}

_BIN_OPS: Dict[str, Union[Type[_BinOp], Type[Log]]] = {
    '^' : Exponent,
    '/' : Divide,
    '*' : Times,
    '-' : Minus,
    '+' : Plus,
    'log' : Log
}

_ONE_ARG: Dict[str, Type[_Trig]] = {
    'sin' : Sin,
    'cos' : Cos,
    'tan' : Tan,
    'asin' : ArcSin,
    'acos' : ArcCos,
    'atan' : ArcTan
}

_VAR_CHARS_C: Set[str] = _FLOAT_CHARS | _OP_CHARS | set('()')

def remove_whitespace(s: str) -> str:
    """Returns new string with no whitespace."""
    return ''.join(s.split())

def _is_float_char(c: str) -> bool:
    """Returns whether c could be in a float."""
    return c in _FLOAT_CHARS

def is_op_char(c: str) -> bool:
    """Returns whether c is a mathematical operator."""
    return c in _OP_CHARS

def is_func_str(s: str) -> bool:
    """Returns whether s is the invocation of a function."""
    return s in _FUNC_STRS

def _is_var(c: str) -> bool:
    """Returns whether c is a variable name."""
    return len(c) == 1 and c not in _VAR_CHARS_C

def _check_tokens(tokens: Deque[str], expr: str) -> None:
    """Checks that all the tokens are valid and errors otherwise."""
    var_name = ''
    for i, tok in enumerate(tokens):
        if not tok:
            raise ValueError(f'Internal error: empty token in {tokens}')

        elif _is_var(tok):
            if not var_name:
                var_name = tok
            elif tok != var_name:
                raise SyntaxError(f'Only single-variable functions are supported: {expr}')

        elif len(tok) > 1 and not (can_be_float(tok) or is_func_str(tok) or is_op_char(tok)):
            raise SyntaxError(f'Variables can have just one letter, so {tok} is not allowed: {expr}')

        elif len(tok) > 1 and _is_float_char(tok[0]) and not can_be_float(tok):
            raise SyntaxError(f'Invalid number: {tok}')

        elif i < len(tok) - 1 and is_op_char(tok) and is_op_char(tok[i + 1]):
            raise SyntaxError(f'Expected expression between operators: {expr}')

def _class_name(op: Any) -> str:
    """Returns the name of the class of this operator."""
    return type(op).__name__

def disp_operator(op: ArithmeticOpBase) -> str:
    """Returns a pretty string representing the operator function tree.
    
    Args:
    :   op (ArithmeticOpBase) : the function to display

    Returns:
    :   tree (str) : a string with the whole tree
    """
    return '\n' + _disp_helper(op, 0)

def _disp_helper(op: ArithmeticOpBase, tabs: int) -> str:
    """Displays the operator function tree."""
    if isinstance(op, const):
        return str(op.n)
    if isinstance(op, identity):
        return 'x'
    if isinstance(op, TwoFunctionsBase):
        tabs += 1
        tab_str = '\t' * tabs
        return f'{_class_name(op)} :\n{tab_str}{_disp_helper(op.first, tabs)} and\n{tab_str}{_disp_helper(op.second, tabs)}'
    if isinstance(op, _single_arg):
        return f'{_class_name(op)}(x)'
    return f'{_class_name(op)} with n = {op.n}'

def can_be_float(thing: Any) -> bool:
    """Returns whether the thing can be casted as a float without erroring.
    
    Args:
    :   thing (any) : the object to look at

    Returns:
    :   is_float (bool) : whether the object can be a float
    """
    try:
        n = float(thing)
        return True
    except ValueError:
        return False
