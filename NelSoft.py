#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import binaries.GUI
import binaries.arduino
import os
import shutil
import time
import subprocess

class NelSoft():

    def __init__(self):
        self.subp = None
        self.controlador = None
        self.fotoactual = 0
        self.setactual = 1
        self.fotosets = 3
        self.fotosporset = 10
        self.girosporvuelta = 220
        self.usrpath = os.path.expanduser('~')
        self.proypath = os.path.expanduser('~')
        self.softpath = os.path.expanduser('~') + '/NelSoft'
        self.mvepath = os.path.expanduser('~') + '/binaries/mve/apps'
        self.mvgpath = os.path.expanduser('~') + '/binaries/openMVG_build/' + (
                       'Linux-x86_64-RELEASE')
        self.smvspath = os.path.expanduser('~') + '/binaries/smvs'
        self.texreconpath = os.path.expanduser('~') + (
                            '/binaries/texrecon/build/apps/texrecon')
        self.binpath = os.path.expanduser('~') + '/NelSoft/binaries'
        self.ledsON = False
        self.foldercreado = False
        self.focusactual = 2        
        self.optdict = {0 : 22, 1 : 11, 2: 5, 3 : 4}
        self.cbbxopt = 1
        

    def iniciar(self):
        try:
            p = subprocess.Popen(['v4l2-ctl', '-c', 'focus_auto=0'])
            p.wait()
            focusactual = str(subprocess.check_output(['v4l2-ctl', '-C',
                          'focus_absolute'], shell=False))
            self.focusactual = int(focusactual.replace("focus_absolute: ", ""))
            selector = binaries.GUI.SelectorArchivoGUI(self.proypath,
                         str(self.fotosets), self.cbbxopt)
            selector.show()
            selector.btnpath.clicked.connect(
                lambda: self.actualizarPath(selector.txtpath))
            selector.btncan.clicked.connect(
                lambda: self.cerrarVentana(selector))
            selector.btnsig.clicked.connect(
            lambda: self.validarSelector(selector))
        except:
            binaries.GUI.PopUpsGUI("Error de dispositivo", "Dispositivo"
                + " desconectado", u"La cámara está desconectada, por favor"
                + u"  conéctela y vuelva a intentarlo", 1)

    def continuar(self):
        fotografo = binaries.GUI.SetFotosGUI(self.setactual)
        try:
            self.controlador = binaries.arduino.Controlador()
            fotografo.show()
            self.subp = subprocess.Popen([os.path.join(self.binpath, 
                        'camara')])
            fotografo.btnar.clicked.connect(
                lambda: self.controlador.pasarOrden('a'))
            fotografo.btnab.clicked.connect(
                lambda: self.controlador.pasarOrden('b'))
            fotografo.btnde.clicked.connect(
                lambda: self.controlador.pasarOrden('h'))
            fotografo.btniz.clicked.connect(
                lambda: self.controlador.pasarOrden('g'))
            fotografo.btnld.clicked.connect(
                lambda: self.controlarLuces())
            fotografo.btnan.clicked.connect(
                lambda: self.atras(fotografo))
            fotografo.btnsg.clicked.connect(
                lambda: self.validarFotografo(fotografo))
            fotografo.btncl.clicked.connect(
                lambda: self.cancelar(fotografo))
            fotografo.btnms.clicked.connect(
                lambda: self.controlarEnfoque(1))
            fotografo.btnmn.clicked.connect(
                lambda: self.controlarEnfoque(0))
        except:
            binaries.GUI.PopUpsGUI("Error de dispositivo", "Dispositivo"
                + " desconectado", u"El controlador serial está desconectado"
                + u" por favor conéctelo y vuelva a intentarlo", 1)
            self.atras(fotografo)

    def pipeline(self):
        pipeliner = binaries.GUI.ResultadoGUI()
        pipeliner.btncl.clicked.connect(
            lambda: self.cerrarVentana(pipeliner))
        pipeliner.show()
        
        jsonpath = self.proypath + '/pares/sfm_data.json'
        matchespath = self.proypath + '/pares'
        reconpath = self.proypath + '/recon'
        mvepath = self.proypath + '/MVE'
        
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_SfMInit_ImageListing'), '-i', self.proypath +
            '/fotos', '-o', matchespath, '-d', self.softpath +
            '/resources/sensor_width_camera_database.txt', '-f', '2300'],
            stdout=subprocess.PIPE)
        self.procesar(pipeliner)
                
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_ComputeFeatures'), '-i', jsonpath, '-o', 
            matchespath, '-p', 'ULTRA'], stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_ComputeMatches'), '-i', jsonpath, '-o', matchespath,
            '-g', 'f'], stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_IncrementalSfM'), '-i', jsonpath, '-m',
            matchespath, '-o', reconpath], stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_ComputeSfM_DataColor'), '-i', reconpath + 
            '/sfm_data.bin', '-o', reconpath + '/colorized.ply'], 
            stdout=subprocess.PIPE)        
        
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_ComputeStructureFromKnownPoses'), '-i', reconpath +
            '/sfm_data.bin', '-m', matchespath, '-f', matchespath +
            '/matches.f.bin', '-o', reconpath + '/robust.bin'],
            stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_ComputeSfM_DataColor'), '-i', reconpath +
            '/robust.bin', '-o', reconpath + '/robust_colorized.ply'],
            stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        self.subp = subprocess.Popen([os.path.join(self.mvgpath,
            'openMVG_main_openMVG2MVE2'), '-i', reconpath +
            '/sfm_data.bin', '-o', self.proypath],
            stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        self.subp = subprocess.Popen([os.path.join(self.smvspath, 'smvsrecon'),
            mvepath], stdout=subprocess.PIPE)
        self.procesar(pipeliner)

        self.subp = subprocess.Popen([os.path.join(self.mvepath + '/fssrecon', 
            'fssrecon'), mvepath + '/smvs-B.ply', mvepath + '/surface.ply'], 
            stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        self.subp = subprocess.Popen([os.path.join(self.mvepath + '/meshclean', 
            'meshclean'), mvepath + '/surface.ply', mvepath + '/clean.ply', 
            '-t10', '-c10000'], stdout=subprocess.PIPE)
        self.procesar(pipeliner)
         
        self.subp = subprocess.Popen([os.path.join(self.texreconpath, 
            'texrecon'), mvepath + "::undistorted",  mvepath + '/clean.ply',
            mvepath + '/textured'], stdout=subprocess.PIPE)
        self.procesar(pipeliner)
        
        os.system('meshlab ' + mvepath + '/textured.obj')
        
        self.cerrarVentana(pipeliner)

    def validarFotografo(self, parent):
        parent.close()
        try:
            self.subp.kill()
        except:
            pass        
        monitor = binaries.GUI.CapturandoGUI(self.fotoactual)
        monitor.actualizarLabel(self.fotoactual)        
        self.controlador.pasarOrden('h')
        time.sleep(3)        
        monitor.show()
        sup = self.fotoactual
        inf = self.fotoactual + self.fotosporset                
        os.chdir(self.proypath + '/fotos')
        for i in range(sup, inf):
            monitor.actualizarLabel(self.fotoactual)
            for j in range(0, self.optdict[self.cbbxopt]):                
                self.controlador.pasarOrden('h')
                time.sleep(3)
            p = subprocess.Popen([os.path.join(self.binpath, "capturador"),
                    str(self.fotoactual)])
            p.wait()
            self.fotoactual += 1
        self.setactual += 1
        self.cerrarVentana(monitor)

        if self.setactual != (self.fotosets + 1):
            self.continuar()
        else:
            self.pipeline()

    def validarSelector(self, parent):
        path = parent.txtpath.text()
        try:
            numcaptures = int(parent.txtsets.text())
        except:
            numcaptures = 0
        if numcaptures <= 0 or numcaptures > 10:
            popup = binaries.GUI.PopUpsGUI(u"Error de set", u"Valor no válido",
                    u"Usted ha introducido un valor no válido en el campo" +
                    " correspondiente al numero de sets", 1)
        elif not os.path.isdir(path):
            popup = binaries.GUI.PopUpsGUI("Directorio inexistente",
                    "Directorio inexistente", "El directorio seleccionado " +
                    u"no existe, ¿desea crearlo?", 3)
            crear = popup.resultado
            if crear is True:
                creado = self.crearDirectorios(path, True)
                if creado is True:
                    popup = binaries.GUI.PopUpsGUI(u"Creación exitosa",
                    "Directorio creado", u"El directorio se creó exitosamente" 
                    + " en " + self.proypath, 2)
                    self.fotosets = int(parent.txtsets.text())                    
                    self.cbbxopt = int(parent.cbxtpph.currentIndex());
                    self.fotosporset = self.girosporvuelta / (
                                       self.optdict[self.cbbxopt])
                    self.cerrarVentana(parent)
                    self.continuar()
                else:
                    popup = binaries.GUI.PopUpsGUI("Error de directorio",
                    "Directorio no creado", "El directorio no pudo ser" +
                    " creado en la ubicacion seleccionada", 1)
        else:
            creado = self.crearDirectorios(path, False)
            if creado is True:
                popup = binaries.GUI.PopUpsGUI(u"Folder válido",
                "Continuar proceso", u"El directorio seleccionado es válido," +
                u" el proceso continuará en " + self.proypath, 2)
                self.fotosets = int(parent.txtsets.text())
                self.cbbxopt = int(parent.cbxtpph.currentIndex());
                self.fotosporset = self.girosporvuelta / (
                                   self.optdict[self.cbbxopt])
                self.cerrarVentana(parent)
                self.continuar()
            else:
                popup = binaries.GUI.PopUpsGUI("Error de directorio",
                u"Directorio no válido", "El directorio seleccionado no es" +
                u" válido, por favor seleccione otro", 1)

    def rollBack(self, caller):
        if self.setactual == 1:
            if self.foldercreado is True:
                try:
                    shutil.rmtree(self.proypath)
                    self.foldercreado = False
                except:
                    print('No pude borrar el folder ' + self.proypath)
            else:
                try:
                    os.rmdir('fotos')
                    os.rmdir('pares')
                    os.rmdir('recon')
                    os.rmdir('MVE')
                except:
                    print('No pude borrar el subfolders')
        else:
            lastphoto = (self.setactual - 1) * self.fotosporset - 1
            firstphoto = lastphoto - self.fotosporset
            for i in range(lastphoto, firstphoto, -1):
                try:
                    os.remove(str(i) + '.jpg')
                    self.fotoactual -= 1
                except:
                    print('No pude eliminar ' + str(i) + '.jpg')
        self.cerrarVentana(caller)
        try:
            self.subp.kill()
            self.controlador.cerrar()
        except:
            pass

    def atras(self, caller):
        self.rollBack(caller)
        if(self.setactual == 1):
            self.iniciar()
        else:
            self.setactual -= 1
            self.continuar()

    def cancelar(self, caller):
        while self.setactual > 0:
            self.rollBack(caller)
            self.setactual -= 1

    def crearDirectorios(self, path, fullmode):
        createpath = str(path)
        if fullmode is True:
            try:
                os.makedirs(createpath)
                self.foldercreado = True
            except:
                return False
        try:
            os.chdir(createpath)
            os.makedirs('fotos')
        except:
            return False
        try:
            os.makedirs('pares')
        except:
            os.rmdir('fotos')
            return False
        try:
            os.makedirs('recon')
        except:
            os.rmdir('fotos')
            os.rmdir('pares')
            return False
        try:
            os.makedirs('MVE')
        except:
            os.rmdir('fotos')
            os.rmdir('pares')
            os.rmdir('recon')
            return False
        self.proypath = os.getcwd()
        return True

    def controlarLuces(self):
        if self.ledsON is True:
            self.controlador.pasarOrden('d')
            self.ledsON = False
        else:
            self.controlador.pasarOrden('c')
            self.ledsON = True

    def controlarEnfoque(self, op):
        newfocus = self.focusactual
        if op == 0:
            newfocus -= 5
            newfocus %= 251
        else:
            newfocus += 5
            newfocus %= 251
        p = subprocess.Popen(['v4l2-ctl', '-c', 'focus_absolute=' +
            str(newfocus)])
        p.wait()
        focusactual = str(subprocess.check_output(['v4l2-ctl', '-C',
                          'focus_absolute'], shell=False))
        self.focusactual = int(focusactual.replace("focus_absolute: ", ""))

    def cerrarVentana(self, ventana):
        try:
            ventana.close()
            return True
        except:
            return False

    def actualizarPath(self, txtpath):
        folderpath = QtGui.QFileDialog.getExistingDirectory(None,
            'Abrir directorio', self.usrpath, QtGui.QFileDialog.ShowDirsOnly)
        if folderpath != "":
            txtpath.setText(self.folderpath)
            
    def procesar(self, caller):        
        while True:
            inchar = self.subp.stdout.read(1)
            if inchar:
                caller.agregarLinea(inchar)
            else:
                print('')
                break


if __name__ == '__main__':
    app = QtGui.QApplication([])    
    soft = NelSoft()
    soft.iniciar()
    app.exec_()
    try:
        soft.subp.kill()
        soft.controlador.cerrar()
    except:
        pass
