import json

tokens = {}

# reserved_words
reserved_words = ["WRITE", "READ", "IF", "ELSE", "RETURN", "BEGIN", "END", "MAIN", "STRING", "INT", "REAL", "REPEAT",
                  "UNTIL"]

# operators
operators = {'(': "LEFT-PARENTHESIS", ')': "RIGHT-PARENTHESIS", '+': "PLUS", '-': "MINUS", '*': "MULTIPLY",
             '/': "DIVIDE", ';': "SEMICOLON", '<': "SMALLER-THAN", '>': "BIGGER-THAN", '=': "EQUAL"}


def save_token(temp, output):
    global tokens

    # terminate reading token
    if not temp:
        return

    # output.write(temp)
    # if it's a reserved_words
    if temp in reserved_words:
        tokens[temp] = temp
        # output.write(": " + temp)

    # it's a number
    elif temp.isdecimal() or '.' in temp:
        tokens[temp] = "NUMBER"
        # output.write(": NUMBER")

    elif temp in operators:
        tokens[temp] = operators[temp]
        # output.write(": " + operators[temp])

    elif temp == ':=':
        tokens[temp] = "ASSIGN"
        # output.write(": ASSIGN")

    # it's an indentifier
    else:
        tokens[temp] = "IDENTIFIER"
        # output.write(": IDENTIFIER")

    output.write(json.dumps(tokens) + '\n')
    tokens = {}
    # output.write("\n")


def scanner(input_file, output_file):
    global tokens
    tokens = {}

    # read the file of the instructions
    file = open(input_file, 'r')
    # output file
    global output
    output = open(output_file, 'w')

    temp = ''
    state = "INPUT"

    c = ''
    while True:
        if state != "DONE":
            c = file.read(1)

        if c in operators and temp != ":" and temp != ":=" and state != "COMMENT":
            save_token(temp, output)
            save_token(c, output)
            temp = ""
            state = "INPUT"
            continue

        if not c:
            save_token(temp, output)
            break

        if state == "INPUT":
            if c == ' ' or c == '\n':
                state = "INPUT"

            elif c.isnumeric():
                state = "NUMBER"
                temp += c

            elif c.isalpha():
                state = "STRING"
                temp += c

            elif c == ':':
                temp += c
                state = "ASSIGN"

            elif c == '{':
                state = "COMMENT"

            elif c in operators:
                temp += c
                state = "DONE"
            else:
                state = "ERROR"

        elif state == "STRING":
            if c.isnumeric() or c.isalpha():
                state = "STRING"
                temp += c

            else:
                state = "DONE"

        elif state == "NUMBER":
            if c.isnumeric() or c == '.':
                temp += c
                state = "NUMBER"
            elif c.isalpha():
                state = "ERROR"
            else:
                state = "DONE"

        elif state == "ASSIGN":
            if c == '=':
                temp = ":="
                state = "DONE"
            else:
                state = "ERROR"

        elif state == "COMMENT":
            if c == '}':
                state = "INPUT"

        elif state == "DONE":
            # TODO
            save_token(temp, output)
            temp = ""
            state = "INPUT"

        elif state == "ERROR":
            print("BOW, Syntax Error!")
            return False

    file.close()
    output.close()
    return True
