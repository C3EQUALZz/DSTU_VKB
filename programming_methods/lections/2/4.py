# Реверс строки с помощью стека

def reverse_string(string: str):
    stack = []

    for ch in string:
        stack.append(ch)

    result = ''
    while len(stack):
        result += stack.pop()

    return result

print(reverse_string("hello"))
