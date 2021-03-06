from collections import deque
import numpy as np
from typing import Deque

def rolling_average(x: np.ndarray, n_buckets: int = 0) -> np.ndarray:
    """Returns the values for a rolling average of x.
    
    Specifically, the ith value in x will correspond to the average of
    x[i - n_buckets - 1:i + 1]. Useful for plotting with 
    matplotlib.pyplot.plot(range(x.shape[0]), rolling_average(x)).

    Args:
    :   x (np.array) : the array of values to average
    :   n_buckets (int) : how large the sample should be. If zero (the default),
        n_buckets will be one-tenth the length of x

    Returns:
    :   avgs (np.array) : the array of rolling averages
    """
    res = np.empty(x.shape[0])
    q: Deque[float] = deque()
    curr_total: float = 0
    n_buckets = n_buckets if n_buckets else x.shape[0] // 10
    for i in range(x.shape[0]):
        if len(q) >= n_buckets:
            curr_total -= q.popleft()
        
        curr_total += x[i]
        q.append(x[i])
        res[i] = curr_total / len(q)

    return res

