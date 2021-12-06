import random
from tkinter import *
import threading
import names
import time
from queue import Queue
import data as dt
import numpy as np


class QueueClass(Queue) :
    def __init__(self,maxSize,name) :
        Queue.__init__(self,maxsize=maxSize)
        self.Lock = threading.Lock()
        self.LockGet = threading.Lock()
        self.LockTime = threading.Lock()
        self.Name = name
        self.Time = 0

simTime = 0
simEnd = 119
rejected = QueueClass(1000000,'Rejected') # for passenger who fail to board flight
exit = QueueClass(1000000,'Exit') # for passenger who pass check in
passengers = [] # for total all pass who go through the door
passengersLock = threading.Lock()
DoorQ = QueueClass(10000,'DOORQ')
FlightTime = 29 # next flight time
TicketInt = ['MH0370', 'BD0674', 'BA1326', 'BA1476', 'GF5232'] # international flight
TicketDom = ['AA8025', 'AA7991', 'AA8017', 'BA1442', 'BA1388'] # domestic flight
FlightTimeProbabilities = []
threads = [] # all threads

OverallWaitingTime = 0 # total waiting time for all passengers
OverallWaitingTimeLock = threading.Lock()
CheckInServersQ = [] # list for check in queue
CheckInServers = [] # list for check in server

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
            elif self.Status == CheckInServer.BUSY and not self.Q.empty():
                self.Status = CheckInServer.FREE

                if not self.Customer.Passport:
                    time.sleep(random.uniform(0, 3))
                    self.Customer.pos = Passenger.CHECKIN_REJECTED
                    rejected.Lock.acquire()
                    rejected.put(self)
                    rejected.Lock.release()
                
                if self.Customer.Luggage:
                    time.sleep(random.uniform(2, 5))
                    self.Customer.pos = Passenger.CHECKIN_DONE
                    exit.Lock.acquire()
                    exit.put(self)
                    exit.Lock.release()
                else:
                    time.sleep(random.uniform(5, 10))
                    self.Customer.pos = Passenger.CHECKIN_DONE
                    exit.Lock.acquire()
                    exit.put(self)
                    exit.Lock.release()
            time.sleep(1)
                
    def CheckGetCustomer(self):
        self.Q.LockGet.acquire()
        if not self.Q.empty():
            self.Customer = self.Q.get()
            self.Status = CheckInServer.BUSY
        self.Q.LockGet.release()

class Passenger(threading.Thread):
    status = ['Single','Married','Family']
    statusWeight = [0.2,0.66,0.14]
    DOORQ_IN_QUEUE = 0
    CHECKIN_IN_QUEUE = 1
    CHECKIN_SERVING = 2
    CHECKIN_REJECTED = 3
    CHECKIN_DONE = 4
    
    def __init__(self, maritalStatus, Ticket, FlightType, name):
        threading.Thread.__init__(self)
        self.MaritalStatus = maritalStatus
        self.FlightType = FlightType
        self.Ticket = Ticket
        self.Passport = np.random.choice([True,False],1,[0.98,0.02])
        self.Name = name
        self.pos = Passenger.DOORQ_IN_QUEUE
        self.Luggage = np.random.choice([True,False],1,[0.75,0.25])
        self.Q = None
    
    def run(self):
        global simTime, simEnd, CheckInServers, rejected, OverallWaitingTime, DoorQ

        while simTime < simEnd:
            if self.pos == Passenger.CHECKIN_IN_QUEUE:
                OverallWaitingTimeLock.acquire()
                OverallWaitingTime += 1
                OverallWaitingTimeLock.release()
                self.Q.LockTime.acquire()
                self.Q.Time += 1
                self.Q.LockTime.release()

            if  self.pos == Passenger.CHECKIN_SERVING:
                pass

            if self.pos == Passenger.DOORQ_IN_QUEUE:
                newQ = random.sample(CheckInServersQ, 3)
                qsize = []
                Break = False
                for i in newQ:
                    qsize.append(i.qsize())
                    if not i.full():
                        if i.empty():
                            self.Q = i
                            self.Q.Lock.acquire()
                            self.Q.put(self)
                            self.Q.Lock.release()
                            self.pos = Passenger.CHECKIN_IN_QUEUE
                            Break = True
                            break
                        else:
                            qsize.append(i.qsize())
                if not Break:
                    OverallWaitingTimeLock.acquire()
                    OverallWaitingTime += 1
                    OverallWaitingTimeLock.release()
                    DoorQ.Lock.acquire()
                    DoorQ.Time += 1
                    DoorQ.Lock.release()
                    if qsize[0] > qsize[1]:
                        if qsize[0] > qsize[2]:
                            self.Q = newQ[0]
                        else:
                            self.Q = newQ[2]
                    else:
                        if qsize[1] > qsize[2]:
                            self.Q = newQ[1]
                        else:
                            self.Q = newQ[2]
                    
                    self.Q.Lock.acquire()
                    self.Q.put(self)
                    self.Q.Lock.release()
                    self.pos = Passenger.CHECKIN_IN_QUEUE
                             
                
            if  self.pos == Passenger.CHECKIN_REJECTED:
                break

            if self.pos == Passenger.CHECKIN_DONE:
                break

            time.sleep(1)

        passengersLock.acquire()
        for i in range(len(passengers)):
            if passengers[i] is not None:
                if passengers[i].Name == self.Name:
                    passengers[i].Name = ""
                    break
        passengersLock.release()

for i in range(3):
    CheckInQ = QueueClass(10000,f'Q{i}')
    server = CheckInServer(CheckInQ)
    CheckInServersQ.append(CheckInQ)
    CheckInServers.append(server)
    CheckInServers[i].start()
    threads.append(server)

while simTime < simEnd:

    NewPassengerAmount = random.randint(1,5)
    for i in range(NewPassengerAmount):

        maritalStatus = np.random.choice(Passenger.status,1,Passenger.statusWeight)[0]

        flightType = np.random.choice(['International','Domestic'],1,[dt.InternationalRatio,dt.DomesticRatio])

        Ticket = random.choice(TicketInt)

        if maritalStatus == Passenger.status[0]:
            Name = names.get_full_name()
        else:
            Name = names.get_last_name

        newPass = Passenger(maritalStatus, Ticket, flightType,Name)
        newPass.start()
        passengersLock.acquire()
        passengers.append(newPass)
        passengersLock.release()
        DoorQ.put(newPass)
        threads.append(newPass)

    time.sleep(1)
    simTime += 1
    print(simTime)

for x in threads:
    x.join()
bigQ = 0
for i in passengers:
    if i.Name != "":
        bigQ += 1

print(f'People going in = {DoorQ.qsize()}')
print(f'Passenger in BigQ = {bigQ}')
print(f'People waiting time before going to checkin queue = {DoorQ.Time}')
print(f'Q1 = {CheckInServersQ[0].qsize()}, waiting time {CheckInServersQ[0].Time}')
print(f'Q2 = {CheckInServersQ[1].qsize()}, waiting time {CheckInServersQ[1].Time}')
print(f'Q3 = {CheckInServersQ[2].qsize()}, waiting time {CheckInServersQ[2].Time}')
print(f'Overall = {OverallWaitingTime}')
print(f'Rejected = {rejected.qsize()}')
print(f'Done = {exit.qsize()}')