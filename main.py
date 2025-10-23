code = open("./ideone_ibyt63.cpp", "r").read()

"""
keyword
identifier
operator
numeric constant
character constant
special character
comments
white space
new line
"""

i = 0
word = []
tokens = []
keywords = [
    "int",
    "str",
    "char",
    "if",
    "else",
    "return",
    "for",
    "while",
    "switch",
    "do",
    "include",
]
specialChars = [
    "!",
    "`",
    "@",
    "#",
    "$",
    "(",
    ")",
    "{",
    "}",
    "[",
    "]",
    "\\",
    "'",
    '"',
    ";",
    ":",
    ",",
    "?",
]
stringBrackets = ["`", '"', "'"]
operators = [
    "+",
    "=",
    "*",
    "+",
    "-",
    "%",
    "&",
    "|",
    "+=",
    "-=",
    "*=",
    "/=",
    "%=",
    "**",
    "<",
    ">",
    "<>",
    "<=",
    ">=",
    "==",
    "===",
    "!=",
    "!==",
]
while i < len(code):
    pointFlag = False
    word = []
    if (
        65 <= ord(code[i]) < 91
        or 97 <= ord(code[i]) < 123
        or ord(code[i]) == 95
    ):
        while (
            48 <= ord(code[i]) < 58
            or 65 <= ord(code[i]) < 91
            or 97 <= ord(code[i]) < 123
            or ord(code[i]) == 95
        ):
            word.append(code[i])
            i += 1

        if ''.join(word) in keywords:
            tokens.append(f"<'keyword', {(''.join(word))}>")
        else:
            tokens.append(f"<'identifier', {(''.join(word))}>")

    elif 48 <= ord(code[i]) < 58 or ord(code[i]) == 46:
        while 48 <= ord(code[i]) < 58 or (ord(code[i]) == 46 and pointFlag == False):
            if ord(code[i]) == 46: pointFlag = True
            word.append(code[i])
            i += 1
        tokens.append(f"<'numerical constant', {(''.join(word))}>")

    elif code[i] == '/' and code[i + 1] == '/':
        tokens.append(f"<'special character', //>")
        i += 2
        while code[i] != '\n':
            word.append(code[i])
            i += 1
        tokens.append(f"<'comment', {(''.join(word))}>")
        tokens.append(f"<'new line', \\n>")
        i += 1

    elif code[i] == '/' and code[i + 1] == '*':
        tokens.append(f"<'special character', /*>")
        i += 2
        while f"{code[i]}{code[i + 1]}" != '*/':
            word.append(code[i])
            i += 1
        tokens.append(f"<'comment', {(''.join(word))}>")
        tokens.append(f"<'special character', */")
        i += 2

    elif code[i] in operators:
        if code[i + 1] in operators:
            tokens.append(f"<'operator', {code[i]}{code[i + 1]}>")
            i += 2
            continue
        else:
            tokens.append(f"<'operator', {code[i]}>")
            i += 1
            continue
    elif code[i] in stringBrackets:
        b = code[i]
        tokens.append(f"<'special character', {code[i]}>")
        i += 1
        while code[i] != b:
            word.append(code[i])
            i += 1
        tokens.append(f"<'character constant', {(''.join(word))}>")
        tokens.append(f"<'special character', {code[i]}>")
        i += 1
    elif code[i] == ' ':
        tokens.append(f"<'white space', >")
        i += 1
    elif code[i] == '\n':
        tokens.append(f"<'new line', \\n>")
        i += 1
    elif code[i] in specialChars:
        tokens.append(f"<'special character', {code[i]}>")
        i += 1
    else:
        print('SYNTAX ERROR')

open("./tokens.txt", "w").write('\n'.join(tokens))