from random import random
from ClassQueue import QueueClass as qClass
from tkinter import *
import threading
import names
import time
from queue import Queue
import data as dt

CheckInQs = []
DoorQ = []
CheckInServers = []
simTime = 0
simEnd = 120
FlightTime = 29
Ticket = ['MH0370', 'BD0674', 'BA1326', 'BA1476', 'GF5232','AA8025', 'AA7991', 'AA8017', 'BA1442', 'BA1388']
FlightQueueInt = Queue(maxsize=5)
FlightQueueDom = Queue(maxsize=5)
for i in TicketInt:
    FlightQueueInt.put(i)
for i in TicketDom:
    FlightQueueDom.put(i)
CurrentFlight = []
CurrentFlight[0] = FlightQueueInt.get()
CurrentFlight[1] = FlightQueueDom.get()
FlightTimeProbabilities = []
passengers = []



class CheckInServer(threading.Thread):
    BUSY = 0
    FREE = 1
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.Status = CheckInServer.FREE
        self.Customer = None
        self.Name = names.get_full_name()
        self.Q = queue

    def run(self):
        global simTime, simEnd
        while simTime < simEnd :
            if self.Status == CheckInServer.FREE:
                self.CheckGetCustomer()
            else :
                customer = self.Customer
    
    def CheckGetCustomer(self):
        Q = self.Q
        Q.Lock.acquire()
        if not Q.empty():
            self.Customer = Q.get()
        else:
            print('No customer on queue {0}'.format(Q.Name))
        Q.Lock.release()

class Customer(threading.Thread):
    status = ['Single','Married','Family']
    statusWeight = [0.2,0.66,0.14]
    CHECKIN_IN_QUEUE = 'In checkin queue'
    CHECKIN_SERVING = 'Currently being served'
    DOORQ_IN_QUEUE = 'Just arrive to the airport'
    
    def __init__(self, maritalStatus, Ticket, FlightType, passport, name):
        threading.Thread.__init__(self)
        self.MaritalStatus = maritalStatus
        self.FlightType = FlightType
        self.Ticket = Ticket
        self.Passport = passport
        self.Name = name
        self.pos = Customer.DOORQ_IN_QUEUE

    def run(self):
        global simTime, simEnd
        while simTime < simEnd :
            if self.Status == CheckInServer.FREE:
                self.CheckGetCustomer()
            else :
                customer = self.Customer

def getTicket(Tickets,probabilities):
    return random.choices(Tickets,probabilities)

for i in range(3):
    newServerQ = qClass(None,f'CI #{i}')
    CheckInQs.append(newServerQ)
    newCheckInServer = CheckInServer(CheckInQs[i])
    newCheckInServer.start()
    CheckInServers.append(newCheckInServer)

while simTime < simEnd:
    
    if not simTime%FlightTime:
        FlightTimeProbability = 50
        FlightTime += 30
        CurrentFlight[0] = FlightQueueInt.get()
        CurrentFlight[1] = FlightQueueDom.get()
    else:
        FlightTimeProbability += 1.6
        FlightIntList = list(FlightQueueInt.queue)
        FlightDomList = list(FlightQueueDom.queue)

    NoNewPassenger = random.int(3,8)
    for i in range(NoNewPassenger):

        maritalStatus = random.choices(Customer.status,Customer.statusWeight)[0]

        flightType = random.choices(['International','Domestic'],[dt.InternationalRatio,dt.DomesticRatio])
        FlightTimeProbabilities = [FlightTimeProbability]

        for i in range(1,len(FlightIntList)):
            FlightTimeProbabilities.append((100-FlightTimeProbability)/ len(FlightIntList))
        if flightType == 'International':
            Ticket = getTicket(FlightIntList,FlightTimeProbabilities)
        else:
            Ticket = getTicket(FlightDomList,FlightTimeProbabilities)
        
        passport = random.choices([True,False],[0.98,0.02])

        if maritalStatus == Customer.status[0]:
            Name = names.get_full_name()
        else:
            Name = names.get_last_name
        

        newPass = Customer(maritalStatus, Ticket, flightType, passport)
        passengers.append(newPass)
        DoorQ.append(newPass)

    time.sleep(0.25)
    simTime += 1