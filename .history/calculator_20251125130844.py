a=10
b=20
c=30
print(a)
print(b)
print(c)

class Calculator:
    """A simple calculator class."""

    def addition(self, a, b):
        """Returns the sum of a and b."""
        return a + b

    def subtract(self, a, b):
        """Returns the difference of a and b."""
        return a - b

    def into(self, a, b):
        """Returns the product of a and b."""
        return a * b

    def division(self, a, b):
        """Returns the quotient of a and b. Raises ValueError on division by zero."""
        if b == 0:
            raise ValueError("Cannot divide by zero.")
        return a / b