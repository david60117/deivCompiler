import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from pprint import pformat

from PySide6.QtCore import QEasingCurve, QEvent, QPropertyAnimation, Qt
from PySide6.QtGui import QFont, QFontDatabase, QIcon, QKeySequence, QShortcut, QTextCursor, QTextDocument
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QLineEdit,
    QMessageBox
)

from compilador import generacion, interprete, lexico, semantico, sintactico
from interfaz.principal import Ui_MainWindow

CARPETA = Path(__file__).resolve().parent
FILTRO_ARCHIVOS = "Código Deiv (*.deiv)"
LINEAS_CONSOLA = 8      # alto máximo de la consola; si hay más líneas aparece el deslizador


def elegir_fuente(opciones, respaldo):
    disponibles = set(QFontDatabase.families())
    return next((f for f in opciones if f in disponibles), respaldo)


def repintar(widget):
    """Vuelve a aplicar el QSS después de cambiar una propiedad dinámica."""
    widget.style().unpolish(widget)
    widget.style().polish(widget)


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        self.setWindowTitle("Compiler Studio")
        self.archivo_actual = None      # None = main.deiv sin guardar
        self.arbol = None               # árbol del análisis sintáctico
        self.completadas = 0            # cuántas fases seguidas han pasado

        mono = elegir_fuente(("JetBrains Mono", "Menlo", "Consolas", "DejaVu Sans Mono"), "Courier New")
        for widget in (self.editor, self.salida):
            fuente = widget.font()
            fuente.setFamily(mono)
            widget.setFont(fuente)

        # Iconos de la barra de herramientas (interfaz/iconos/*.svg)
        for boton, icono in ((self.btnNuevo, "nuevo"), (self.btnAbrir, "abrir"), (self.btnGuardar, "guardar"),
                             (self.btnCopiar, "copiar"), (self.btnPegar, "pegar"), (self.btnBuscar, "buscar")):
            boton.setIcon(QIcon(str(CARPETA / "interfaz" / "iconos" / f"{icono}.svg")))

        # Búsqueda: la lupa se despliega en una barra y se vuelve a ocultar cuando ya no se usa
        self.campoBuscar.addAction(self.btnBuscar.icon(), QLineEdit.ActionPosition.LeadingPosition)
        self.campoBuscar.installEventFilter(self)
        self.animacionBuscar = QPropertyAnimation(self.cajaBuscar, b"maximumWidth", self)
        self.animacionBuscar.setDuration(180)
        self.animacionBuscar.setEasingCurve(QEasingCurve.Type.OutCubic)
        self.animacionBuscar.finished.connect(lambda: self.cajaBuscar.setMaximumWidth(16777215))

        # Botones de fase y filas del diagnóstico (icono, texto), en el mismo orden
        self.botones_fase = [self.btnLexico, self.btnSintactico, self.btnSemantico, self.btnGenerarCodigo]
        self.fases = [(self.checkLexico, self.textoLexico),
                      (self.checkSintactico, self.textoSintactico),
                      (self.checkSemantico, self.textoSemantico),
                      (self.checkCodigo, self.textoCodigo)]

        self.btnNuevo.clicked.connect(self.nuevo_archivo)
        self.btnAbrir.clicked.connect(self.abrir_archivo)
        self.btnGuardar.clicked.connect(self.guardar_archivo)
        self.btnCopiar.clicked.connect(self.copiar)
        self.btnPegar.clicked.connect(self.pegar)
        self.btnBuscar.clicked.connect(self.mostrar_buscar)
        self.campoBuscar.textChanged.connect(self.buscar_al_escribir)
        self.btnBuscarSiguiente.clicked.connect(self.buscar_siguiente)
        self.btnBuscarAnterior.clicked.connect(self.buscar_anterior)
        QShortcut(QKeySequence.StandardKey.Find, self).activated.connect(self.mostrar_buscar)   # Cmd+F / Ctrl+F
        self.btnLexico.clicked.connect(self.analisis_lexico)
        self.btnSintactico.clicked.connect(self.analisis_sintactico)
        self.btnSemantico.clicked.connect(self.analisis_semantico)
        self.btnGenerarCodigo.clicked.connect(self.codigo_intermedio)
        self.btnEjecutar.clicked.connect(self.ejecutar)
        self.btnCerrarConsola.clicked.connect(self.ocultar_consola)
        self.editor.textChanged.connect(self.codigo_modificado)

        self.listaArchivos.setCurrentRow(0)
        self.reiniciar_diagnostico()
        self.ocultar_consola()
        self.cajaBuscar.hide()
        self.actualizar_botones()

        pantalla = self.screen().availableGeometry()
        self.resize(min(1440, pantalla.width() - 40), min(860, pantalla.height() - 40))

    # ---------------- Archivos ----------------
    def poner_nombre(self, nombre):
        self.archivoActual.setText(nombre)
        self.listaArchivos.item(0).setText("</>  " + nombre)

    def nuevo_archivo(self):
        self.editor.clear()
        self.archivo_actual = None
        self.poner_nombre("main.deiv")
        self.ocultar_consola()

    def abrir_archivo(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Abrir archivo",
            "",
            FILTRO_ARCHIVOS
        )

        if not archivo:
            return
        if not archivo.lower().endswith(".deiv"):
            QMessageBox.warning(self, "Abrir archivo", "Solo se pueden abrir archivos .deiv")
            return

        try:
            with open(archivo, "r", encoding="utf-8") as f:
                contenido = f.read()
        except (OSError, UnicodeDecodeError) as error:
            QMessageBox.warning(self, "Abrir archivo", f"No se pudo abrir el archivo:\n{error}")
            return

        self.editor.setPlainText(contenido)     # reinicia el diagnóstico
        self.archivo_actual = archivo
        self.poner_nombre(Path(archivo).name)
        self.ocultar_consola()

    def guardar_archivo(self):

        archivo = self.archivo_actual
        if not archivo:
            archivo, _ = QFileDialog.getSaveFileName(
                self,
                "Guardar archivo",
                "main.deiv",
                FILTRO_ARCHIVOS
            )
            if archivo and not archivo.lower().endswith(".deiv"):
                archivo += ".deiv"

        if not archivo:
            return

        try:
            with open(archivo, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())
        except OSError as error:
            QMessageBox.warning(self, "Guardar archivo", f"No se pudo guardar el archivo:\n{error}")
            return

        self.archivo_actual = archivo
        self.poner_nombre(Path(archivo).name)

    # ---------------- Edición ----------------
    def copiar(self):
        """Copia lo seleccionado; si no hay selección, copia todo el código."""
        if self.editor.textCursor().hasSelection():
            self.editor.copy()
        else:
            QApplication.clipboard().setText(self.editor.toPlainText())

    def pegar(self):
        """Pega el texto del portapapeles donde está el cursor."""
        self.editor.paste()

    # ---------------- Buscar ----------------
    def mostrar_buscar(self):
        """Despliega la barra de búsqueda a partir de la lupa."""
        if not self.cajaBuscar.isVisible():
            self.btnBuscar.hide()
            self.cajaBuscar.show()
            self.animacionBuscar.setStartValue(0)
            self.animacionBuscar.setEndValue(self.cajaBuscar.sizeHint().width())
            self.animacionBuscar.start()
        self.campoBuscar.setFocus()
        self.campoBuscar.selectAll()

    def ocultar_buscar(self):
        """Regresa a la lupa cuando la búsqueda ya no se usa."""
        self.animacionBuscar.stop()
        self.cajaBuscar.hide()
        self.btnBuscar.show()

    def eventFilter(self, objeto, evento):
        """Teclas de la barra de búsqueda y ocultarla cuando pierde el foco."""
        if objeto is self.campoBuscar:
            if evento.type() == QEvent.Type.KeyPress:
                if evento.key() == Qt.Key.Key_Escape:
                    self.editor.setFocus()      # al perder el foco, la barra se oculta sola
                    return True
                if evento.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                    if evento.modifiers() & Qt.KeyboardModifier.ShiftModifier:
                        self.buscar_anterior()
                    else:
                        self.buscar_siguiente()
                    return True
            elif evento.type() == QEvent.Type.FocusOut and evento.reason() not in (
                    Qt.FocusReason.ActiveWindowFocusReason, Qt.FocusReason.PopupFocusReason):
                self.ocultar_buscar()
        return super().eventFilter(objeto, evento)

    def buscar_al_escribir(self):
        """Mientras se escribe, busca desde el inicio de la coincidencia actual."""
        cursor = self.editor.textCursor()
        cursor.setPosition(cursor.selectionStart())
        self.editor.setTextCursor(cursor)
        self.buscar()

    def buscar_siguiente(self):
        self.buscar()

    def buscar_anterior(self):
        self.buscar(hacia_atras=True)

    def buscar(self, hacia_atras=False):
        """Selecciona la siguiente (o anterior) coincidencia; al llegar al final da la vuelta."""
        texto = self.campoBuscar.text()
        if not texto:
            self.resultadosBuscar.clear()
            return
        opciones = QTextDocument.FindFlag.FindBackward if hacia_atras else QTextDocument.FindFlag(0)
        inicio = self.editor.textCursor()
        if not self.editor.find(texto, opciones):
            cursor = QTextCursor(inicio)
            cursor.movePosition(QTextCursor.MoveOperation.End if hacia_atras else QTextCursor.MoveOperation.Start)
            self.editor.setTextCursor(cursor)
            if not self.editor.find(texto, opciones):
                self.editor.setTextCursor(inicio)      # no hay coincidencias: el cursor se queda donde estaba

        codigo = self.editor.toPlainText().lower()
        total = codigo.count(texto.lower())
        if total == 0:
            self.resultadosBuscar.setText("Sin resultados")
        else:
            actual = codigo[:self.editor.textCursor().selectionStart()].count(texto.lower()) + 1
            self.resultadosBuscar.setText(f"{actual} de {total}")

    # ---------------- Botones y diagnóstico ----------------
    def actualizar_botones(self):
        """Cada fase se activa solo si pasó la anterior; Ejecutar tras el semántico."""
        self.btnLexico.setEnabled(bool(self.editor.toPlainText().strip()))
        for i, boton in enumerate(self.botones_fase[1:], start=1):
            boton.setEnabled(self.completadas >= i)
        self.btnEjecutar.setEnabled(self.completadas >= 3)

    def marcar_fase(self, indice, correcta=True):
        for widget in self.fases[indice]:
            widget.setProperty("marcada", correcta)
            repintar(widget)
        todas = all(check.property("marcada") for check, _ in self.fases)
        self.indicadorAnalisis.setVisible(todas)

    def reiniciar_diagnostico(self, desde=0):
        for i in range(desde, len(self.fases)):
            self.marcar_fase(i, False)

    def codigo_modificado(self):
        """Cualquier cambio en el código invalida las fases anteriores."""
        self.completadas = 0
        self.arbol = None
        self.reiniciar_diagnostico()
        self.actualizar_botones()

    def correr_fase(self, indice, nombre, fase):
        """Ejecuta una fase; fase() regresa (salida, mensaje) o lanza Exception."""
        try:
            salida, mensaje = fase()
        except Exception as error:
            self.completadas = indice
            self.reiniciar_diagnostico(desde=indice)
            self.mostrar_consola(str(error), f"{nombre}: se encontró un error.", error=True)
        else:
            self.completadas = max(self.completadas, indice + 1)
            self.marcar_fase(indice)
            self.mostrar_consola(salida, mensaje)
        self.actualizar_botones()

    # ---------------- Consola de salida ----------------
    def mostrar_consola(self, salida, mensaje="", error=False):
        self.salida.setProperty("error", error)
        repintar(self.salida)
        self.salida.setPlainText(salida)
        lineas = min(salida.count("\n") + 1, LINEAS_CONSOLA)
        alto = self.salida.fontMetrics().lineSpacing() * lineas + 2 * self.salida.document().documentMargin() + 4
        self.salida.setFixedHeight(int(alto))
        self.mensaje.setText(mensaje)
        self.mensaje.setVisible(bool(mensaje))
        self.consola.show()

    def ocultar_consola(self):
        self.consola.hide()

    # ---------------- Fases de compilación ----------------
    def analisis_lexico(self):
        def fase():
            tokens = lexico.analizar_lexico(self.editor.toPlainText())
            filas = ["%-5s %-12s %s" % ("Línea", "Token", "Valor")]
            filas += ["%-5d %-12s %r" % (linea, tipo, valor) for tipo, valor, linea in tokens]
            return "\n".join(filas), f"Análisis léxico correcto: {len(tokens)} tokens."
        self.correr_fase(0, "Análisis léxico", fase)

    def analisis_sintactico(self):
        def fase():
            self.arbol = sintactico.analizar_sintactico(self.editor.toPlainText())
            if not self.arbol:
                raise Exception("Error sintáctico: no hay instrucciones")
            return pformat(self.arbol, width=100), "Análisis sintáctico correcto: árbol generado."
        self.correr_fase(1, "Análisis sintáctico", fase)

    def analisis_semantico(self):
        def fase():
            declaradas = semantico.analizar_semantico(self.arbol)
            lista = ", ".join(sorted(declaradas)) or "(ninguna)"
            return "Variables declaradas: " + lista, "Análisis semántico correcto."
        self.correr_fase(2, "Análisis semántico", fase)

    def codigo_intermedio(self):
        def fase():
            lineas = generacion.generar_codigo(self.arbol)
            return "\n".join(lineas), f"Código intermedio generado: {len(lineas)} instrucciones."
        self.correr_fase(3, "Código intermedio", fase)

    def ejecutar(self):
        captura = io.StringIO()
        try:
            with redirect_stdout(captura):      # lo que imprime "invocar" va a la consola
                interprete.ejecutar(self.arbol, {})
        except Exception as error:
            salida = (captura.getvalue() + str(error)).strip()
            self.mostrar_consola(salida, "La ejecución se detuvo por un error.", error=True)
        else:
            salida = captura.getvalue().rstrip("\n") or "(el programa no mostró nada)"
            self.mostrar_consola(salida, "Proceso finalizado correctamente.")


app = QApplication(sys.argv)
app.setFont(QFont(elegir_fuente(("Inter", "Helvetica Neue", "Segoe UI"), "Arial")))
app.setStyleSheet((CARPETA / "interfaz" / "estilos.qss").read_text(encoding="utf-8"))

window = Window()
window.show()

sys.exit(app.exec())
