# -----------------------------------------------------------------------------
# Fase 3: análisis semántico
# Recorre el árbol sin ejecutarlo y revisa que toda variable usada esté declarada.
# -----------------------------------------------------------------------------

def _revisar_expresion(e, declaradas):
    if e[0] == 'id':
        if e[1] not in declaradas:
            raise Exception("Error semántico: la variable '%s' no está declarada" % e[1])
    elif e[0] in ('negativo', 'not'):
        _revisar_expresion(e[1], declaradas)
    elif e[0] == 'binaria':
        _revisar_expresion(e[2], declaradas)
        _revisar_expresion(e[3], declaradas)

def analizar_semantico(instrucciones, declaradas=None):
    """Lanza Exception si hay error semántico; si no, regresa el conjunto de variables declaradas."""
    if declaradas is None:
        declaradas = set()
    for ins in instrucciones:
        if ins[0] == 'declarar':
            _, tipo, nombre, expr = ins
            if expr:
                _revisar_expresion(expr, declaradas)
            declaradas.add(nombre)
        elif ins[0] == 'asignar':
            _, nombre, expr = ins
            if nombre not in declaradas:
                raise Exception("Error semántico: la variable '%s' no está declarada" % nombre)
            _revisar_expresion(expr, declaradas)
        elif ins[0] == 'mostrar':
            _revisar_expresion(ins[1], declaradas)
        elif ins[0] == 'si':
            _, condicion, entonces, sino = ins
            _revisar_expresion(condicion, declaradas)
            analizar_semantico(entonces, declaradas)
            analizar_semantico(sino, declaradas)
        elif ins[0] == 'mientras':
            _, condicion, cuerpo = ins
            _revisar_expresion(condicion, declaradas)
            analizar_semantico(cuerpo, declaradas)
        elif ins[0] == 'para':
            _, inicio, condicion, paso, cuerpo = ins
            analizar_semantico([inicio], declaradas)
            _revisar_expresion(condicion, declaradas)
            analizar_semantico(cuerpo, declaradas)
            analizar_semantico([paso], declaradas)
    return declaradas
