import sys
sys.setrecursionlimit(10000)

############################################
########### CODE IS NOT COMPLETE YET #######



tokens = []
i = 0

def peek(s=0):
    global tokens, i
    if i + s >= len(tokens): 
        return [None, None]
    return tokens[i + s]

def eat(expected, isValue=0):
    global tokens, i
    if peek()[isValue] == expected: 
        i += 1
    else: 
        raise SyntaxError(f'Expected {expected} not {tokens[i][isValue]} at i = {i}')

def WHITESPACE():
    global i
    global tokens
    while peek()[0] in ['white space', 'new line']: 
        eat(peek()[0], 0)
    return

def DATATYPE():
    global i
    global tokens
    if peek()[1] in ['int', 'char', 'bool', 'float', 'double']: 
        eat('keyword', 0)
    else: 
        raise SyntaxError(f'Expected datatype not {tokens[i]} at i = {i}')

def ID():
    global i
    global tokens
    if peek()[0] == 'identifier': 
        eat('identifier', 0)
    else: 
        raise SyntaxError(f'Expected identifier not {tokens[i]} at i = {i}')

def COMMENT():
    global i
    global tokens
    # Handle // comment
    if peek()[1] == '//':
        eat('//', 1)
        eat('comment', 0)
    # Handle /* comment */
    elif peek()[1] == '/*':
        eat('/*', 1)
        eat('comment', 0)
        eat('*/', 1)
    else: 
        raise SyntaxError(f'Expected comment not {tokens[i]} at i = {i}')
    return

def NUM_CONST():
    global i
    global tokens
    if peek()[0] == 'numerical constant':
        eat('numerical constant', 0)
    else: 
        raise SyntaxError(f'expected numerical constant not {peek()}')

def CHAR_CONST():
    global i
    global tokens
    if peek()[1] == "'":
        eat("'", 1)
        eat('character constant', 0)
        eat("'", 1)
    else: 
        raise SyntaxError(f'expected character constant not {peek()}')

def EQU_OP():
    global i
    global tokens
    if peek()[1] in ['==', '*', '+', '-', '/', '%']: 
        eat('operator', 0)
    else: 
        raise SyntaxError(f'Expected operator not {tokens[i]} at i = {i}')

def ASSIGNMENT_OPERATOR():
    global i
    global tokens
    if peek()[1] in ['=', '+=', '-=', '*=', '/=', '%=']: 
        eat('operator', 0)
    else: 
        raise SyntaxError(f'Expected assignment operator not {tokens[i]} at i = {i}')

def VALUE():
    global i
    global tokens
    if peek()[0] == 'numerical constant':
        NUM_CONST()
    elif peek()[1] == "'":
        CHAR_CONST()
    elif peek()[0] == 'identifier':
        ID()
    else: 
        raise SyntaxError(f'Invalid value: {peek()} at i = {i}')

def EQU_FORM():
    global i
    global tokens
    VALUE()
    WHITESPACE()
    EQU_OP()
    WHITESPACE()
    VALUE()

def EQUATION():
    global i
    global tokens
    saved = i
    try:
        EQU_FORM()
        return
    except SyntaxError:
        i = saved
        VALUE()

def IF():
    global i
    global tokens
    eat('if', 1)
    WHITESPACE()
    eat('(', 1)
    WHITESPACE()
    EQUATION()
    WHITESPACE()
    eat(')', 1)
    WHITESPACE()
    eat('{', 1)
    CODE()
    eat('}', 1)
    WHITESPACE()
    ELSE()

def ELSE():
    global i
    global tokens
    saved = i
    try:
        eat('else', 1)
        WHITESPACE()
        if peek()[1] == '{':
            eat('{', 1)
            WHITESPACE()
            CODE()
            WHITESPACE()
            print(i, peek())
            eat('}', 1)
        else:
            IF()
    except SyntaxError:
        i = saved  # ε case - no else

def DECLARE_FOLLOWER():
    global i
    global tokens
    if peek()[1] == ',':
        eat(',', 1)
        WHITESPACE()
        ID()
        WHITESPACE()
        DECLARE_FOLLOWER()
    elif peek()[1] == ';':
        eat(';', 1)
    else: 
        raise SyntaxError(f'Expected \',\' or \';\' not {tokens[i]} at i = {i}')

def DECLARE():
    global i
    global tokens
    DATATYPE()
    WHITESPACE()
    eat('identifier', 0)
    WHITESPACE()
    DECLARE_FOLLOWER()
    WHITESPACE()

def RETURN():
    global i
    global tokens
    eat('return', 1)
    WHITESPACE()
    EQUATION()
    eat(';', 1)
    WHITESPACE()

def ASSIGNMENT():
    global i
    global tokens
    saved = i
    # Try with datatype first
    try:
        DATATYPE()
        WHITESPACE()
    except SyntaxError:
        i = saved  # No datatype - simple assignment
    
    ID()
    WHITESPACE()
    ASSIGNMENT_OPERATOR()
    WHITESPACE()
    EQUATION()
    eat(';', 1)
    WHITESPACE()

def ITEM():
    global i
    global tokens
    saved = i
    # Try each possible item type
    if peek()[1] in ['int', 'char', 'bool', 'float', 'double']:
        try:
            DECLARE()
            return True
        except SyntaxError:
            i = saved
            try:
                ASSIGNMENT()
                return True
            except SyntaxError:
                i = saved
    elif peek()[1] == '//' or peek()[1] == '/*':
        COMMENT()
        WHITESPACE()
        return True
    elif peek()[1] == 'if':
        IF()
        return True
    elif peek()[1] == 'return':
        RETURN()
        return True
    elif peek()[0] in ['white space', 'new line']:
        WHITESPACE()
        return True
    elif peek()[1] == '}':
        return False  # End of code block
    else:
        # Try assignment without datatype
        try:
            ASSIGNMENT()
            return True
        except SyntaxError:
            i = saved
    
    return False  # Could not parse any item

def CODE():
    # Parse zero or more items
    while True:
        if not ITEM():
            break

def P():
    eat('int', 1)
    WHITESPACE()
    eat('main', 1)
    WHITESPACE()
    eat('(', 1)
    WHITESPACE()
    eat(')', 1)
    WHITESPACE()
    eat('{', 1)
    WHITESPACE()
    CODE()
    WHITESPACE()
    eat('}', 1)
    WHITESPACE()
    
    # Check for EOF
    if i < len(tokens):
        raise SyntaxError(f'Unexpected tokens at end: {tokens[i:]}')

# Read tokens
code = open("./tokens.txt", "r")
tokens_raw = code.read().strip()[1:-1].split(">\n<")
tokens = []

for token in tokens_raw:
    if token:
        token = token.split(",", 1)
        if len(token) == 2:
            tokens.append([token[0].strip(), token[1].strip()])
        else:
            tokens.append([token[0].strip(), ''])

code.close()

# print(tokens)

print(f"Total tokens: {len(tokens)}")

try:
    P()
    print("Parsing successful! No syntax errors.")
except SyntaxError as e:
    print(f"Syntax Error: {e}")
    print(f"Current token index: {i}")
    if i < len(tokens):
        print(f"Current token: {tokens[i]}")
    print(f"Previous tokens: {tokens[max(0, i-3):i]}")
except Exception as e:
    print(f"Unexpected error: {e}")
    import traceback
    traceback.print_exc()