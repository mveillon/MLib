from __future__ import annotations
from typing import Deque, List
from ..base_arithmetic import ArithmeticOpBase
from .lexer import is_func_str, is_op_char, shunting_yard
from .token_types import Token, Num, Var, Log, _BinOp, _Trig
from ._parse_utils import _ONE_ARG, _BIN_OPS, _FUNC_COMBOS, _TRIG_MAP, _is_var, can_be_float
from ..arithmetic import const, identity, log_base_n
from ..combos import chain
from collections import deque

def parse_expr(expr: str) -> ArithmeticOpBase:
    """Parses the arithmetic function and returns a ArithmeticOpBase.
    
    Args:
    :   expr (str) : a string representing a mathematical function

    Returns:
    :   func (ArithmeticOpBase) : an object that can be treated like a function
            with the same output as the given expr
    """
    return _parse_tree(_str_to_tree(shunting_yard(expr), expr), expr)

def _parse_tree(tree: Token, expr: str) -> ArithmeticOpBase:
    """Parses the tree into an ArithmeticOpBase."""
    typ = type(tree)
    if isinstance(tree, Num):
        return const(tree.n)

    if isinstance(tree, Var):
        return identity()

    if isinstance(tree, Log):
        const_base = _parse_tree(tree.base, expr)
        if not isinstance(const_base, const):
            raise SyntaxError(f'Expected scalar value for log base: {expr}')
        return chain(log_base_n(const_base.n), _parse_tree(tree.expr, expr))

    if isinstance(tree, _BinOp):
        return _FUNC_COMBOS[typ](_parse_tree(tree.l, expr),
                                 _parse_tree(tree.r, expr))

    if isinstance(tree, _Trig):
        return chain(_TRIG_MAP[typ](), _parse_tree(tree.expr, expr))

    raise ValueError(f'Internal error: invalid tree {tree} from {expr}')

def _str_to_tree(tokens: List[str], expr: str) -> Token:
    """Takes a list of tokens from shunting yard and turns it into a syntax tree of Token objects."""
    if len(tokens) == 0:
        raise SyntaxError(f'Empty expression {expr}')

    operands: Deque[Token] = deque()
    for tok in tokens:
        if is_op_char(tok) or tok == 'log':
            if len(operands) < 2:
                raise SyntaxError(f'Arity mismatch. Expected two arguments for {tok}: {expr}')
            r = operands.pop()
            l = operands.pop()
            operands.append(_BIN_OPS[tok](l, r))

        elif is_func_str(tok):
            if not operands:
                raise SyntaxError(f'Arity mismatch. Expected one argument for {tok}: {expr}')

            operands.append(_ONE_ARG[tok](operands.pop()))

        elif _is_var(tok):
            operands.append(Var(tok))

        elif can_be_float(tok):
            operands.append(Num(float(tok)))

        else:
            raise SyntaxError(f'Unexpected token {tok} in {expr}')

    if len(operands) != 1:
        raise ValueError(f'Internal error: wrong number of operands {operands} in {expr}')

    return operands[0]
    