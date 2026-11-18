import io
import sys
from contextlib import redirect_stdout
from pathlib import Path
from pprint import pformat

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
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

        # Botones de fase y filas del diagnóstico (icono, texto), en el mismo orden
        self.botones_fase = [self.btnLexico, self.btnSintactico, self.btnSemantico, self.btnGenerarCodigo]
        self.fases = [(self.checkLexico, self.textoLexico),
                      (self.checkSintactico, self.textoSintactico),
                      (self.checkSemantico, self.textoSemantico),
                      (self.checkCodigo, self.textoCodigo)]

        self.btnNuevo.clicked.connect(self.nuevo_archivo)
        self.btnAbrir.clicked.connect(self.abrir_archivo)
        self.btnGuardar.clicked.connect(self.guardar_archivo)
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
