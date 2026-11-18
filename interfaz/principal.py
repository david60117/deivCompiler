# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'interfaz.ui'
##
## Created by: Qt User Interface Compiler version 6.12.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QFrame, QHBoxLayout, QLabel,
    QListWidget, QListWidgetItem, QMainWindow, QPlainTextEdit,
    QPushButton, QSizePolicy, QSpacerItem, QToolButton,
    QVBoxLayout, QWidget)

from interfaz.editor import EditorCodigo

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 860)
        MainWindow.setMinimumSize(QSize(1000, 680))
        self.central = QWidget(MainWindow)
        self.central.setObjectName(u"central")
        self.layoutCentral = QVBoxLayout(self.central)
        self.layoutCentral.setSpacing(0)
        self.layoutCentral.setObjectName(u"layoutCentral")
        self.layoutCentral.setContentsMargins(0, 0, 0, 0)
        self.encabezado = QFrame(self.central)
        self.encabezado.setObjectName(u"encabezado")
        self.layoutEncabezado = QVBoxLayout(self.encabezado)
        self.layoutEncabezado.setSpacing(9)
        self.layoutEncabezado.setObjectName(u"layoutEncabezado")
        self.layoutEncabezado.setContentsMargins(18, 12, 18, 10)
        self.layoutTitulo = QHBoxLayout()
        self.layoutTitulo.setSpacing(8)
        self.layoutTitulo.setObjectName(u"layoutTitulo")
        self.layoutTitulo.setContentsMargins(0, 0, 0, 0)
        self.iconoApp = QLabel(self.encabezado)
        self.iconoApp.setObjectName(u"iconoApp")

        self.layoutTitulo.addWidget(self.iconoApp)

        self.titulo = QLabel(self.encabezado)
        self.titulo.setObjectName(u"titulo")

        self.layoutTitulo.addWidget(self.titulo)

        self.espacioTitulo = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutTitulo.addItem(self.espacioTitulo)

        self.indicadorEstado = QLabel(self.encabezado)
        self.indicadorEstado.setObjectName(u"indicadorEstado")

        self.layoutTitulo.addWidget(self.indicadorEstado)


        self.layoutEncabezado.addLayout(self.layoutTitulo)

        self.layoutAcciones = QHBoxLayout()
        self.layoutAcciones.setSpacing(10)
        self.layoutAcciones.setObjectName(u"layoutAcciones")
        self.layoutAcciones.setContentsMargins(0, 0, 0, 0)
        self.btnNuevo = QPushButton(self.encabezado)
        self.btnNuevo.setObjectName(u"btnNuevo")
        self.btnNuevo.setIconSize(QSize(18, 18))
        self.btnNuevo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnNuevo)

        self.btnAbrir = QPushButton(self.encabezado)
        self.btnAbrir.setObjectName(u"btnAbrir")
        self.btnAbrir.setIconSize(QSize(18, 18))
        self.btnAbrir.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnAbrir)

        self.btnGuardar = QPushButton(self.encabezado)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setIconSize(QSize(18, 18))
        self.btnGuardar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnGuardar)

        self.btnCopiar = QPushButton(self.encabezado)
        self.btnCopiar.setObjectName(u"btnCopiar")
        self.btnCopiar.setIconSize(QSize(18, 18))
        self.btnCopiar.setFocusPolicy(Qt.NoFocus)
        self.btnCopiar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnCopiar)

        self.btnPegar = QPushButton(self.encabezado)
        self.btnPegar.setObjectName(u"btnPegar")
        self.btnPegar.setIconSize(QSize(18, 18))
        self.btnPegar.setFocusPolicy(Qt.NoFocus)
        self.btnPegar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnPegar)

        self.separadorAcciones = QFrame(self.encabezado)
        self.separadorAcciones.setObjectName(u"separadorAcciones")
        self.separadorAcciones.setMaximumSize(QSize(16777215, 30))
        self.separadorAcciones.setFrameShape(QFrame.VLine)

        self.layoutAcciones.addWidget(self.separadorAcciones)

        self.espacioAcciones = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutAcciones.addItem(self.espacioAcciones)

        self.btnLexico = QPushButton(self.encabezado)
        self.btnLexico.setObjectName(u"btnLexico")
        self.btnLexico.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnLexico)

        self.btnSintactico = QPushButton(self.encabezado)
        self.btnSintactico.setObjectName(u"btnSintactico")
        self.btnSintactico.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnSintactico)

        self.btnSemantico = QPushButton(self.encabezado)
        self.btnSemantico.setObjectName(u"btnSemantico")
        self.btnSemantico.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnSemantico)

        self.btnGenerarCodigo = QPushButton(self.encabezado)
        self.btnGenerarCodigo.setObjectName(u"btnGenerarCodigo")
        self.btnGenerarCodigo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnGenerarCodigo)

        self.btnEjecutar = QPushButton(self.encabezado)
        self.btnEjecutar.setObjectName(u"btnEjecutar")
        self.btnEjecutar.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutAcciones.addWidget(self.btnEjecutar)


        self.layoutEncabezado.addLayout(self.layoutAcciones)


        self.layoutCentral.addWidget(self.encabezado)

        self.areaTrabajo = QWidget(self.central)
        self.areaTrabajo.setObjectName(u"areaTrabajo")
        self.layoutAreaTrabajo = QHBoxLayout(self.areaTrabajo)
        self.layoutAreaTrabajo.setSpacing(0)
        self.layoutAreaTrabajo.setObjectName(u"layoutAreaTrabajo")
        self.layoutAreaTrabajo.setContentsMargins(0, 0, 0, 0)
        self.explorador = QFrame(self.areaTrabajo)
        self.explorador.setObjectName(u"explorador")
        self.explorador.setMinimumSize(QSize(170, 0))
        self.explorador.setMaximumSize(QSize(170, 16777215))
        self.layoutExplorador = QVBoxLayout(self.explorador)
        self.layoutExplorador.setSpacing(8)
        self.layoutExplorador.setObjectName(u"layoutExplorador")
        self.layoutExplorador.setContentsMargins(10, 12, 10, 10)
        self.tituloArchivos = QLabel(self.explorador)
        self.tituloArchivos.setObjectName(u"tituloArchivos")

        self.layoutExplorador.addWidget(self.tituloArchivos)

        self.listaArchivos = QListWidget(self.explorador)
        QListWidgetItem(self.listaArchivos)
        self.listaArchivos.setObjectName(u"listaArchivos")

        self.layoutExplorador.addWidget(self.listaArchivos)


        self.layoutAreaTrabajo.addWidget(self.explorador)

        self.zonaEditor = QWidget(self.areaTrabajo)
        self.zonaEditor.setObjectName(u"zonaEditor")
        self.layoutZonaEditor = QVBoxLayout(self.zonaEditor)
        self.layoutZonaEditor.setSpacing(8)
        self.layoutZonaEditor.setObjectName(u"layoutZonaEditor")
        self.layoutZonaEditor.setContentsMargins(12, 10, 12, 10)
        self.layoutPestana = QHBoxLayout()
        self.layoutPestana.setSpacing(0)
        self.layoutPestana.setObjectName(u"layoutPestana")
        self.layoutPestana.setContentsMargins(0, 0, 0, 0)
        self.archivoActual = QLabel(self.zonaEditor)
        self.archivoActual.setObjectName(u"archivoActual")

        self.layoutPestana.addWidget(self.archivoActual)

        self.espacioPestana = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutPestana.addItem(self.espacioPestana)

        self.etiquetaEditor = QLabel(self.zonaEditor)
        self.etiquetaEditor.setObjectName(u"etiquetaEditor")

        self.layoutPestana.addWidget(self.etiquetaEditor)


        self.layoutZonaEditor.addLayout(self.layoutPestana)

        self.editor = EditorCodigo(self.zonaEditor)
        self.editor.setObjectName(u"editor")

        self.layoutZonaEditor.addWidget(self.editor)


        self.layoutAreaTrabajo.addWidget(self.zonaEditor)

        self.layoutAreaTrabajo.setStretch(1, 1)

        self.layoutCentral.addWidget(self.areaTrabajo)

        self.panelesInferiores = QWidget(self.central)
        self.panelesInferiores.setObjectName(u"panelesInferiores")
        self.layoutPanelesInferiores = QVBoxLayout(self.panelesInferiores)
        self.layoutPanelesInferiores.setSpacing(9)
        self.layoutPanelesInferiores.setObjectName(u"layoutPanelesInferiores")
        self.layoutPanelesInferiores.setContentsMargins(10, 4, 10, 10)
        self.diagnostico = QFrame(self.panelesInferiores)
        self.diagnostico.setObjectName(u"diagnostico")
        self.layoutDiagnostico = QVBoxLayout(self.diagnostico)
        self.layoutDiagnostico.setSpacing(7)
        self.layoutDiagnostico.setObjectName(u"layoutDiagnostico")
        self.layoutDiagnostico.setContentsMargins(18, 12, 18, 14)
        self.layoutCabeceraDiagnostico = QHBoxLayout()
        self.layoutCabeceraDiagnostico.setSpacing(0)
        self.layoutCabeceraDiagnostico.setObjectName(u"layoutCabeceraDiagnostico")
        self.layoutCabeceraDiagnostico.setContentsMargins(0, 0, 0, 0)
        self.tituloDiagnostico = QLabel(self.diagnostico)
        self.tituloDiagnostico.setObjectName(u"tituloDiagnostico")

        self.layoutCabeceraDiagnostico.addWidget(self.tituloDiagnostico)

        self.espacioDiagnostico = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutCabeceraDiagnostico.addItem(self.espacioDiagnostico)

        self.indicadorAnalisis = QLabel(self.diagnostico)
        self.indicadorAnalisis.setObjectName(u"indicadorAnalisis")

        self.layoutCabeceraDiagnostico.addWidget(self.indicadorAnalisis)


        self.layoutDiagnostico.addLayout(self.layoutCabeceraDiagnostico)

        self.layoutFaseLexico = QHBoxLayout()
        self.layoutFaseLexico.setSpacing(10)
        self.layoutFaseLexico.setObjectName(u"layoutFaseLexico")
        self.layoutFaseLexico.setContentsMargins(0, 0, 0, 0)
        self.checkLexico = QLabel(self.diagnostico)
        self.checkLexico.setObjectName(u"checkLexico")
        self.checkLexico.setAlignment(Qt.AlignCenter)

        self.layoutFaseLexico.addWidget(self.checkLexico)

        self.textoLexico = QLabel(self.diagnostico)
        self.textoLexico.setObjectName(u"textoLexico")

        self.layoutFaseLexico.addWidget(self.textoLexico)

        self.espacioFaseLexico = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutFaseLexico.addItem(self.espacioFaseLexico)


        self.layoutDiagnostico.addLayout(self.layoutFaseLexico)

        self.layoutFaseSintactico = QHBoxLayout()
        self.layoutFaseSintactico.setSpacing(10)
        self.layoutFaseSintactico.setObjectName(u"layoutFaseSintactico")
        self.layoutFaseSintactico.setContentsMargins(0, 0, 0, 0)
        self.checkSintactico = QLabel(self.diagnostico)
        self.checkSintactico.setObjectName(u"checkSintactico")
        self.checkSintactico.setAlignment(Qt.AlignCenter)

        self.layoutFaseSintactico.addWidget(self.checkSintactico)

        self.textoSintactico = QLabel(self.diagnostico)
        self.textoSintactico.setObjectName(u"textoSintactico")

        self.layoutFaseSintactico.addWidget(self.textoSintactico)

        self.espacioFaseSintactico = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutFaseSintactico.addItem(self.espacioFaseSintactico)


        self.layoutDiagnostico.addLayout(self.layoutFaseSintactico)

        self.layoutFaseSemantico = QHBoxLayout()
        self.layoutFaseSemantico.setSpacing(10)
        self.layoutFaseSemantico.setObjectName(u"layoutFaseSemantico")
        self.layoutFaseSemantico.setContentsMargins(0, 0, 0, 0)
        self.checkSemantico = QLabel(self.diagnostico)
        self.checkSemantico.setObjectName(u"checkSemantico")
        self.checkSemantico.setAlignment(Qt.AlignCenter)

        self.layoutFaseSemantico.addWidget(self.checkSemantico)

        self.textoSemantico = QLabel(self.diagnostico)
        self.textoSemantico.setObjectName(u"textoSemantico")

        self.layoutFaseSemantico.addWidget(self.textoSemantico)

        self.espacioFaseSemantico = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutFaseSemantico.addItem(self.espacioFaseSemantico)


        self.layoutDiagnostico.addLayout(self.layoutFaseSemantico)

        self.layoutFaseCodigo = QHBoxLayout()
        self.layoutFaseCodigo.setSpacing(10)
        self.layoutFaseCodigo.setObjectName(u"layoutFaseCodigo")
        self.layoutFaseCodigo.setContentsMargins(0, 0, 0, 0)
        self.checkCodigo = QLabel(self.diagnostico)
        self.checkCodigo.setObjectName(u"checkCodigo")
        self.checkCodigo.setAlignment(Qt.AlignCenter)

        self.layoutFaseCodigo.addWidget(self.checkCodigo)

        self.textoCodigo = QLabel(self.diagnostico)
        self.textoCodigo.setObjectName(u"textoCodigo")

        self.layoutFaseCodigo.addWidget(self.textoCodigo)

        self.espacioFaseCodigo = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutFaseCodigo.addItem(self.espacioFaseCodigo)


        self.layoutDiagnostico.addLayout(self.layoutFaseCodigo)


        self.layoutPanelesInferiores.addWidget(self.diagnostico)

        self.consola = QFrame(self.panelesInferiores)
        self.consola.setObjectName(u"consola")
        self.layoutConsola = QVBoxLayout(self.consola)
        self.layoutConsola.setSpacing(6)
        self.layoutConsola.setObjectName(u"layoutConsola")
        self.layoutConsola.setContentsMargins(15, 12, 15, 14)
        self.layoutCabeceraConsola = QHBoxLayout()
        self.layoutCabeceraConsola.setSpacing(0)
        self.layoutCabeceraConsola.setObjectName(u"layoutCabeceraConsola")
        self.layoutCabeceraConsola.setContentsMargins(0, 0, 0, 0)
        self.tituloConsola = QLabel(self.consola)
        self.tituloConsola.setObjectName(u"tituloConsola")

        self.layoutCabeceraConsola.addWidget(self.tituloConsola)

        self.espacioConsola = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)

        self.layoutCabeceraConsola.addItem(self.espacioConsola)

        self.btnCerrarConsola = QToolButton(self.consola)
        self.btnCerrarConsola.setObjectName(u"btnCerrarConsola")
        self.btnCerrarConsola.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.layoutCabeceraConsola.addWidget(self.btnCerrarConsola)


        self.layoutConsola.addLayout(self.layoutCabeceraConsola)

        self.salida = QPlainTextEdit(self.consola)
        self.salida.setObjectName(u"salida")
        self.salida.setReadOnly(True)
        self.salida.setLineWrapMode(QPlainTextEdit.NoWrap)

        self.layoutConsola.addWidget(self.salida)

        self.mensaje = QLabel(self.consola)
        self.mensaje.setObjectName(u"mensaje")

        self.layoutConsola.addWidget(self.mensaje)


        self.layoutPanelesInferiores.addWidget(self.consola)


        self.layoutCentral.addWidget(self.panelesInferiores)

        self.layoutCentral.setStretch(1, 1)
        MainWindow.setCentralWidget(self.central)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"Compiler Studio", None))
        self.iconoApp.setText(QCoreApplication.translate("MainWindow", u"</>", None))
        self.titulo.setText(QCoreApplication.translate("MainWindow", u"Compiler Studio", None))
        self.indicadorEstado.setText(QCoreApplication.translate("MainWindow", u"Listo", None))
        self.btnNuevo.setText(QCoreApplication.translate("MainWindow", u" Nuevo", None))
        self.btnAbrir.setText(QCoreApplication.translate("MainWindow", u" Abrir", None))
        self.btnGuardar.setText(QCoreApplication.translate("MainWindow", u" Guardar", None))
        self.btnCopiar.setText(QCoreApplication.translate("MainWindow", u" Copiar", None))
        self.btnPegar.setText(QCoreApplication.translate("MainWindow", u" Pegar", None))
        self.btnLexico.setText(QCoreApplication.translate("MainWindow", u"An\u00e1lisis l\u00e9xico", None))
        self.btnLexico.setProperty(u"tipo", QCoreApplication.translate("MainWindow", u"primario", None))
        self.btnSintactico.setText(QCoreApplication.translate("MainWindow", u"An\u00e1lisis sint\u00e1ctico", None))
        self.btnSintactico.setProperty(u"tipo", QCoreApplication.translate("MainWindow", u"primario", None))
        self.btnSemantico.setText(QCoreApplication.translate("MainWindow", u"An\u00e1lisis sem\u00e1ntico", None))
        self.btnSemantico.setProperty(u"tipo", QCoreApplication.translate("MainWindow", u"primario", None))
        self.btnGenerarCodigo.setText(QCoreApplication.translate("MainWindow", u"C\u00f3digo intermedio", None))
        self.btnGenerarCodigo.setProperty(u"tipo", QCoreApplication.translate("MainWindow", u"primario", None))
        self.btnEjecutar.setText(QCoreApplication.translate("MainWindow", u"Ejecutar", None))
        self.btnEjecutar.setProperty(u"tipo", QCoreApplication.translate("MainWindow", u"exito", None))
        self.tituloArchivos.setText(QCoreApplication.translate("MainWindow", u"ARCHIVOS", None))

        __sortingEnabled = self.listaArchivos.isSortingEnabled()
        self.listaArchivos.setSortingEnabled(False)
        ___qlistwidgetitem = self.listaArchivos.item(0)
        ___qlistwidgetitem.setText(QCoreApplication.translate("MainWindow", u"</>  main.deiv", None))
        self.listaArchivos.setSortingEnabled(__sortingEnabled)

        self.archivoActual.setText(QCoreApplication.translate("MainWindow", u"main.deiv", None))
        self.etiquetaEditor.setText(QCoreApplication.translate("MainWindow", u"Editor", None))
        self.tituloDiagnostico.setText(QCoreApplication.translate("MainWindow", u"Diagn\u00f3stico del compilador", None))
        self.indicadorAnalisis.setText(QCoreApplication.translate("MainWindow", u"An\u00e1lisis completado", None))
        self.checkLexico.setText(QCoreApplication.translate("MainWindow", u"\u2713", None))
        self.checkLexico.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"check", None))
        self.textoLexico.setText(QCoreApplication.translate("MainWindow", u"An\u00e1lisis l\u00e9xico completado", None))
        self.textoLexico.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"fase", None))
        self.checkSintactico.setText(QCoreApplication.translate("MainWindow", u"\u2713", None))
        self.checkSintactico.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"check", None))
        self.textoSintactico.setText(QCoreApplication.translate("MainWindow", u"An\u00e1lisis sint\u00e1ctico correcto", None))
        self.textoSintactico.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"fase", None))
        self.checkSemantico.setText(QCoreApplication.translate("MainWindow", u"\u2713", None))
        self.checkSemantico.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"check", None))
        self.textoSemantico.setText(QCoreApplication.translate("MainWindow", u"An\u00e1lisis sem\u00e1ntico correcto", None))
        self.textoSemantico.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"fase", None))
        self.checkCodigo.setText(QCoreApplication.translate("MainWindow", u"\u2713", None))
        self.checkCodigo.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"check", None))
        self.textoCodigo.setText(QCoreApplication.translate("MainWindow", u"C\u00f3digo intermedio generado", None))
        self.textoCodigo.setProperty(u"rol", QCoreApplication.translate("MainWindow", u"fase", None))
        self.tituloConsola.setText(QCoreApplication.translate("MainWindow", u"CONSOLA DE SALIDA", None))
        self.btnCerrarConsola.setText(QCoreApplication.translate("MainWindow", u"\u2715", None))
#if QT_CONFIG(tooltip)
        self.btnCerrarConsola.setToolTip(QCoreApplication.translate("MainWindow", u"Cerrar consola", None))
#endif // QT_CONFIG(tooltip)
        self.mensaje.setText("")
    # retranslateUi

