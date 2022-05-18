class Token:
    def __eq__(self, other):
        return type(other) == type(self)

class Num (Token):
    def __init__(self, n):
        self.n = n

    def __eq__(self, other):
        super().__eq__(other) and self.n == other.n

class Var (Token):
    def __init__(self, s):
        self.s = s

    def __eq__(self, other):
        super().__eq__(other) and self.s == other.s

class _BinOp (Token):
    def __init__(self, l, r):
        self.l = l
        self.r = r

    def __eq__(self, other):
        (super().__eq__(other) and 
         self.l == other.l and 
         self.r == other.r)

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
    def __init__(self, base, expr):
        self.base = base
        self.expr = expr

    def __eq__(self, other):
        return (super().__eq__(other) and 
                self.base == other.base and 
                self.expr == other.expr)

class _Trig (Token):
    def __init__(self, expr):
        self.expr = expr

    def __eq__(self, other):
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