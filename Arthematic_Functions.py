from numbers import Number
import operator
import math

def arithmetic(a, b=None, op='+'):
    """
    Perform arithmetic operations.

    a, b: numbers (b can be None for unary ops)
    op: operation name or symbol. Supported:
      '+' or 'add'
      '-' or 'sub'
      '*' or 'mul'
      '/' or 'div'
      '//' or 'floordiv'
      '%' or 'mod'
      '**' or 'pow'
      'neg' (unary)
      'abs' (unary)
      'sqrt' (unary)
    Returns the numeric result or raises ValueError/ZeroDivisionError/TypeError.
    """
    if not isinstance(a, Number):
        raise TypeError("a must be a number")
    if op in ('neg', 'abs', 'sqrt'):
        if b is not None:
            raise ValueError(f"operation '{op}' is unary and does not accept b")
        if op == 'neg':
            return -a
        if op == 'abs':
            return abs(a)
        if op == 'sqrt':
            if a < 0:
                raise ValueError("sqrt of negative number")
            return math.sqrt(a)

    if b is None or not isinstance(b, Number):
        raise TypeError("b must be a number for binary operations")

    ops = {
        '+': operator.add, 'add': operator.add,
        '-': operator.sub, 'sub': operator.sub,
        '*': operator.mul, 'mul': operator.mul,
        '/': operator.truediv, 'div': operator.truediv,
        '//': operator.floordiv, 'floordiv': operator.floordiv,
        '%': operator.mod, 'mod': operator.mod,
        '**': operator.pow, 'pow': operator.pow,
    }

    func = ops.get(op)
    if func is None:
        raise ValueError(f"unsupported operation: {op}")
    # let underlying operator raise ZeroDivisionError if needed
    return func(a, b)