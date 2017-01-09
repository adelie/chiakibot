import re
import random

operators = { '^' : (lambda a, b: a ** b, 4, 'right'), '*' : (lambda a, b: a * b, 3, 'left'),
              '/' : (lambda a, b: 1.0 * a / b, 3, 'left'), '+' : (lambda a, b: a + b, 2, 'left'),
              '-' : (lambda a, b: a - b, 2, 'left') }
def roll(dice):
    """Boop."""
    dice = dice.replace(' ', '')
    tokens = re.split('(\+|-|\*|/|\^|\(|\))', dice)
    print(tokens)
    stack = []
    output = []

    # parse into postfix notation for use
    for token in tokens:
        if token in operators:
            if operators[token][2] == 'left':
                while stack and stack[-1] in operators and operators[token][1] <= operators[stack[-1]][1]:
                    output.append(stack.pop())
            elif operators[token][2] == 'right':
                while stack and stack[-1] in operators and operators[token][1] < operators[stack[-1]][1]:
                    output.append(stack.pop())
            stack.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            if stack and stack[-1] == '(':
                stack.pop()
        elif token:
            output.append(token)
    while stack:
        output.append(stack.pop())

    # now that everything's been parsed, solve and give numbers!
    stack = []
    for token in output:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            stack.append(operators[token][0](a, b))
        else:
            stack.append(roll_calculator(token))
    print(stack[0])

def roll_calculator(dice):
    result = 0
    try:
        result = int(dice)
    except ValueError:
        tokens = dice.split('d')
        if len(tokens) == 1 or not tokens[1].isdigit():
            pass
        else:
            rolls, limit = tokens
            if not rolls:
                rolls = 1
            rolls, limit = int(rolls), int(limit)
            for roll in range(rolls):
                result += random.randint(1, limit)
    return result
