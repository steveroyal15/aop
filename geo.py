from typing import Tuple
import ply.lex as lex
import ply.yacc as yacc
from pyparsing import col
import draw

import sys

reserve = {
    'print': 'PRINT',
    'DRAW': 'DRAW',
    'SET': 'SET'
}

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


t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COMMA = r'\,'


def t_POINTS(t):
    r'(\(\d+\.\d+,\d+\.\d+\))|(\(\d+\,\d+\.\d+\))|(\(\d+\.\d+,\d+\))|(\(\d+\,\d+\))'
    t.value = (float(t.value.split(',')[0].replace(
        '(', '')), float(t.value.split(',')[1].replace(')', ''),))
    t.type = "POINTS"
    return t


def t_Float(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    t.type = "FLOAT"
    return t


def t_INT(t):
    r'\d+'
    t.value = int(t.value)
    return t


def t_SHAPE(t):
    r'Shapes.Rectangle|Shapes.Circle|Shapes.Line|Shapes.Square'
    t.value = t.value.split('.', 1)[1]
    t.type = "SHAPE"
    return t


def t_COLOR(t):
    r'Colors.Red|Colors.Blue|Colors.Green|Colors.Black|Colors.Yellow|Colors.Organge'
    t.value = t.value.split('.', 1)[1]
    t.type = "COLOR"
    return t


def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    t.type = reserve.get(t.value, "IDENTIFIER")
    return t


t_EQUALS = r'\='


def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)


def t_error(t):
    print("Illegal character!")


t_ignore = ' \t'
lexer = lex.lex()


precedence = (

)


def p_run(p):
    '''
    run : var_assign
        | get_var
        | print
        | draw
    '''
    run(p[1])


def p_var_assign(p):
    '''
var_assign : SET IDENTIFIER EQUALS INT
           | SET IDENTIFIER EQUALS FLOAT
           | SET IDENTIFIER EQUALS SHAPE
           | SET IDENTIFIER EQUALS COLOR
           | SET IDENTIFIER EQUALS POINTS
           | SET IDENTIFIER EQUALS IDENTIFIER
    '''
    p[0] = ('SET', p[2], p[4])


def p_get_var(p):
    '''
    get_var : IDENTIFIER
    '''
    p[0] = ('var', p[1])


def p_print(p):
    '''
    print : PRINT LPAREN expression RPAREN
    '''
    p[0] = ('print', p[3])


def p_draw_shape(p):
    '''
    draw : drawRec
         | drawCircle
    '''
    p[0] = ('draw', p[1])


def p_drawCircle(p):
    '''
    drawCircle : DRAW SHAPE expression COMMA expression COMMA expression
    '''
    p[0] = ('draw', p[2], p[3], p[5], p[7])


def p_drawRec(p):
    '''
    drawRec : DRAW SHAPE expression COMMA expression COMMA expression COMMA expression COMMA expression
    '''
    p[0] = ('draw', p[2], p[3], p[5], p[7], p[9], p[11])


def p_experession(p):
    '''
    expression : get_var
               | INT
               | FLOAT
               | POINTS
               | COLOR
    '''
    p[0] = ('expression', p[1])


env = {}


def run(p):
    global env
    if type(p) == tuple:
        if p[0] == 'SET':
            env[p[1]] = p[2]
        elif p[0] == 'var':
            return env.get(p[1])
        elif (p[0] == 'expression'):
            return run(p[1])
        elif p[0] == "print":
            print(run(p[1]))
        elif p[0] == "draw":
            if (p[1][1] == 'Circle'):
                parsetree = p[1]
                midpoint = run(parsetree[2])
                radius = run(parsetree[3])
                color = run(parsetree[4])
                env['DrawCanvas'] = draw.DrawShape()
                env['DrawCanvas'].drawCircle(midpoint, radius, color)
            elif (p[1][1] == 'Rectangle'):
                parsetree = p[1]
                topleftx = run(parsetree[2])
                toplefty = run(parsetree[3])
                length = run(parsetree[4])
                width = run(parsetree[5])
                color = run(parsetree[6])
                env['DrawCanvas'] = draw.DrawShape()
                env['DrawCanvas'].drawRec(
                    topleftx, toplefty, length, width, color)
        else:
            return p

    else:
        return p


parser = yacc.yacc()

while True:
    try:
        s = input('Geo >>')
    except EOFError:
        break
    parser.parse(s)
