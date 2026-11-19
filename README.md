# Deiv Compiler

Compilador del lenguaje **Deiv** con **Compiler Studio**, un editor gráfico hecho en Python con PySide6 (Qt) y PLY. Muestra paso a paso las fases de un compilador: análisis léxico, sintáctico y semántico, generación de código intermedio y ejecución.

## Características

- Editor con números de línea y resaltado de sintaxis.
- Archivos: nuevo, abrir y guardar (`.deiv`).
- Edición: copiar, pegar y buscar (**Ctrl+F** / **Cmd+F**).
- **Análisis léxico:** tabla de tokens con línea, tipo y valor.
- **Análisis sintáctico:** árbol del programa, con un parser LALR generado por PLY.
- **Análisis semántico:** revisa que las variables estén declaradas antes de usarse.
- **Código intermedio:** código de tres direcciones con temporales y etiquetas.
- **Ejecución:** intérprete que corre el programa y muestra su salida.
- Panel de diagnóstico que marca cada fase y mensajes de error con número de línea.

## Requisitos

- Python 3.10 o superior
- Git
- PySide6 (se instala con `requirements.txt`). PLY ya viene incluido en la carpeta `ply/`.

## Instalación y ejecución

### Windows (PowerShell o CMD)

```bat
git clone https://github.com/david60117/deivCompiler.git
cd deivCompiler
py -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

> Si PowerShell no deja activar el entorno ("running scripts is disabled"), ejecuta una vez
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` o usa CMD.

### macOS / Linux

```bash
git clone https://github.com/david60117/deivCompiler.git
cd deivCompiler
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Uso

1. Pulsa **Abrir** y elige `ejemplos/ejemplo.deiv`, o escribe un programa en el editor.
2. Pulsa en orden **Análisis léxico**, **Análisis sintáctico**, **Análisis semántico** y **Código intermedio**. Cada botón se activa cuando la fase anterior termina sin errores.
3. Pulsa **Ejecutar** (disponible después del análisis semántico) para ver la salida del programa.

Cualquier cambio en el código reinicia el diagnóstico.

## El lenguaje Deiv

### Tipos de datos

| Tipo       | Equivale a | Ejemplo                    |
|------------|------------|----------------------------|
| `pan`      | entero     | `pan edad = 20;`           |
| `migaja`   | decimal    | `migaja precio = 9.5;`     |
| `cadena`   | texto      | `cadena saludo = "Hola";`  |
| `sospecha` | booleano   | `sospecha listo = real;`   |

### Palabras reservadas

| Deiv            | Equivalente en C |
|-----------------|------------------|
| `si_jala`       | `if`             |
| `valio`         | `else`           |
| `valio si_jala` | `else if`        |
| `insiste`       | `while`          |
| `para`          | `for`            |
| `invocar`       | `printf`         |
| `real` / `ia`   | `true` / `false` |

### Reglas principales

- Las instrucciones terminan con `;` y los bloques van entre `{ }`.
- Toda variable se declara con su tipo antes de usarse.
- Operadores aritméticos `+ - * / %`, relacionales `< > <= >= == !=` y lógicos `&& || !`, con la precedencia de C.
- La división entre dos `pan` es entera (`7 / 2` da `3`).
- Comentarios con `//` y `/* ... */`.

### Ejemplo

```
/* Factorial de 5 */
pan n = 5;
pan factorial = 1;
insiste (n > 1) {
    factorial = factorial * n;
    n = n - 1;
}
invocar(factorial);          // muestra 120

// Pares del 1 al 10
para (pan i = 1; i <= 10; i = i + 1) {
    si_jala (i % 2 == 0) {
        invocar(i);
    }
}
```

## Estructura del proyecto

```
main.py                  Punto de entrada: ventana y conexión de las fases
requirements.txt         Dependencias (PySide6)
compilador/
    lexico.py            Análisis léxico (tokens y expresiones regulares)
    sintactico.py        Análisis sintáctico (producciones y árbol)
    semantico.py         Análisis semántico (variables declaradas)
    generacion.py        Código intermedio de tres direcciones
    interprete.py        Ejecución del árbol
interfaz/
    interfaz.ui          Diseño de la ventana (Qt Designer)
    principal.py         Clase generada con pyside6-uic
    editor.py            Editor con números de línea y resaltado
    estilos.qss          Estilos de la interfaz
    iconos/              Iconos de la barra de herramientas y de la búsqueda
ejemplos/
    ejemplo.deiv         Programa de prueba
ply/                     Biblioteca PLY (Python Lex-Yacc)
```

## Autor

**David Jonathan Hernández Mejía**. Licenciatura en Ingeniería de Software, Grupo 301.

## Créditos

- [PLY (Python Lex-Yacc)](https://github.com/dabeaz/ply), de David Beazley.
- Iconos de [Lucide](https://lucide.dev) (licencia ISC).
