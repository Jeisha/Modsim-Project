from tkinter import *
import threading
import names

class CheckInServer(threading.Thread):
    BUSY = 0
    FREE = 1
    def __init__(self):
        threading.Thread.__init__(self)
        self.Status = CheckInServer.FREE
        self.Customer = None
        self.Name = names.get_full_name()

    def run(self, simTime, simEnd, queue):
        while simTime < simEnd :
            if self.Status == CheckInServer.FREE:
                pass
            else :
                pass
    
    def CheckGetCustomer(self, queue):
        queue.Lock.acquire()
        if not queue.empty():
            self.Customer = queue.get()
        else:
            print('No customer on queue {0}'.format(queue.Name))
        
