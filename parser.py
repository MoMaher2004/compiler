import sys
sys.setrecursionlimit(100)

# rules
'''
P => 'int' WHITESPACE ' ' WHITESPACE 'main' WHITESPACE '(' WHITESPACE ')' WHITESPACE '{' WHITESPACE CODE WHITESPACE '}' WHITESPACE
CODE => ITEM CODE | ε
ITEM => ASSIGNMENT | NEWLINE | ASSIGNMENT_DATATYPE | COMMENT | LOOP | IF | RETURN | DECLARE | WHITESPACEASSIGNMENT => ASSIGNMENT_DATATYPE ' ' WHITESPACE ID WHITESPACE ASSIGNMENT_OPERATOR WHITESPACE EQUATION ';'
ASSIGNMENT_DATATYPE => DATATYPE ASSIGNMENT WHITESPACE ' ' | ε

VALUE => NUM_CONST | CHAR_CONST | FUNC_CALL | ID
EQUATION => VALUE | EQU_FORM
EQU_OP => '==' | '+' | '-' | '*' | '/' | '%'
EQU_FORM => VALUE WHITESPACE EQU_OP WHITESPACE VALUE

DATATYPE => 'int' | 'char' | 'float' | 'double' | 'bool'
WHITESPACE => ' ' WHITESPACE | ε
NEWLINE => newline NEWLINE | ε
ASSIGNMENT_OPERATOR => '=' | '+=' | '-=' | '*=' | '/=' | '%='
RETURN => 'return' EQUATION ';'
LOOP => 'for' WHITESPACE '(' WHITESPACE ASSIGNMENT WHITESPACE ';' WHITESPACE EQUATION WHITESPACE ';' WHITESPACE ASSIGNMENT WHITESPACE ')' WHITESPACE '{' WHITESPACE CODE WHITESPACE '}' WHITESPACE | 'while' WHITESPACE '(' WHITESPACE EQUATION WHITESPACE ')' WHITESPACE '{' WHITESPACE CODE WHITESPACE '}'
PARAMS => PARAM | PARAM WHITESPACE ',' WHITESPACE PARAM
PARAM => ID | EQUATION
ID => identifier
IF => 'if' WHITESPACE '(' WHITESPACE EQUATION WHITESPACE ')' WHITESPACE '{' WHITESPACE CODE WHITESPACE '}' ELSE
ELSE => 'else' ' ' IF | 'else' WHITESPACE '{' CODE '}' | ε
DECLARE => DATATYPE WHITESPACE identifier WHITESPACE DECLARE_FOLLOWER WHITESPACE
DECLARE_FOLLOWER => ',' ID DECLARE_FOLLOWER WHITESPACE | ';'
COMMENT => '//' comment | '/*' comment '*/'
NUM_CONST => numeric_constant
CHAR_CONST => character_constant
FUNC_CALL => ID '(' PARAMS ')'
'''

# highlights
'''
tolerance with whitespaces in some places
allow assigning function return values
loops are added
'''

tokens = []
i = 0

def peek(s=0):
    global tokens
    global i
    if i + s >= len(tokens): return None
    return tokens[i + s]

def eat(expected, isValue = 0):
    global tokens
    global i
    # print(peek())
    if peek()[isValue] == expected: i += 1
    else: raise SyntaxError(f'Expected {expected} not {tokens[i][isValue]} at i = {i}')

def WHITESPACE():
    while peek()[0] in ['white space', 'new line']: eat(peek()[0], 0)
    return

def DATATYPE():
    global tokens
    global i
    if peek()[1] in ['int', 'char', 'bool', 'float', 'double']: eat('keyword', 0)
    else: raise SyntaxError(f'Expected datatype not {tokens[i]} at i = {i}')
    return

def ID():
    global tokens
    global i
    if peek()[0] == 'identifier': 
        eat('identifier', 0)
        return 
    else: raise SyntaxError(f'Expected identifier not {tokens[i]} at i = {i}')

def COMMENT():
    global tokens
    global i
    eat('//', 1)
    eat('comment', 0)
    return

def NUM_CONST():
    if peek()[0] == 'numerical constant':
        return
    else: raise SyntaxError(f'expected numerical constant not {peek()}')

def CHAR_CONST():
    if peek()[0] == 'character constant':
        return
    else: raise SyntaxError(f'expected character constant not {peek()}')

def EQU_OP():
    global tokens
    global i
    if peek()[1] in ['==', '*', '+', '-', '/', '%']: eat('operator', 0)
    else: raise SyntaxError(f'Expected operator not {tokens[i]} at i = {i}')
    return

# def PARAMS():

# def FUNC_CALL():
#     ID()
#     eat('(', 1)
#     PARAMS()
#     eat(')', 1)
#     return

def EQU_FORM():
    print(peek())
    VALUE()
    WHITESPACE()
    EQU_OP()
    WHITESPACE()
    VALUE()
    return

def EQUATION():
    global tokens
    global i
    saved = i
    e = None
    for f in [VALUE, EQU_FORM]:
        try:
            f()
            return
        except SyntaxError as err:
            i = saved
            e = err
        except IndexError as err:
            i = saved
            e = err
    raise SyntaxError('Invalid value')

def VALUE():
    global tokens
    global i
    saved = i
    e = None
    for f in [NUM_CONST, CHAR_CONST, EQUATION, ID]: # may add FUNC_CALL later
        try:
            f()
            return
        except SyntaxError as err:
            i = saved
            e = err
        except IndexError as err:
            i = saved
            e = err
    raise SyntaxError('Invalid value')


def IF():
    global tokens
    global i
    eat('if', 1)
    WHITESPACE()
    eat('(', 1)
    WHITESPACE()
    EQUATION()
    WHITESPACE()
    eat(')', 1)
    WHITESPACE()
    eat('{', 1)
    WHITESPACE()
    CODE()
    WHITESPACE()
    eat('}', 1)
    ELSE()
    return

def DECLARE_FOLLOWER():
    global tokens
    global i
    if peek()[1] == ',':
        eat(',', 1)
        ID()
        DECLARE_FOLLOWER()
        WHITESPACE()
        return
    elif peek()[1] == ';':
        eat(';', 1)
        return
    else: raise SyntaxError(f'Expected \',\' or \';\' not {tokens[i]} at i = {i}')

def DECLARE():
    global tokens
    global i
    DATATYPE()
    WHITESPACE()
    eat('identifier', 0)
    WHITESPACE()
    DECLARE_FOLLOWER()
    WHITESPACE()
    return

def CODE():
    global tokens
    global i
    saved = i
    e = None
    for f in [IF, DECLARE, COMMENT, WHITESPACE]:
        print(f.__name__)
        try:
            f()
            CODE()
            return
        except SyntaxError as err:
            i = saved
            e = err
        except IndexError as err:
            i = saved
            e = err
    raise SyntaxError('Invalid code')
        
def P():
    global tokens
    global i
    eat('int', 1)
    eat('white space', 0)
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

code = open("./tokens.txt", "r")
tokens = code.read().split("\n")
tokens = [t[1:-1].split(",", 1) for t in tokens]
P()
code.close()
