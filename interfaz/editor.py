"""Editor de código con números de línea y resaltado de sintaxis.

En interfaz.ui aparece como un QPlainTextEdit promovido a EditorCodigo.
"""
from PySide6.QtCore import QEvent, QRect, QRegularExpression, QSize, Qt
from PySide6.QtGui import QColor, QFont, QPainter, QSyntaxHighlighter, QTextCharFormat
from PySide6.QtWidgets import QPlainTextEdit, QWidget

RESERVADAS = ("pan", "migaja", "cadena", "sospecha", "si_jala", "valio", "insiste", "para",
              "real", "ia")
FUNCIONES = ("invocar",)


def formato(color, negrita=False, cursiva=False):
    f = QTextCharFormat()
    f.setForeground(QColor(color))
    if negrita:
        f.setFontWeight(QFont.Weight.Bold)
    f.setFontItalic(cursiva)
    return f


class Resaltador(QSyntaxHighlighter):
    def __init__(self, documento):
        super().__init__(documento)
        # El orden importa: la última regla gana (los comentarios al final)
        self.reglas = [
            (QRegularExpression(r"\b\d+(\.\d+)?\b"), formato("#2563EB")),
            (QRegularExpression(r"\b(" + "|".join(RESERVADAS) + r")\b"), formato("#1D4ED8")),
            (QRegularExpression(r"\b(" + "|".join(FUNCIONES) + r")\b"), formato("#7C3AED")),
            (QRegularExpression(r'"[^"]*"'), formato("#B45309")),
            (QRegularExpression(r"//.*"), formato("#15803D", cursiva=True)),
        ]
        self.comentario = formato("#15803D", cursiva=True)

    def highlightBlock(self, texto):
        for patron, fmt in self.reglas:
            coincidencias = patron.globalMatch(texto)
            while coincidencias.hasNext():
                m = coincidencias.next()
                self.setFormat(m.capturedStart(), m.capturedLength(), fmt)

        # Comentarios /* ... */ que pueden abarcar varias líneas (estado 1 = comentario abierto)
        self.setCurrentBlockState(0)
        inicio = 0 if self.previousBlockState() == 1 else texto.find("/*")
        while inicio >= 0:
            fin = texto.find("*/", inicio + (0 if self.previousBlockState() == 1 and inicio == 0 else 2))
            if fin < 0:
                self.setCurrentBlockState(1)
                self.setFormat(inicio, len(texto) - inicio, self.comentario)
                break
            self.setFormat(inicio, fin + 2 - inicio, self.comentario)
            inicio = texto.find("/*", fin + 2)


class _AreaNumeros(QWidget):
    def __init__(self, editor):
        super().__init__(editor)
        self.editor = editor

    def sizeHint(self):
        return QSize(self.editor.ancho_numeros(), 0)

    def paintEvent(self, evento):
        self.editor.pintar_numeros(evento)


class EditorCodigo(QPlainTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.numeros = _AreaNumeros(self)
        self.resaltador = Resaltador(self.document())
        self.setLineWrapMode(QPlainTextEdit.LineWrapMode.NoWrap)
        self.blockCountChanged.connect(self._actualizar_margen)
        self.updateRequest.connect(self._actualizar_area)
        self._actualizar_margen()

    def ancho_numeros(self):
        digitos = max(2, len(str(self.blockCount())))
        return self.fontMetrics().horizontalAdvance("9" * digitos) + 26

    def _actualizar_margen(self, _=0):
        self.setViewportMargins(self.ancho_numeros(), 0, 0, 0)

    def _actualizar_area(self, rect, dy):
        if dy:
            self.numeros.scroll(0, dy)
        else:
            self.numeros.update(0, rect.y(), self.numeros.width(), rect.height())
        if rect.contains(self.viewport().rect()):
            self._actualizar_margen()

    def resizeEvent(self, evento):
        super().resizeEvent(evento)
        r = self.contentsRect()
        self.numeros.setGeometry(QRect(r.left(), r.top(), self.ancho_numeros(), r.height()))

    def changeEvent(self, evento):
        super().changeEvent(evento)
        if evento.type() == QEvent.Type.FontChange:
            self._actualizar_margen()

    def keyPressEvent(self, evento):
        if evento.key() == Qt.Key.Key_Tab:
            self.insertPlainText("    ")  # tabulador = 4 espacios
        else:
            super().keyPressEvent(evento)

    def pintar_numeros(self, evento):
        p = QPainter(self.numeros)
        p.setPen(QColor("#64748B"))
        p.setFont(self.font())
        bloque = self.firstVisibleBlock()
        numero = bloque.blockNumber()
        arriba = round(self.blockBoundingGeometry(bloque).translated(self.contentOffset()).top())
        abajo = arriba + round(self.blockBoundingRect(bloque).height())
        ancho = self.numeros.width() - 14
        while bloque.isValid() and arriba <= evento.rect().bottom():
            if bloque.isVisible() and abajo >= evento.rect().top():
                p.drawText(0, arriba, ancho, self.fontMetrics().height(),
                           Qt.AlignmentFlag.AlignRight, f"{numero + 1:02d}")
            bloque = bloque.next()
            arriba = abajo
            abajo = arriba + round(self.blockBoundingRect(bloque).height())
            numero += 1
        p.end()
