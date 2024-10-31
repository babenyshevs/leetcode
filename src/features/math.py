import numpy as np
from typing import Dict

def get_derivative(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """
    Calculate the derivative of two arrays with normalization.

    Parameters:
    ----------
    x : np.ndarray
        The first array (independent variable values).
    y : np.ndarray
        The second array (dependent variable values).

    Returns:
    -------
    np.ndarray
        Array containing the calculated derivative values, with NaN prepended
        to match the length of the input arrays.

    Example:
    -------
    >>> x = np.array([1, 2, 3, 4])
    >>> y = np.array([2, 4, 6, 8])
    >>> get_derivative(x, y)
    array([nan, 2. , 2. , 2. ])
    """
    # Ensure inputs are numpy arrays
    x = np.array(x)
    y = np.array(y)

    # Calculate percentage differences
    dx_perc = np.diff(x) / x[:-1]
    dy_perc = np.diff(y) / y[:-1]

    # Compute the derivative and round to 4 decimal places
    derivative = np.round(dy_perc / dx_perc, 4)

    # Align with original array length by prepending NaN
    derivative = np.insert(derivative, 0, np.nan)

    return derivative

def fib(n: int, memo: Dict[int, int] = {}) -> int:
    """
    Compute the nth Fibonacci number using memoization.

    Parameters:
    ----------
    n : int
        The position of the Fibonacci sequence to calculate.
    memo : Dict[int, int], optional
        A dictionary for storing previously computed Fibonacci numbers.

    Returns:
    -------
    int
        The nth Fibonacci number.

    Example:
    -------
    >>> fib(5)
    5
    >>> fib(10)
    55
    """
    if n in memo:  # Check if already computed
        return memo[n]
    if n <= 1:
        return n
    # Store the result in the memo dictionary
    memo[n] = fib(n - 1, memo) + fib(n - 2, memo)
    return memo[n]
