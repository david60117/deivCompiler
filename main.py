import sys
from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QFileDialog,
    QMessageBox
)

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

        mono = elegir_fuente(("JetBrains Mono", "Menlo", "Consolas", "DejaVu Sans Mono"), "Courier New")
        for widget in (self.editor, self.salida):
            fuente = widget.font()
            fuente.setFamily(mono)
            widget.setFont(fuente)

        # Filas del diagnóstico (icono, texto), una por fase
        self.fases = [(self.checkLexico, self.textoLexico),
                      (self.checkSintactico, self.textoSintactico),
                      (self.checkSemantico, self.textoSemantico),
                      (self.checkCodigo, self.textoCodigo)]
        # Fases que todavía no están programadas: sus botones se quedan desactivados
        self.pendientes = [self.btnLexico, self.btnSintactico, self.btnSemantico,
                           self.btnGenerarCodigo, self.btnEjecutar]

        self.btnNuevo.clicked.connect(self.nuevo_archivo)
        self.btnAbrir.clicked.connect(self.abrir_archivo)
        self.btnGuardar.clicked.connect(self.guardar_archivo)
        self.btnCerrarConsola.clicked.connect(self.ocultar_consola)

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

        self.editor.setPlainText(contenido)
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
        for boton in self.pendientes:
            boton.setEnabled(False)

    def marcar_fase(self, indice, correcta=True):
        for widget in self.fases[indice]:
            widget.setProperty("marcada", correcta)
            repintar(widget)
        todas = all(check.property("marcada") for check, _ in self.fases)
        self.indicadorAnalisis.setVisible(todas)

    def reiniciar_diagnostico(self, desde=0):
        for i in range(desde, len(self.fases)):
            self.marcar_fase(i, False)

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


app = QApplication(sys.argv)
app.setFont(QFont(elegir_fuente(("Inter", "Helvetica Neue", "Segoe UI"), "Arial")))
app.setStyleSheet((CARPETA / "interfaz" / "estilos.qss").read_text(encoding="utf-8"))

window = Window()
window.show()

sys.exit(app.exec())
