# -----------------------------------------------------------------------------
# Fase 4: generación de código intermedio (código de tres direcciones)
# Recorre el árbol del parser y regresa una lista de líneas como:
#     t1 = x + 1
#     if_false t2 goto L1
# -----------------------------------------------------------------------------

VALOR_INICIAL = {'pan': '0', 'migaja': '0.0', 'cadena': '""', 'sospecha': 'ia'}

def generar_codigo(arbol):
    """Regresa la lista de líneas de código de tres direcciones del árbol."""
    codigo = []
    contador = {'t': 0, 'L': 0}

    def nuevo(prefijo):
        contador[prefijo] += 1
        return '%s%d' % (prefijo, contador[prefijo])

    def expresion(e):
        """Emite las líneas de la expresión y regresa la dirección con su resultado."""
        if e[0] == 'valor':
            v = e[1]
            if type(v) is bool:
                return 'real' if v else 'ia'
            if type(v) is str:
                return '"%s"' % v
            return str(v)
        if e[0] == 'id':
            return e[1]
        if e[0] == 'negativo':
            a = expresion(e[1])
            t = nuevo('t')
            codigo.append('%s = -%s' % (t, a))
            return t
        if e[0] == 'not':
            a = expresion(e[1])
            t = nuevo('t')
            codigo.append('%s = !%s' % (t, a))
            return t
        # binaria
        izq = expresion(e[2])
        der = expresion(e[3])
        t = nuevo('t')
        codigo.append('%s = %s %s %s' % (t, izq, e[1], der))
        return t

    def instrucciones(lista):
        for ins in lista:
            if ins[0] == 'declarar':
                _, tipo, nombre, expr = ins
                valor = expresion(expr) if expr else VALOR_INICIAL[tipo]
                codigo.append('%s = %s' % (nombre, valor))
            elif ins[0] == 'asignar':
                _, nombre, expr = ins
                codigo.append('%s = %s' % (nombre, expresion(expr)))
            elif ins[0] == 'mostrar':
                codigo.append('mostrar %s' % expresion(ins[1]))
            elif ins[0] == 'si':
                _, condicion, entonces, sino = ins
                l_sino, l_fin = nuevo('L'), nuevo('L')
                codigo.append('if_false %s goto %s' % (expresion(condicion), l_sino))
                instrucciones(entonces)
                codigo.append('goto %s' % l_fin)
                codigo.append('%s:' % l_sino)
                instrucciones(sino)
                codigo.append('%s:' % l_fin)
            elif ins[0] == 'mientras':
                _, condicion, cuerpo = ins
                l_inicio, l_fin = nuevo('L'), nuevo('L')
                codigo.append('%s:' % l_inicio)
                codigo.append('if_false %s goto %s' % (expresion(condicion), l_fin))
                instrucciones(cuerpo)
                codigo.append('goto %s' % l_inicio)
                codigo.append('%s:' % l_fin)
            elif ins[0] == 'para':
                _, inicio, condicion, paso, cuerpo = ins
                instrucciones([inicio])
                l_inicio, l_fin = nuevo('L'), nuevo('L')
                codigo.append('%s:' % l_inicio)
                codigo.append('if_false %s goto %s' % (expresion(condicion), l_fin))
                instrucciones(cuerpo)
                instrucciones([paso])
                codigo.append('goto %s' % l_inicio)
                codigo.append('%s:' % l_fin)

    instrucciones(arbol)
    return codigo
