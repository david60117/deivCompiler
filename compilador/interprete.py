# -----------------------------------------------------------------------------
# Ejecutar: intérprete que recorre el árbol que armó el parser
# -----------------------------------------------------------------------------
import operator

OPERADORES = {
    '+': operator.add, '-': operator.sub, '*': operator.mul, '%': operator.mod,
    '<': operator.lt, '>': operator.gt, '<=': operator.le, '>=': operator.ge,
    '==': operator.eq, '!=': operator.ne,
}
TIPOS = {'pan': int, 'migaja': float, 'cadena': str, 'sospecha': bool}

MAX_ITERACIONES = 100000

def _contar(vueltas):
    if vueltas > MAX_ITERACIONES:
        raise Exception("Error de ejecución: un ciclo superó %d iteraciones" % MAX_ITERACIONES)
    return vueltas + 1

def evaluar(e, tabla):
    if e[0] == 'valor':    return e[1]
    if e[0] == 'negativo': return -evaluar(e[1], tabla)
    if e[0] == 'not':      return not evaluar(e[1], tabla)
    if e[0] == 'id':
        if e[1] not in tabla:
            raise Exception("Error semántico: la variable '%s' no está declarada" % e[1])
        return tabla[e[1]][1]
    # binaria
    op, izq = e[1], evaluar(e[2], tabla)
    if op == '&&': return bool(izq) and bool(evaluar(e[3], tabla))
    if op == '||': return bool(izq) or bool(evaluar(e[3], tabla))
    der = evaluar(e[3], tabla)
    if op in ('/', '%') and der == 0:
        raise Exception("Error semántico: división entre cero")
    if op == '/':
        if type(izq) is int and type(der) is int:   # división entera, como en C
            return int(izq / der)
        return izq / der
    return OPERADORES[op](izq, der)

def ejecutar(instrucciones, tabla):
    for ins in instrucciones:
        if ins[0] == 'declarar':
            _, tipo, nombre, expr = ins
            valor = evaluar(expr, tabla) if expr else TIPOS[tipo]()
            tabla[nombre] = (tipo, TIPOS[tipo](valor))
        elif ins[0] == 'asignar':
            _, nombre, expr = ins
            if nombre not in tabla:
                raise Exception("Error semántico: la variable '%s' no está declarada" % nombre)
            tipo = tabla[nombre][0]
            tabla[nombre] = (tipo, TIPOS[tipo](evaluar(expr, tabla)))
        elif ins[0] == 'mostrar':
            valor = evaluar(ins[1], tabla)
            if type(valor) is bool:
                valor = 'real' if valor else 'ia'
            print(valor)
        elif ins[0] == 'si':
            _, condicion, entonces, sino = ins
            ejecutar(entonces if evaluar(condicion, tabla) else sino, tabla)
        elif ins[0] == 'mientras':
            _, condicion, cuerpo = ins
            vueltas = 0
            while evaluar(condicion, tabla):
                vueltas = _contar(vueltas)
                ejecutar(cuerpo, tabla)
        elif ins[0] == 'para':
            _, inicio, condicion, paso, cuerpo = ins
            ejecutar([inicio], tabla)
            vueltas = 0
            while evaluar(condicion, tabla):
                vueltas = _contar(vueltas)
                ejecutar(cuerpo, tabla)
                ejecutar([paso], tabla)
