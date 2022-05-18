from ._parse_utils import remove_whitespace, _is_float_char, is_func_str, is_op_char 
from ._parse_utils import _check_tokens, PRIORITIES, _is_var, can_be_float
from collections import deque
from math import e

def find_tokens(expr):
    """Finds all the tokens in expr.
    
    Args:
    :   expr (str) : a string expression in infix form

    Returns:
    :   tokens (list) : a list of tokens (all strings), each element being one of:
            a number, a variable, a function, an operator, or a parenthesis
    """
    res = deque()
    if not expr: return res
    is_num = _is_float_char(expr[0])
    curr_word = deque()
    expr = remove_whitespace(expr)
    i = 0
    while i < len(expr):
        c = expr[i]
        if c == '-' and not curr_word:
            if not res or res[-1] != ')':
                res.append('-1')
                res.append('*')
            else:
                res.append('-')
            if i == len(expr) - 1:
                raise SyntaxError(f'Expected expression after -: {expr}')
            is_num = _is_float_char(expr[i + 1])

        elif is_op_char(c):
            if not (curr_word or (res and res[-1] == ')')):
                raise SyntaxError(f'Expected first argument to operator: {expr}')
            if curr_word: res.append(''.join(curr_word))
            res.append(c)
            curr_word = deque()
            if i == len(expr) - 1:
                raise SyntaxError(f'Expected second argument to operator: {expr}')
            is_num = _is_float_char(expr[i + 1])

        elif c == '(':
            if len(res) >= 2 and res[-2] == 'log':
                res.pop()
                res.pop()
                as_str = ''.join(curr_word)
                if as_str and can_be_float(as_str):
                    res.append(as_str)
                else:
                    raise SyntaxError(f'Unexpected log base {as_str} in {expr}')
                res.append('log')

            elif len(curr_word) == 2 and list(curr_word) == ['l', 'n']:
                res.append(str(e))
                res.append('log')

            elif curr_word:
                res.append(''.join(curr_word))
                if not is_func_str(res[-1]):
                    res.append('*')
                        
            res.append(c)
            curr_word = deque()
            if i < len(expr) - 1:
                is_num = _is_float_char(expr[i + 1])

        elif c == ')':
            if curr_word:
                res.append(''.join(curr_word))
            res.append(c)
            curr_word = deque()
            if i < len(expr) - 1:
                if not is_op_char(expr[i + 1]) and expr[i + 1] != ')':
                    res.append('*')
                is_num = _is_float_char(expr[i + 1])

        elif _is_float_char(c) != is_num:
            res.append(''.join(curr_word))
            res.append('*')
            curr_word = deque([c])
            is_num = not is_num

        else:
            curr_word.append(c)
        
        i += 1

    if curr_word: res.append(''.join(curr_word))
    _check_tokens(res, expr)
    return res

def shunting_yard(expr):
    """Parses the infix expression and turns it into a postfix list of tokens.
    
    Args:
    :   expr (str) : an expression written in infix

    Returns:
    :   tokens (list) : a list of strings representing the tokens, in postfix order
    """
    res = deque()
    operators = deque()
    tokens = find_tokens(expr)
    for tok in tokens:
        if can_be_float(tok) or _is_var(tok):
            res.append(tok)

        elif is_func_str(tok) or tok == '(':
            operators.append(tok)

        elif is_op_char(tok):
            tok_priority = PRIORITIES[tok]
            while (operators and
                   operators[-1] != '(' and 
                   (PRIORITIES[operators[-1]] < tok_priority or
                    (PRIORITIES[operators[-1]] == tok_priority and tok != '^'))):
                res.append(operators.pop())
            operators.append(tok)
            
        elif tok == ')':
            if not operators:
                raise SyntaxError(f'Unmatched right parenthesis in {expr}')
            while operators[-1] != '(':
                res.append(operators.pop())
                if not operators:
                    raise SyntaxError(f'Unmatched right parenthesis in {expr}')

            operators.pop()
            if operators and is_func_str(operators[-1]):
                res.append(operators.pop())

    while operators:
        to_add = operators.pop()
        if to_add == '(':
            raise SyntaxError(f'Unmatched left parenthesis in {expr}')
        res.append(to_add)

    return list(res)
