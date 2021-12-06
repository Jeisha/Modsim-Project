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
simEnd = 30
rejected = QueueClass(1000000,'Rejected') # for passenger who fail to board flight
exit = QueueClass(1000000,'Exit') # for passenger who pass check in
passengers = [] # for total all pass who go through the door
passengersLock = threading.Lock()
DoorQ = QueueClass(10000,'DOORQ')
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
            if self.Status == CheckInServer.BUSY and self.Customer != None:
                self.Status = CheckInServer.FREE

                if not self.Customer.Passport:
                    time.sleep(random.randint(0, 3))
                    self.Customer.pos = Passenger.CHECKIN_REJECTED
                    rejected.Lock.acquire()
                    rejected.put(self)
                    rejected.Lock.release()
                
                if self.Customer.Luggage:
                    time.sleep(random.randint(0, 3))
                    self.Customer.pos = Passenger.CHECKIN_DONE
                    exit.Lock.acquire()
                    exit.put(self)
                    exit.Lock.release()
                else:
                    time.sleep(random.randint(1, 4))
                    self.Customer.pos = Passenger.CHECKIN_DONE
                    exit.Lock.acquire()
                    exit.put(self)
                    exit.Lock.release()
                
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
    
    def __init__(self, maritalStatus, FlightType, name):
        threading.Thread.__init__(self)
        self.MaritalStatus = maritalStatus
        self.FlightType = FlightType
        self.Ticket = np.random.choice([True,False],1,[0.98,0.02])
        self.Passport = np.random.choice([True,False],1,[0.98,0.02])
        self.Name = name
        self.pos = Passenger.DOORQ_IN_QUEUE
        self.Luggage = np.random.choice([True,False],1,[0.75,0.25])
        self.Q = None
        print(f'Passenger {self.Name} created.')
    
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
                            Break = False
                            qsize.append(i.qsize())
                if not Break:
                    minVal = min(qsize)
                    minIndex = qsize.index(minVal)
                    self.Q = newQ[minIndex]
                    self.Q.Lock.acquire()
                    self.Q.put(self)
                    self.Q.Lock.release()
                    self.pos = Passenger.CHECKIN_IN_QUEUE
                
                             
            if  self.pos == Passenger.CHECKIN_REJECTED:
                print(f'Passenger {self.Name} rejected')
                break
            if self.pos == Passenger.CHECKIN_DONE:
                print(f'Passenger {self.Name} has done Check-in. Goint to next procedure.')
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
print('Servers Created.... Starting Simulation...')
time.sleep(1)

while simTime < simEnd:
    
    FlightTimeProbabilities = dt.PassengerArriveProb
    NewPassengerAmount = FlightTimeProbabilities[simTime%30]

    for i in range(NewPassengerAmount):

        maritalStatus = np.random.choice(Passenger.status,1,Passenger.statusWeight)[0]

        flightType = np.random.choice(['International','Domestic'],1,[dt.InternationalRatio,dt.DomesticRatio])

        if maritalStatus == Passenger.status[0]:
            Name = names.get_full_name()
        else:
            Name = names.get_last_name()

        newPass = Passenger(maritalStatus, flightType, Name)
        newPass.start()
        passengersLock.acquire()
        passengers.append(newPass)
        passengersLock.release()
        DoorQ.put(newPass)
        threads.append(newPass)

    time.sleep(1)
    simTime += 1

for x in threads:
    x.join()
bigQ = 0
for i in passengers:
    if i.Name != "":
        bigQ += 1

print(f'People going in = {DoorQ.qsize()}')
print(f'Passenger in BigQ = {bigQ}')
print(f'Q1 = {CheckInServersQ[0].qsize()}, waiting time {CheckInServersQ[0].Time}')
print(f'Q2 = {CheckInServersQ[1].qsize()}, waiting time {CheckInServersQ[1].Time}')
print(f'Q3 = {CheckInServersQ[2].qsize()}, waiting time {CheckInServersQ[2].Time}')
print(f'Overall = {OverallWaitingTime}')
print(f'Rejected = {rejected.qsize()}')
print(f'Done = {exit.qsize()}')