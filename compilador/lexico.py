# Palabras reservadas: se reconocen primero como ID y luego se reclasifican
reservadas = {
    'pan'       : 'RENTERO',
    'migaja'    : 'RDECIMAL',
    'cadena'    : 'RCADENA',
    'sospecha'  : 'RBOOLEANO',
    'si_jala'   : 'RSI',
    'valio'     : 'RSINO',
    'insiste'   : 'RMIENTRAS',
    'para'      : 'RPARA',
    'invocar'   : 'RMOSTRAR',
    'real'      : 'RVERDADERO',
    'ia'        : 'RFALSO',
}

tokens  = [
    'PARIZQ',
    'PARDER',
    'LLAVIZQ',
    'LLAVDER',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'IGUAL',
    'IGUALIGUAL',
    'DIFERENTE',
    'MENORQUE',
    'MAYORQUE',
    'MENORIGUAL',
    'MAYORIGUAL',
    'AND',
    'OR',
    'NOT',
    'PTCOMA',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'ID'
] + list(reservadas.values())

# Tokens
t_PARIZQ     = r'\('
t_PARDER     = r'\)'
t_LLAVIZQ    = r'\{'
t_LLAVDER    = r'\}'
t_MAS        = r'\+'
t_MENOS      = r'-'
t_POR        = r'\*'
t_DIVIDIDO   = r'/'
t_MODULO     = r'%'
t_IGUAL      = r'='
t_IGUALIGUAL = r'=='
t_DIFERENTE  = r'!='
t_MENORQUE   = r'<'
t_MAYORQUE   = r'>'
t_MENORIGUAL = r'<='
t_MAYORIGUAL = r'>='
t_AND        = r'&&'
t_OR         = r'\|\|'
t_NOT        = r'!'
t_PTCOMA     = r';'

def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Floaat value too large %d", t.value)
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        t.value = 0
    return t

def t_CADENA(t):
    r'"[^"\n]*"'
    t.value = t.value[1:-1]     # quita las comillas
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reservadas.get(t.value, 'ID')     # distingue mayúsculas, como C
    return t

# Comentarios: no regresan token, así que se descartan
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count("\n")

def t_COMENTARIO_SIMPLE(t):
    r'//.*'

# Caracteres ignorados
t_ignore = " \t"


def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def t_error(t):
    raise Exception("Error léxico: carácter ilegal '%s' (línea %d)" % (t.value[0], t.lexer.lineno))

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


def analizar_lexico(codigo):
    """Regresa la lista de tokens del código como tuplas (tipo, valor, línea)."""
    lexer.lineno = 1
    lexer.input(codigo)
    return [(t.type, t.value, t.lineno) for t in lexer]


if __name__ == "__main__":
    from pathlib import Path

    ejemplo = Path(__file__).resolve().parent.parent / "ejemplos" / "ejemplo.deiv"
    for token in analizar_lexico(ejemplo.read_text(encoding="utf-8")):
        print(token)
