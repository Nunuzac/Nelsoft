#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui


class SetFotosGUI(QtGui.QWidget):
    
    def __init__(self, setn):
        super(SetFotosGUI, self).__init__()
        self.btnar = QtGui.QPushButton(self)
        self.btnab = QtGui.QPushButton(self)
        self.btnde = QtGui.QPushButton(self)
        self.btniz = QtGui.QPushButton(self)
        self.btnld = QtGui.QPushButton(self)
        self.btnsg = QtGui.QPushButton(self)
        self.btncl = QtGui.QPushButton(self)
        self.btnan = QtGui.QPushButton(self)
        self.btnms = QtGui.QPushButton(self)
        self.btnmn = QtGui.QPushButton(self)
        self.setn = setn
        self.shouldclose = True
        self.initUI()

    def initUI(self):
        self.setFixedSize(382, 220)
        self.move(100, 100)
        self.setWindowTitle('NelSoft - Toma de secuencia ' + str(self.setn))

        self.btnar.setText("Arriba")
        self.btnar.setToolTip(u'Subir cámara')
        self.btnar.resize(85, 30)
        self.btnar.move(125, 20)

        self.btnld.setText("LEDS")
        self.btnld.setToolTip('Encender / apagar LEDS')
        self.btnld.resize(85, 30)
        self.btnld.move(125, 70)

        self.btnab.setText('Abajo')
        self.btnab.setToolTip(u'Bajar cámara')
        self.btnab.resize(85, 30)
        self.btnab.move(125, 120)

        self.btniz.setText('Izquierda')
        self.btniz.setToolTip('Rotar a la izquierda')
        self.btniz.resize(85, 30)
        self.btniz.move(20, 70)

        self.btnde.setText('Derecha')
        self.btnde.setToolTip('Rotar a la derecha')
        self.btnde.resize(85, 30)
        self.btnde.move(230, 70)

        self.btnan.setText('Anterior')
        self.btnan.setToolTip('Volver')
        self.btnan.resize(85, 30)
        self.btnan.move(31, 170)

        self.btnsg.setText('Siguiente')
        self.btnsg.setToolTip(u'Iniciar reconstrucción')
        self.btnsg.resize(85, 30)
        self.btnsg.move(147, 170)

        self.btncl.setText('Cancelar')
        self.btncl.setToolTip('Cancelar')
        self.btncl.resize(85, 30)
        self.btncl.move(263, 170)

        self.btnms.setText('+')
        self.btnms.setToolTip('Subir enfoque')
        self.btnms.resize(27, 27)
        self.btnms.move(335, 57)

        self.btnmn.setText('-')
        self.btnmn.setToolTip('Bajar enfoque')
        self.btnmn.resize(27, 27)
        self.btnmn.move(335, 87)


class SelectorArchivoGUI(QtGui.QWidget):
    
    def __init__(self, path, fotosets, tperph):
        super(SelectorArchivoGUI, self).__init__()
        self.path = path
        self.fotosets = fotosets
        self.tperph = tperph
        self.txtpath = QtGui.QLineEdit(self)
        self.btnpath = QtGui.QPushButton(self)
        self.labdescr = QtGui.QLabel(self)
        self.labpath = QtGui.QLabel(self)
        self.labsets = QtGui.QLabel(self)
        self.labtpph = QtGui.QLabel(self)
        self.cbxtpph = QtGui.QComboBox(self)
        self.txtsets = QtGui.QLineEdit(self)
        self.btnsig = QtGui.QPushButton(self)
        self.btncan = QtGui.QPushButton(self)

        self.initUI()

    def initUI(self):
        self.setFixedSize(615, 178)
        self.move(100, 100)
        self.setWindowTitle('NelSoft - selector de directorio de proyecto')

        self.labdescr.setText('Por favor seleccione el directorio para el ' +
                              u'proyecto y el número de sets por capturar')
        self.labdescr.resize(self.labdescr.sizeHint())
        self.labdescr.move(20, 20)

        self.labpath.setText('Directorio del proyecto:')
        self.labpath.resize(self.labpath.sizeHint())
        self.labpath.move(20, 57)

        self.txtpath.setText(self.path)
        self.txtpath.resize(349, 27)
        self.txtpath.move(200, 53)

        self.btnpath.setText('...')
        self.btnpath.resize(27, 27)
        self.btnpath.move(568, 53)

        self.labsets.setText(u'Número de sets:')
        self.labsets.resize(self.labpath.sizeHint())
        self.labsets.move(20, 94)
        
        self.txtsets.setText(self.fotosets)
        self.txtsets.resize(40, 27)
        self.txtsets.move(200, 90)
        
        self.labtpph.setText(u'Fotos por set:')
        self.labtpph.resize(self.labpath.sizeHint())
        self.labtpph.move(300, 94)
        
        self.cbxtpph.move(450, 90)
        self.cbxtpph.addItem("10", 0)
        self.cbxtpph.addItem("20", 1)
        self.cbxtpph.addItem("44", 2)
        self.cbxtpph.addItem("55", 3)
        self.cbxtpph.setCurrentIndex(self.tperph)

        self.btnsig.setText('Siguiente')
        self.btnsig.resize(85, 27)
        self.btnsig.move(188, 131)

        self.btncan.setText('Cancelar')
        self.btncan.resize(85, 27)
        self.btncan.move(341, 131)


class ResultadoGUI(QtGui.QWidget):

    def __init__(self):
        super(ResultadoGUI, self).__init__()
        self.labdescr = QtGui.QLabel(self)
        self.boxsalida = QtGui.QTextEdit(self)
        self.btncl = QtGui.QPushButton(self)
        self.initUI()

    def initUI(self):
        self.setFixedSize(1000, 600)
        self.move(100, 100)
        self.setWindowTitle(u'Procesando imágenes')

        self.labdescr.setText('Salida del pipeline:')
        self.labdescr.move(20, 20)

        self.boxsalida.move(20, 57)
        self.boxsalida.resize(960, 523)
        self.boxsalida.setReadOnly(True)

        self.btncl.setText('Cancelar')
        self.btncl.resize(85, 27)
        self.btncl.move(835, 835)
    
    def agregarLinea(self, text):
        cursor = self.boxsalida.textCursor()
        cursor.movePosition(QtGui.QTextCursor.End)
        cursor.insertText(text)
        self.boxsalida.ensureCursorVisible()
        cursor.movePosition(QtGui.QTextCursor.End)
        self.boxsalida.repaint()


class CapturandoGUI(QtGui.QWidget):

    def __init__(self, numcap):
        super(CapturandoGUI, self).__init__()
        self.labdescr = QtGui.QLabel(self)
        self.numcap = numcap
        self.initUI()

    def initUI(self):
        self.setFixedSize(220, 65)
        self.move(100, 300)
        self.setWindowTitle('Capturando')

        self.labdescr.setText('Tomando foto ')
        self.labdescr.move(20, 20)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.labdescr.setFont(font)

    def actualizarLabel(self, text):
        self.labdescr.setText('Tomando foto ' + str(text))
        self.labdescr.resize(self.labdescr.sizeHint())
        self.repaint()


class PopUpsGUI():

    def __init__(self, titulo, texto, info, tipo):
        self.titulo = titulo
        self.texto = texto
        self.info = info
        self.tipo = tipo
        if self.tipo in [1, 2]:
            self.resultado = self.mostrarSencillo(self.titulo, self.texto,
                             self.info, self.tipo)
        elif self.tipo == 3:
            self.resultado = self.mostrarDoble(self.titulo, self.texto,
                             self.info)
        else:
            self.resultado = False

    def mostrarSencillo(self, titulo, texto, info, tipo):
        msg = QtGui.QMessageBox()

        if tipo == 1:
            msg.setIcon(QtGui.QMessageBox.Warning)
        else:
            msg.setIcon(QtGui.QMessageBox.Information)

        msg.setText(texto)
        msg.setInformativeText(info)
        msg.setWindowTitle(titulo)
        msg.setStandardButtons(QtGui.QMessageBox.Ok)
        msg.show()
        ret = msg.exec_()
        str(ret)
        return False

    def mostrarDoble(self, titulo, texto, info):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Information)
        msg.setText(texto)
        msg.setInformativeText(info)
        msg.setWindowTitle(titulo)
        msg.setStandardButtons(QtGui.QMessageBox.No | QtGui.QMessageBox.Yes)
        msg.show()
        ret = msg.exec_()

        if ret == QtGui.QMessageBox.No:
            return False
        elif ret == QtGui.QMessageBox.Yes:
            return True