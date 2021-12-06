import threading
from queue import Queue

class QueueClass(Queue) :
    def __init__(self,maxSize,name) :
        Queue.__init__(self,maxsize=maxSize)
        self.Lock = threading.Lock()
        self.Name = name
        self.Time = 0