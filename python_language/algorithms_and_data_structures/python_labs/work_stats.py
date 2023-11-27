
def bracket_sequence(raw_string):
    stack, flag = [], True
    for i in raw_string:
        if i in ['(','[','{']:
            stack.append(i)
        elif i in [')','}',']']:
            if len(stack) == 0:
                flag = False
                break
            if (i == ')' and stack.pop() == '(') \
                or (i == '}' and stack.pop() == '{') \
                or (i == ']' and stack.pop() == '['):
                continue
            else:
                flag = False
                break
    return print('Является скобочной последовательностью') if flag == True else print('Является не скобочной последовательностью')

def polska_calculate(raw_string):
    stack = []
    flag = True
    for symbol in raw_string:
        if symbol.isdigit():
            stack.append(int(symbol))
        else:
            if len(stack) == 0:
                flag = False
                break
            if symbol == '*':
                stack.append(stack.pop() * stack.pop())
            elif symbol == '+':
                stack.append(stack.pop() + stack.pop())
            elif symbol == '-':
                i = stack.pop()
                j = stack.pop()
                stack.append(j - i)
            elif symbol == '/':
                i = stack.pop()
                j = stack.pop()
                stack.append(j / i)
    if flag:
        print(*stack)
    else:
        print('Ошибка')
