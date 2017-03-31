import serial
import time
#import numpy as np

#controller properties
BaudRate = 2400
DataBits = 8
StopBits = 1
Parity = 'PARITY_NONE'
FlowControl = False

class ColdController(object):
    '''
    classdocs
    '''
    
    def __init__(self, comport, debug=False):
        self.port = comport
        self.debug = debug
        
#         port - Device name or None
#         baudrate (int) - Baud rate such as 9600 or 115200 etc.
#         bytesize - Number of data bits. Possible values: FIVEBITS, SIXBITS, SEVENBITS, EIGHTBITS
#         parity - Enable parity checking. Possible values: PARITY_NONE, PARITY_EVEN, PARITY_ODD PARITY_MARK, PARITY_SPACE
#         stopbits - Number of stop bits. Possible values: STOPBITS_ONE, STOPBITS_ONE_POINT_FIVE, STOPBITS_TWO
#         timeout (float) - Set a read timeout value.
#         xonxoff (bool) - Enable software flow control.
#         rtscts (bool) - Enable hardware (RTS/CTS) flow control.
#         dsrdtr (bool) - Enable hardware (DSR/DTR) flow control.
#         write_timeout (float) - Set a write timeout value.
#         inter_byte_timeout (float) - Inter-character timeout, None to disable (default).
#         Raises:    
#         ValueError - Will be raised when parameter are out of range, e.g. baud rate, data bits.
#         SerialException - In case the device can not be found or can not be configured.
        
        self.ser = serial.Serial(port=self.port, baudrate=BaudRate, bytesize=DataBits, stopbits=StopBits, timeout=5.0)     
        self.ser.flush()
        time.sleep(0.5)
        
    def _readline(self):
        eol = b'\r\n\r\n' #controller end of line format
        leneol = len(eol)
        line = bytearray()
        while True:
            c = self.ser.read(1)
            if c:
                line += c
                if line[-leneol:] == eol:
                    break
            else:
                break
        return bytes(line)
 
    def close(self):
        self.ser.close()
        
    def Communicator(self,comm):
        self.ser.flush()
        self.ser.flushInput()
        #self.ser.flushOutput()
        time.sleep(.25)
        self.ser.write(bytes('*' + comm + '\n', 'ascii'))
        output = self._readline()
        time.sleep(.25)
        #self.ser.flush()
        #self.ser.flushInput()
        #self.ser.flushOutput()
        return output
    
    def Hi(self):
        out=self.Communicator('Hi')
        print(out)
        
    def SetTime(self,HH,MM,SS):
        out=self.Communicator('SetTime '  + HH + ":" + MM + ":" + SS)
        print(out)
        
    def SetTimeCurrent(self):
        time.strftime('%H:%M:%S', time.localtime())
        out=self.Communicator('SetTime '  + time.strftime('%H:%M:%S', time.localtime()))
        print(out)
        
    def SetDate(self,MM,DD,YY):
        out=self.Communicator('SetDate ' + MM + ":" + DD + ":" + YY )
        print(out)
        
    def SetDateCurrent(self):
        out=self.Communicator('SetDate ' + time.strftime('%m:%d:%y', time.localtime()) )
        print(out)
        
    def GetTime(self):
        out=self.Communicator('GetTime')
        try:
            return str(out)[:-4]
        except ValueError:
            print("Decode ValueError")
            return "99:99:99"
    
    def GetDate(self):
        out=self.Communicator('GetDate')
        try:
            return str(out)[:-4]
        except ValueError:
            print("Decode ValueError")
            return "99:99:99"
    
    def GetTemp(self):
        out=self.Communicator('GetTemp')
        try:
            return float(out)
        except ValueError:
            print("Decode ValueError")
            return 9999
    
    def SetTempUnits(self,unit):
        out=self.Communicator('SetTempUnits ' + unit)
        print(out)
    
    def GetTempUnits(self):
        out=self.Communicator('GetTempUnits')
        try:
            return str(out)[:-4]
        except ValueError:
            print("Decode ValueError")
            return "MEOW"
    
    def SetHighTemp(self,temp): #in current temp units
        out=self.Communicator('SetHighTemp ' + str(temp))
        print(out)
        
    def GetHighTemp(self): #in current temp units
        out=self.Communicator('GetHighTemp')
        try:
            return str(out)[:-4]
        except ValueError:
            print("Decode ValueError")
            return 9999
    
    
    def SetCurrent(self,amps): #current in amps
        out=self.Communicator('SetCurrent ' + str(amps))
        print(out)
        
    def GetCurrent(self): #prints current in amps
        out=self.Communicator('GetCurrent')
        try:
            return float(out)
        except ValueError:
            print("Decode ValueError")
            return 9999
    
    def Stop(self):
        out=self.Communicator('Stop')
        self.PrintErrorHandler(out)
        
        
#if __name__ == '__main__':
    #meow = ColdController("COM6")
    #meow.Hi()
    #meow.SetTempUnits('K')
    #a=meow.QuickSaveData(5, 'test.txt')
    #a=meow.QuickLogData(10)
    #print(a)
    #meow.close()