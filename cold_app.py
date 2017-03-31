from ScopeFoundry import BaseMicroscopeApp
from cold_controller_hw import ColdControllerHW
from cold_logger import ColdLoggerMeasure

class ColdApp(BaseMicroscopeApp):
    
    name = 'cold'
    
    def setup(self):
        
        self.add_hardware(ColdControllerHW(self))
        
        self.add_measurement(ColdLoggerMeasure(self))
        
        
if __name__ == '__main__':
    import sys
    
    app = ColdApp(sys.argv)
    sys.exit(app.exec_())