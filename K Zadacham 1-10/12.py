class Stack:
    def __init__(self):
        self.stack = []

    def is_empty(self):
        return len(self.stack) == 0

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()

    def peek(self):
        if not self.is_empty():
            return self.stack[-1]

    def size(self):
        return len(self.stack)

def precedence(operator):
    if operator == '+' or operator == '-':
        return 1
    if operator == '*' or operator == '/':
        return 2
    return 0

def infix_to_postfix(expression):
    output = []
    stack = Stack()
    for char in expression.split():
        if char.isdigit():
            output.append(char)
        elif char == '(':
            stack.push(char)
        elif char == ')':
            while not stack.is_empty() and stack.peek() != '(':
                output.append(stack.pop())
            if not stack.is_empty() and stack.peek() != '(':
                return -1
            else:
                stack.pop()
        else:
            while (not stack.is_empty() and
                   precedence(char) <= precedence(stack.peek())):
                output.append(stack.pop())
            stack.push(char)

    while not stack.is_empty():
        output.append(stack.pop())

    return " ".join(output)

expression = "( 10 + 2 ) * 2"
print(infix_to_postfix(expression))
