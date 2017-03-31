from ScopeFoundry import HardwareComponent
from cold_controller_dev import ColdController
import os

class ColdControllerHW(HardwareComponent):
    
    name = 'cold_controller'
    
    def setup(self):
        
        #for mac
        devlist=[]
        for root, dirs, files in os.walk("/dev", topdown=False):
            for name in files:
                if name[0:3]=='cu.':
                    print(os.path.join(root, name))
                    devlist.append(os.path.join(root, name))
                    
        #for windoes
        #devlist = ["COM8"]
        
        self.settings.New('port', dtype=str, initial=devlist[-1])
        self.settings.New('temp', dtype=float, ro=True)
        self.settings.New('temp_unit', dtype=str, choices=('FAHRENHEIT', 'CENTIGRADE', 'KELVIN'), initial='CENTIGRADE')
        self.settings.New('current', dtype=float, unit='A', vmin=0.000, vmax=0.900, spinbox_decimals = 2, spinbox_step=0.01)
    
    def connect(self):
        self.dev = ColdController(comport=self.settings['port'],
                                  debug=self.settings['debug_mode'])
        
        
        S = self.settings
        
        S.temp.connect_to_hardware(
            read_func = self.dev.GetTemp, 
            )
        
        S.temp_unit.connect_to_hardware(
            read_func=self.dev.GetTempUnits,
            write_func=self.dev.SetTempUnits
            )
    
        S.current.connect_to_hardware(
            read_func=self.dev.GetCurrent,
            write_func=self.dev.SetCurrent
            )
        
    
    def disconnect(self):
        
        self.settings.disconnect_all_from_hardware()
        
        if hasattr(self, 'dev'):
            self.dev.close()
            del self.dev