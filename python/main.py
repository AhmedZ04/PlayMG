import serial.tools.list_ports

class Main():
    
    def __init__(self, baudrate=9600):
        self.Serial = serial.Serial()
        self.Serial.port = self._get_COM()
        self.Serial.baudrate = baudrate

    def _get_COM(self):
        ports = serial.tools.list_ports.comports()

        for port in ports:
            if str(port).startswith("COM3"):
                return "COM3"

    def ReadSerial(self):
        self.Serial.open()
        while True:
            if self.Serial.in_waiting:
                packet = self.Serial.readline()
                print(packet.decode('utf'))


if __name__ == "__main__":
    main = Main()
    main.ReadSerial()