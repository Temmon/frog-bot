

def add(ctx, num1:int, num2:int):
    return f"{num1} + {num2} is {num1 + num2}"

frogs = [{
            "command": add,
            "name": "add",
            "description": "Adds two numbers",
        }]


if __name__ == '__main__':
    print(add(None, 3, 4))
    print(add(None, 3, -4))
    print(add(None, 0, 2))
    print(add(None, -4, 1))
