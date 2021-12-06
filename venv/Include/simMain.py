import threading

class customer(threading.Thread):
    def __init__(self,name,position):
        threading.Thread.__init__(self)
        self.name = name
        self.pos = position