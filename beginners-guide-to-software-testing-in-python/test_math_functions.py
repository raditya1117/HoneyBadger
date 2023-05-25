def is_not_a_number(x):
    number_classes = [int, float]
    if type(x) not in number_classes:
        return True
    return False


def add(a, b):
    if is_not_a_number(a) or is_not_a_number(b):
        raise TypeError("Both values must be numbers.")
    return a + b


def subtract(a, b):
    if is_not_a_number(a) or is_not_a_number(b):
        raise TypeError("Both values must be numbers.")
    return a - b


def multiply(a, b):
    if is_not_a_number(a) or is_not_a_number(b):
        raise TypeError("Both values must be numbers.")
    return a * b


def divide(a, b):
    if is_not_a_number(a) or is_not_a_number(b):
        raise TypeError("Both values must be numbers.")
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
