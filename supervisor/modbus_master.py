'''
Created on Apr 8, 2015

@author: erik

MODBUS master(server) over TCP/IP
'''

from pymodbus.client.sync import ModbusTcpClient

class MBclient(ModbusTcpClient):
    '''
    Class for MODBUS slave points
    '''
    
    def __init__(self, *args, **kwargs):
        ''' Constructor
        
        default modbus port is 502'''
        #ip address
        self.addr = args[0]
        
        ModbusTcpClient.__init__(self, self.addr)
        
        self.connect()
        
    def readCoil(self, coil):
        '''returns single read of coil value'''
        return self.read_coils(coil, 1).bits[0]
        
    def writeCoil(self, coil, val):
        '''writes value to single coil'''
        self.write_coils(coil, [val])
    
    def toggleCoil(self, coil):
        '''toggles the current value of a single coil'''
        val = self.read_coils(coil,1).bits[0]
        
        if type(val) is not bool:
            '''throw exception'''
            print 'communications problem, return read is:', val
        else:
            self.writeCoil(coil, (not val))

  

class MBserver(object):
    '''
    Class for MODBUS master controllers
    '''
    
    def __init__(self, *args, **kwargs):
        '''
        Constructor
        '''
        #dictionary of Modbus slave classes 
        self.clients = kwargs.pop("clients")
        
#==testing==============================================================        
if __name__ == "__main__": 
    from time import sleep
    
    test_client = MBclient('192.168.0.51')
    
    master = MBserver(
                      clients = {1:test_client}
                      )
    
    print "Client key names: ", master.clients.keys()
    
#     while 1:
    print "coil 7 value:", test_client.readCoil(7) # master.clients[1].readCoil(7)
    
    master.clients[1].toggleCoil(8)
    print "coil 8 toggled:", master.clients[1].readCoil(8)
    
    sleep(0.5)
        
        
        