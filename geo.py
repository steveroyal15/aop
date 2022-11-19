
# import ply and yacc library
import ply.lex as lex
import ply.yacc as yacc


import sys


# Token for reserve words
reserve = {
    'print': 'PRINT',
    'DRAW': 'DRAW',
    'SET': 'SET',
    'exit': 'EXIT'
}


# List of tokens plus concatenate reserve tokens
tokens = [
    "INT",
    "FLOAT",
    "POINTS",
    "IDENTIFIER",
    "EQUALS",
    "SHAPE",
    "COLOR",
    'LPAREN',
    'RPAREN',
    'COMMA',
] + list(reserve.values())


# regex to identify left parenthesis
t_LPAREN = r'\('
# regex to identify right parenthesis
t_RPAREN = r'\)'
# regex to identify comma
t_COMMA = r'\,'


# function and regex to identify points
def t_POINTS(t):
    r'(\(\d+\.\d+,\d+\.\d+\))|(\(\d+\,\d+\.\d+\))|(\(\d+\.\d+,\d+\))|(\(\d+\,\d+\))'
    t.value = (float(t.value.split(',')[0].replace(
        '(', '')), float(t.value.split(',')[1].replace(')', ''),))
    t.type = "POINTS"
    return t


# function and regex to identify float numbers
def t_Float(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    t.type = "FLOAT"
    return t


# function and regex to identify integer
def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


# function and regex to identify shapes
def t_SHAPE(t):
    r'RECTANGLE|CIRCLE|LINE|SQUARE'
    t.value = t.value
    t.type = "SHAPE"
    return t

# function and regex to identify Colors


def t_COLOR(t):
    r'RED|BLUE|GREEN|BLACK|YELLOW|ORANGE'
    t.value = t.value
    t.type = "COLOR"
    return t


# function and regex to identify Identifier
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserve.get(t.value, "IDENTIFIER")
    return t


# Regex to identify equal sign
t_EQUALS = r'\='


# function and regex to identify new line
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


# function print error when a character doesn't match grammer
def t_error(t):
    print("Illegal character!")


# regex to identify characters to ignore when checking for token
t_ignore = ' \t'

# assign the lexer to a variable
lexer = lex.lex()


precedence = (


)


# Main function to run grammers
def p_run(p):
    '''
    run : var_assign
        | get_var
        | print
        | draw
        | exit_program
        | empty
    '''
    result = run(p[1])
    if (result != None):
        if (result[0] != 'var'):
            print(result)
        else:
            print(result[1])


# grammer for setting defining a variable and set it's value
def p_var_assign(p):
    '''
var_assign : SET IDENTIFIER EQUALS INT
           | SET IDENTIFIER EQUALS FLOAT
           | SET IDENTIFIER EQUALS SHAPE
           | SET IDENTIFIER EQUALS COLOR
           | SET IDENTIFIER EQUALS POINTS
           | SET IDENTIFIER EQUALS get_var
    '''
    # add the name of function,the identifier name and it's value to a tuple for further processing
    p[0] = ('SET', p[2], p[4])


# grammer to indentify when user want to exit program
def p_exit_program(p):
    '''
    exit_program : EXIT LPAREN RPAREN
    '''
    p[0] = ('exit_program', p[1])


# grammer to get the value of an identifier
def p_get_var(p):
    '''
    get_var : IDENTIFIER
    '''
    p[0] = ('var', p[1])


# grammer for a print statement to print whatever is between the parenthesis
def p_print(p):
    '''
    print : PRINT LPAREN expression RPAREN
    '''
    p[0] = ('print', p[3])


# grammer for drawing a shape
def p_draw_shape(p):
    '''
    draw : drawRec
         | drawCircle
    '''
    p[0] = ('draw', p[1])


# grammer for drawing a circle
def p_drawCircle(p):
    '''
    drawCircle : DRAW SHAPE expression COMMA expression COMMA expression
               | DRAW expression expression COMMA expression COMMA expression
    '''
    p[0] = ('draw', p[2], p[3], p[5], p[7])


# grammer for drawing a rectangle
def p_drawRec(p):
    '''
    drawRec : DRAW SHAPE expression COMMA expression COMMA expression COMMA expression COMMA expression
            | DRAW expression expression COMMA expression COMMA expression COMMA expression COMMA expression
    '''
    p[0] = ('draw', p[2], p[3], p[5], p[7], p[9], p[11])


# grammer for an expression and what can be an expression
def p_experession(p):
    '''
    expression : get_var
               | INT
               | FLOAT
               | POINTS
               | COLOR
    '''
    p[0] = ('expression', p[1])


# grammer  to identify a empty statement when user doesn't enter anything and press
def p_empty(p):
    '''
    empty :
    '''
    p[0] = None

# function to identify an error in the grammer and print error messsage


def p_error(p):
    print("Syntax error in expression")


# a python environment variable used as a dictionary to look up geo variables and values
env = {}


# a function to analyze tokens and grammer to perform specific task (operates like the parse tree)
def run(p):
    global env
    # check if the statement grammer contains a tuple(Array)
    if type(p) == tuple:
        if p[0] == 'SET':
            env[p[1]] = p[2]
        elif p[0] == 'var':
            if p[1] in env:
                p = env.get(p[1])
                return p
            else:
                return 'undeclared variable found'.format(run(p[1]))
        elif (p[0] == 'expression'):
            return run(p[1])
        elif p[0] == "print":
            p = run(p[1])
            return p
        elif p[0] == "draw":
            if (run(p[1][1]) == 'CIRCLE'):
                parsetree = p[1]
                midpoint = run(parsetree[2])
                radius = run(parsetree[3])
                color = run(parsetree[4])
                import draw as draw
                env['DrawCanvas'] = draw.DrawShape()
                env['DrawCanvas'].drawCircle(midpoint, radius, color)
            elif (run(p[1][1]) == 'RECTANGLE'):
                parsetree = p[1]
                topleftx = run(parsetree[2])
                toplefty = run(parsetree[3])
                length = run(parsetree[4])
                width = run(parsetree[5])
                color = run(parsetree[6])
                import draw as draw
                env['DrawCanvas'] = draw.DrawShape()
                env['DrawCanvas'].drawRec(
                    topleftx, toplefty, length, width, color)
            else:
                # Print a error if the grammer detect a value that's not a shape
                print("Syntax error {} is not a Shape. Bad expression".format(
                    run(p[1][1])))
                # exit the programing if the exit statement was enter
        elif p[0] == "exit_program":
            print('Program exited......')
            print('Thank you for using GEO......')
            raise EOFError
        else:
            return p
    else:
        return p


parser = yacc.yacc()

print('...............................Welcome to GEO Terminal................................')
# while loop to keep program running unil exit by user
while True:
    try:
        # create a terminal like look for our GEO programming language
        s = input('Geo >>')
        parser.parse(s)
    except EOFError:
        break
