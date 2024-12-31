# good_code.py

def add(a: int, b: int) -> int:
    """Returns the sum of a and b."""
    return a + b

def subtract(a: int, b: int) -> int:
    """Returns the difference between a and b."""
    return a - b

def multiply(a: int, b: int) -> int:
    """Returns the product of a and b."""
    return a * b

def divide(a: int, b: int) -> float:
    """Returns the quotient of a divided by b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

def main():
    """Main function to demonstrate arithmetic operations."""
    try:
        x, y = 10, 5
        print(f"Add: {add(x, y)}")
        print(f"Subtract: {subtract(x, y)}")
        print(f"Multiply: {multiply(x, y)}")
        print(f"Divide: {divide(x, y)}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
