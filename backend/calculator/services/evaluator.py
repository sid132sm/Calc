"""Safe arithmetic expression evaluation for the calculator API."""

from __future__ import annotations

import math
import re


class ExpressionError(ValueError):
    """Raised when a calculator expression cannot be evaluated."""


TOKEN_PATTERN = re.compile(r"\d+(?:\.\d*)?|\.\d+|[+\-×÷]")
OPERATORS = {"+", "-", "×", "÷"}


def evaluate(expression: str) -> str:
    """Evaluate basic arithmetic without using Python's ``eval`` function."""
    expression = expression.strip()
    if not expression or len(expression) > 200:
        raise ExpressionError("Enter a valid expression.")

    tokens = TOKEN_PATTERN.findall(expression)
    if "".join(tokens) != expression:
        raise ExpressionError("Enter a valid expression.")

    values: list[float] = []
    pending: list[str] = []
    expects_value = True

    def apply() -> None:
        operator = pending.pop()
        right = values.pop()
        left = values.pop()
        if operator == "+":
            values.append(left + right)
        elif operator == "-":
            values.append(left - right)
        elif operator == "×":
            values.append(left * right)
        else:
            if right == 0:
                raise ExpressionError("Cannot divide by zero.")
            values.append(left / right)

    for token in tokens:
        if token in OPERATORS:
            if expects_value:
                # The interface's sign toggle produces a leading negative number.
                if token == "-" and not values and not pending:
                    values.append(0.0)
                else:
                    raise ExpressionError("Enter a valid expression.")
            else:
                while pending and _priority(pending[-1]) >= _priority(token):
                    apply()
            pending.append(token)
            expects_value = True
        else:
            if not expects_value:
                raise ExpressionError("Enter a valid expression.")
            values.append(float(token))
            expects_value = False

    if expects_value:
        raise ExpressionError("Enter a valid expression.")
    while pending:
        apply()

    if len(values) != 1 or not math.isfinite(values[0]):
        raise ExpressionError("Result is not a finite number.")
    return format(values[0], ".12g")


def _priority(operator: str) -> int:
    return 2 if operator in {"×", "÷"} else 1
