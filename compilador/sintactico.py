# -----------------------------------------------------------------------------
# Fase 2: análisis sintáctico (arma el árbol, no lo ejecuta)
# -----------------------------------------------------------------------------
from .lexico import tokens, lexer

# Asociación de operadores y precedencia (de menor a mayor, como en C)
precedence = (
    ('left','OR'),
    ('left','AND'),
    ('left','IGUALIGUAL','DIFERENTE'),
    ('left','MENORQUE','MAYORQUE','MENORIGUAL','MAYORIGUAL'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','MODULO'),
    ('right','NOT','UMENOS'),
    )

# Definición de la gramática
# Cada regla arma un nodo (tupla) del árbol; el intérprete lo ejecuta después.
# No se ejecuta durante el parseo porque el cuerpo de un ciclo se reduce una sola vez.
def p_instrucciones_lista(t):
    'instrucciones : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]

def p_instrucciones_una(t):
    'instrucciones : instruccion'
    t[0] = [t[1]]

def p_instruccion(t):
    '''instruccion : declaracion PTCOMA
                   | asignacion PTCOMA
                   | mostrar
                   | si
                   | mientras
                   | para'''
    t[0] = t[1]

def p_tipo(t):
    '''tipo : RENTERO
            | RDECIMAL
            | RCADENA
            | RBOOLEANO'''
    t[0] = t[1]

def p_declaracion(t):
    'declaracion : tipo ID'
    t[0] = ('declarar', t[1], t[2], None)

def p_declaracion_valor(t):
    'declaracion : tipo ID IGUAL expresion'
    t[0] = ('declarar', t[1], t[2], t[4])

def p_asignacion(t):
    'asignacion : ID IGUAL expresion'
    t[0] = ('asignar', t[1], t[3])

def p_mostrar(t):
    'mostrar : RMOSTRAR PARIZQ expresion PARDER PTCOMA'
    t[0] = ('mostrar', t[3])

def p_si(t):
    'si : RSI PARIZQ expresion PARDER bloque'
    t[0] = ('si', t[3], t[5], [])

def p_si_sino(t):
    'si : RSI PARIZQ expresion PARDER bloque RSINO bloque'
    t[0] = ('si', t[3], t[5], t[7])

def p_si_sino_si(t):
    'si : RSI PARIZQ expresion PARDER bloque RSINO si'
    t[0] = ('si', t[3], t[5], [t[7]])

def p_mientras(t):
    'mientras : RMIENTRAS PARIZQ expresion PARDER bloque'
    t[0] = ('mientras', t[3], t[5])

def p_para(t):
    '''para : RPARA PARIZQ declaracion PTCOMA expresion PTCOMA asignacion PARDER bloque
            | RPARA PARIZQ asignacion PTCOMA expresion PTCOMA asignacion PARDER bloque'''
    t[0] = ('para', t[3], t[5], t[7], t[9])

def p_bloque(t):
    'bloque : LLAVIZQ instrucciones LLAVDER'
    t[0] = t[2]

def p_bloque_vacio(t):
    'bloque : LLAVIZQ LLAVDER'
    t[0] = []

def p_expresion_binaria(t):
    '''expresion : expresion MAS expresion
                 | expresion MENOS expresion
                 | expresion POR expresion
                 | expresion DIVIDIDO expresion
                 | expresion MODULO expresion
                 | expresion MENORQUE expresion
                 | expresion MAYORQUE expresion
                 | expresion MENORIGUAL expresion
                 | expresion MAYORIGUAL expresion
                 | expresion IGUALIGUAL expresion
                 | expresion DIFERENTE expresion
                 | expresion AND expresion
                 | expresion OR expresion'''
    t[0] = ('binaria', t[2], t[1], t[3])

def p_expresion_unaria(t):
    'expresion : MENOS expresion %prec UMENOS'
    t[0] = ('negativo', t[2])

def p_expresion_not(t):
    'expresion : NOT expresion'
    t[0] = ('not', t[2])

def p_expresion_agrupacion(t):
    'expresion : PARIZQ expresion PARDER'
    t[0] = t[2]

def p_expresion_valor(t):
    '''expresion : ENTERO
                 | DECIMAL
                 | CADENA'''
    t[0] = ('valor', t[1])

def p_expresion_booleano(t):
    '''expresion : RVERDADERO
                 | RFALSO'''
    t[0] = ('valor', t[1] == 'real')

def p_expresion_id(t):
    'expresion : ID'
    t[0] = ('id', t[1])

def p_error(t):
    if t:
        raise Exception("Error sintáctico en '%s' (línea %d)" % (t.value, t.lineno))
    raise Exception("Error sintáctico: el archivo terminó antes de tiempo")

import ply.yacc as yacc
parser = yacc.yacc()


def analizar_sintactico(codigo):
    """Regresa el árbol (lista de instrucciones); lanza Exception si hay error sintáctico."""
    lexer.lineno = 1
    return parser.parse(codigo, lexer=lexer)


if __name__ == "__main__":
    from pprint import pprint
    try:
        pprint(analizar_sintactico(open("./entrada.txt", "r").read()))
    except Exception as e:
        print(e)
