from .utilities import close_enough
from math import floor

class frange:
    """A range-like iterator that supports floats.

    Same signature as range
    """
    def __init__(self, *args):
        arity_str = f'Arity mismatch: expected no more than three arguments, got {len(args)}'
        assert len(args) > 0 and len(args) <= 3, arity_str
        if len(args) == 1:
            self.start = 0
            self.stop = args[0]
            self.step = 1
        elif len(args) == 2:
            self.start = args[0]
            self.stop = args[1]
            self.step = 1
        else:
            self.start = args[0]
            self.stop = args[1]
            self.step = args[2]
    
    def __iter__(self):
        """Allows for iteration from start to stop with step-size jumps."""
        current = self.start
        diff = current - self.stop
        while diff < 0 and not close_enough(diff, 0):
            yield current
            current += self.step
            diff = current - self.stop

    def __len__(self):
        """Returns the (estimated) number of iterations this iterator will yield."""
        return floor((self.stop - self.start) / self.step)

