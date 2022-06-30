from __future__ import annotations
from ...utilities import number

class Token:
    def __eq__(self, other) -> bool:
        return type(other) == type(self)

class Num (Token):
    def __init__(self, n: number):
        self.n: number = n

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.n == other.n

class Var (Token):
    def __init__(self, s: str):
        self.s: str = s

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.s == other.s

class _BinOp (Token):
    def __init__(self, l: Token, r: Token):
        self.l: Token = l
        self.r: Token = r

    def __eq__(self, other) -> bool:
        return (
            super().__eq__(other) and 
            self.l == other.l and 
            self.r == other.r
        )

class Plus (_BinOp):
    pass

class Minus (_BinOp):
    pass

class Times (_BinOp):
    pass

class Divide (_BinOp):
    pass

class Exponent (_BinOp):
    pass

class Log (Token):
    def __init__(self, base: Token, expr: Token):
        self.base: Token = base
        self.expr: Token = expr

    def __eq__(self, other) -> bool:
        return (super().__eq__(other) and 
                self.base == other.base and 
                self.expr == other.expr)

class _Trig (Token):
    def __init__(self, expr: Token):
        self.expr: Token = expr

    def __eq__(self, other) -> bool:
        return super().__eq__(other) and self.expr == other.expr

class Sin (_Trig):
    pass

class Cos (_Trig):
    pass

class Tan (_Trig):
    pass

class ArcSin (_Trig):
    pass

class ArcCos (_Trig):
    pass

class ArcTan (_Trig):
    pass