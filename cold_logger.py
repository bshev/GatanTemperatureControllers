from ScopeFoundry import Measurement
import pyqtgraph as pg
import time
import os
import numpy as np

class ColdLoggerMeasure(Measurement):
    
    name = 'cold_logger'
    
    def setup(self):
        
        self.ui = self.plot =  pg.PlotWidget()
        
        self.plotline = self.plot.plot(pen='r')
        
    def run(self):
        hw = self.app.hardware['cold_controller']
        
        self.time_list = []
        self.temp_list = []
        self.curr_list = []
        
        self.t0 = time.time()
        
        with open(os.getcwd() + '/data/data_file_%i.txt' % self.t0, 'w') as f:
        
            while not self.interrupt_measurement_called:
                
                temp = hw.settings.temp.read_from_hardware()
                
                curr = hw.settings.current.read_from_hardware()
                
                t1 = time.time()
                self.time_list.append(t1)
                self.temp_list.append(temp)
                self.curr_list.append(curr)
                
                print(t1, temp, curr)
                
                f.write("{}, {}, {}\n".format(t1, temp, curr))
                
                time.sleep(0.5)
            
            
    def update_display(self):
        
        self.plotline.setData(np.array(self.time_list)-self.t0, self.temp_list,pen=None, symbolBrush='b', symbolPen='w')
        
    