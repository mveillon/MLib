class ArithmeticOpBase:
    """Abstract base class for all arithmetic operations.

    These are objects so they can have derivative methods, but they can be
    used like functions i.e. ArithmeticOpBase(0) can be used like a function
    that takes a number and returns a number, even for higher-order functions
    like map.

    Note that, on construction, these objects will simplify themselves, meaning you
    may not end up with an object of the same type as the one you constructed. The
    returned object will always be a descendant of ArithmeticOpBase and will always
    have the same functionality.

    You can add, subtract, multiply, divide, and exponentiate functions using the
    appropriate operators (e.g. +, *). Doing so will return a new function that 
    combines the two given functions appropriately. You can also add numbers and 
    strings to functions. The strings should be parsable expressions.

    Finally, calling an ArithmeticOpBase with another ArithmeticOpBase will return
    a new chain function that first calls the inner function (the one passed as the
    argument), then the outer on the input.
    
    Args:
        n (number) : the constant to use in the operation
    """
    def __init__(self, n):
        self.n = n
        self.priority = -1 #higher means it should go first

    def __new__(cls, n):
        """We define this to allow simplification."""
        return super(ArithmeticOpBase, cls).__new__(cls)
        
    def f(self, x):
        """Returns the result of the function called on x.
        
        Args:
        :   x (number) : the number to pass to the function

        Returns:
        :   res (number) : x combined with self.n in some way based on the specific function
        """
        raise NotImplementedError

    def derivative(self):
        """Returns a string form of the derivative of this function.

        Formatted as an expression (i.e. no 'f(x) = ') for recursive reasons.
        
        Args:
        :   None

        Returns:
        :   f_prime (str) : the symbolic derivative as a string
        """
        return str(self.f_prime())

    def __call__(self, x):
        """Allows the object to pretend to be a function. Returns f(x)."""
        if isinstance(x, ArithmeticOpBase):
            from .combos import chain
            return chain(self, x)
        return self.f(x)

    def f_prime(self):
        """Returns a function that returns the instantaneous slope at x.
        
        Args:
        :   None

        Returns:
        :   derivative (ArithmeticBaseOp) : a function that computes the derivative
        """
        raise NotImplementedError

    def __str__(self):
        """Returns string representation of expression."""
        raise NotImplementedError

    def _get_func(self, other):
        """Makes the other into an ArithmeticOpBase, if it isn't already."""
        if isinstance(other, ArithmeticOpBase):
            return other
        if isinstance(other, int) or isinstance(other, float):
            from .arithmetic import const
            return const(other)
        if isinstance(other, str):
            from .parsing import parse_expr
            return parse_expr(other)
        raise ValueError(f'Unexpected argument to function arithmetic: {other}')

    def _binop(self, other, combiner):
        """Combines self and other using combiner."""
        return combiner(self, self._get_func(other))

    def _simple_add(self, other):
        """Tries to return simplified self + other. If it can't, it will return None."""
        other = self._get_func(other)
        from .arithmetic import const
        if isinstance(other, const) and other.n == 0:
            return self
        return None

    def _simple_sub(self, other):
        """Tries to return simplified self - other. If it can't, it will return None."""
        other = self._get_func(other)
        from .arithmetic import const
        if isinstance(other, const) and other.n == 0:
            return self
        return None

    def _simple_mul(self, other):
        """Tries to return simplified self * other. If it can't, it will return None."""
        other = self._get_func(other)
        from .arithmetic import const
        if isinstance(other, const):
            if other.n == 0:
                return const(0)
            if other.n == 1:
                return self
        return None

    def _simple_div(self, other):
        """Tries to return simplified self / other. If it can't, it will return None."""
        other = self._get_func(other)
        from .arithmetic import const
        if isinstance(other, const) and other.n == 1:
            return self
        return None

    def _simple_exp(self, other):
        """Tries to return simplified self ** other. If it can't, it will return None."""
        other = self._get_func(other)
        from .arithmetic import const
        if isinstance(other, const):
            if other.n == 0:
                return const(1)
            if other.n == 1:
                return self
        return None

    def __add__(self, other): 
        s = self._simple_add(other)
        from .combos import f_plus_g
        return self._binop(other, f_plus_g) if s is None else s

    def __sub__(self, other):
        s = self._simple_sub(other)
        from .combos import f_minus_g
        return self._binop(other, f_minus_g) if s is None else s

    def __mul__(self, other):
        s = self._simple_mul(other)
        from .combos import f_times_g
        return self._binop(other, f_times_g) if s is None else s

    def __truediv__(self, other):
        s = self._simple_div(other)
        from .combos import f_divided_by_g
        return self._binop(other, f_divided_by_g) if s is None else s

    def __pow__(self, other):
        s = self._simple_exp(other)
        from .combos import f_raised_to_g
        return self._binop(other, f_raised_to_g) if s is None else s

class _single_arg (ArithmeticOpBase):
    """Abstract base class for single-argument functions."""
    def __init__(self):
        self.priority = 5

    def __new__(cls):
        o = object.__new__(cls)
        o.__init__()
        return o

