# test.py
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b

# Test the functions
if __name__ == "__main__":
    print(add(3, 4))
    print(subtract(10, 5))
    print(multiply(2, 3))
    print(divide(9, 3))