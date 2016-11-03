import serial


class Controlador():

    def __init__(self):
        self.ser = serial.Serial('/dev/ttyACM0', 9600)

    def pasarOrden(self, orden):
        self.ser.write(orden)

    def cerrar(self):
        self.ser.close()
        del(self)
