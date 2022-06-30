from .parsing import parse_expr

def derivative(expr: str) -> str:
    """Finds the derivative of a string expression.
    
    e.g. 3x + 4 or (x / 2) / (x^2), where ^ means exponent

    Args:
    :   expr (str) : a string representing an expression

    Returns:
    :   f_prime (str) : a string representing the derivative of the expression
    """
    return parse_expr(expr).derivative()