from asynch_dispatch import *
import threading
import serial

class SerialStream(threading.Thread):
  def __init__(self, port='COM1', baud=9600, timeout=0.1, read_size=1000,
      sinks=None, autoStart=True):
    
    threading.Thread.__init__(self)
    self.daemon = True
    
    self.read_size = read_size
    
    self.dispatcher=AsynchDispatch(sinks=sinks,
      callbacks={'serial_data':[self.send]})
    
    try:
      self.port = serial.Serial(port,baud,timeout=timeout)
    except:
      print 'Failed to open serial port at %s' % port.__str__()
      self.port = None
    
    if autoStart:
      self.start()
    
  def run(self):
    if self.port is not None:
      while(True):
        rx_bytes = self.port.read(self.read_size)
        if rx_bytes != '':
          self.dispatcher.dispatch(Message('serial_data',rx_bytes))
        
  def send(self, message):
    if self.port is not None:
      self.port.write(message.data)