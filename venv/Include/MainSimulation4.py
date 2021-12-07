import random
import threading
from typing import List
import names
import time
import numpy as np
from tkinter import *

def putItem(List ,item):
    List.append(item)
    
def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

SimWindow = Tk()
SimHeight = 800
SimWidth = 1000
simTime = 0
simEnd = 30
serverAmount = 3
inQPos = []

rejected = [] # for passenger who fail to board flight
rejectedLock = threading.Lock()
rejectedNumber = 0
rejectedNumberLoc = threading.Lock()
exit = [] # for passenger who pass check in
exitLock = threading.Lock
DoorQ = []
CurrPassengers = []
threads = [] # all threads

OverallWaitingTime = 0 # total waiting time for all passengers
OverallWaitingTimeLock = threading.Lock()
CheckInServersQ = [] # list for check in queue
CheckInServersQTime = [0,0,0]
qNumber =[0,0,0]
qNumberLock = []
CheckInServersQLock = []
CheckInServersQTimeLock = []
for i in range(3):
    qNumberLock.append(threading.Lock())
    CheckInServersQLock.append(threading.Lock())
    CheckInServersQTimeLock.append(threading.Lock())
queueDisplay = [] # display queue
CheckInServers = [] # list for check in server
serverDisplay  = []
passengerDisplay = [] # passenger's display
fillColor = ['red', 'yellow', 'green'] # color for passengers
offset = 0
serverFill='blue' # color for servers
queueFill = 'grey' # color ofr queue line
SimWindow.title('Modelling and Simulation project')

canvas = Canvas(SimWindow,width=SimWidth,height=SimHeight,bg='white')
canvas.grid(row=0,column=0)

class CheckInServer(threading.Thread):
    BUSY = 0
    FREE = 1
    def __init__(self,queue,ID,Loc):
        threading.Thread.__init__(self)
        self.Status = CheckInServer.FREE
        self.Customer = None
        self.Name = names.get_full_name()
        self.Q = queue
        self.ID = ID
        self.Loc = Loc
        
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
                    # add to rejected list
                    putItem(rejected,self.Customer)
                    # increasing the number served by the server
                    qNumber[CheckInServersQ.index(self.Q)] += 1
                else:
                    if self.Customer.Luggage:
                        time.sleep(random.randint(1,4))
                        self.Customer.pos = Passenger.CHECKIN_DONE
                        # add to done list
                        putItem(exit,self.Customer)
                        # increasing the number served by the server
                        qNumber[CheckInServersQ.index(self.Q)] += 1   
                    else:
                        time.sleep(random.randint(1, 5))
                        self.Customer.pos = Passenger.CHECKIN_DONE
                        # add to done list
                        putItem(exit,self.Customer)
                        # increasing the number served by the server 
                        qNumber[CheckInServersQ.index(self.Q)] += 1   
    
    def CheckGetCustomer(self):
            if self.Q:
                self.Customer = self.Q[0]
                self.Q.remove(self.Customer)
                self.Status = CheckInServer.BUSY
                self.Customer.pos = Passenger.CHECKIN_SERVING
            else:
                self.Customer = None
            time.sleep(2)

class Passenger(threading.Thread):
    status = ['Single','Married','Family']
    statusWeight = [0.2,0.66,0.14]
    DOORQ_IN_QUEUE = 0
    CHECKIN_IN_QUEUE = 1
    CHECKIN_SERVING = 2
    CHECKIN_REJECTED = 3
    CHECKIN_DONE = 4

    def __init__(self, maritalStatus, name, Loc):
        threading.Thread.__init__(self)
        self.MaritalStatus = maritalStatus
        self.Ticket = np.random.choice([True,False],1,[0.98,0.02])
        self.Passport = np.random.choice([True,False],1,[0.98,0.02])
        self.Name = name
        self.pos = Passenger.DOORQ_IN_QUEUE
        self.Luggage = np.random.choice([True,False],1,[0.75,0.25])
        self.Q = None
        self.Loc = Loc
        self.move = None
        self.visible = True
        print(f'Passenger {self.Name} created.')
    
    def run(self):
        global simTime, simEnd, CheckInServers, rejected, OverallWaitingTime, inQPos, CheckInServersQ, canvas
        while simTime < simEnd:
            self.move = np.array((0,0))
            if self.pos == Passenger.CHECKIN_SERVING:
                continue
            if self.pos == Passenger.CHECKIN_IN_QUEUE:
                qNo = CheckInServersQ.index(self.Q)
                InqNo = self.Q.index(self)
                currLoc = inQPos[qNo][InqNo]
                self.move = np.array(currLoc) - np.array(self.Loc)
                self.Loc = self.move + self.Loc
                OverallWaitingTime += 1   
                CheckInServersQTime[CheckInServersQ.index(self.Q)] += 1   

            if self.pos == Passenger.DOORQ_IN_QUEUE:
                newQ = random.sample(CheckInServersQ, 3)
                qsize = []
                Break = False
                for i in newQ:
                    if not i:
                        self.Q = i
                        putItem(self.Q, self)
                        self.pos = Passenger.CHECKIN_IN_QUEUE
                        Break = True
                        print(f'{self.Name} went into queue {CheckInServersQ.index(self.Q) + 1}')
                        break
                    else:
                        Break = False
                        qsize.append(len(i))
                if not Break:
                    minVal = min(qsize)
                    minIndex = qsize.index(minVal)
                    self.Q = newQ[minIndex]
                    putItem(self.Q, self)
                    self.pos = Passenger.CHECKIN_IN_QUEUE
                    print(f'{self.Name} went into {CheckInServersQ.index(self.Q) + 1}')
                
            # if rejected                 
            if  self.pos == Passenger.CHECKIN_REJECTED:
                print(f'Passenger {self.Name} rejected')
                self.visible = False
                break
            # if done checkin  
            if self.pos == Passenger.CHECKIN_DONE:
                print(f'Passenger {self.Name} has done Check-in. Going to next procedure.')
                self.visible = False
                break
            time.sleep(2)

offset = 0
queueStartLoc = []
hello = []
# creating servers and server queue
for i in range(serverAmount):
    InqueueLoc = [320+offset,120]
    inQOffset = 0
    tempQPos = []

    for j in range(17):
        tempQPos.append([InqueueLoc[0],InqueueLoc[1]+inQOffset])
        inQOffset +=30
    
    inQPos.append(tempQPos)
    Loc = np.array((325+offset,630))
    queueStartLoc.append(Loc)
    CheckInQ = []
    CheckInServersQ.append(CheckInQ)
    queueLoc = [300+offset,120]
    queueDisplay.append(canvas.create_rectangle(queueLoc[0], queueLoc[1], queueLoc[0] + 60, queueLoc[1] + 500, fill=queueFill))

    # Assigning queue to server
    Loc = [300+offset, 50]
    server = CheckInServer(CheckInServersQ[i],i, Loc)
    CheckInServers.append(server)
    serverDisplay.append(canvas.create_rectangle(Loc[0], Loc[1], Loc[0] + 60, Loc[1] + 60, fill=serverFill))
    CheckInServers[i].start()
    threads.append(server)
    offset += 200

while simTime < simEnd:


    NewPassengerAmount = random.randint(0,4)
    for i in range(NewPassengerAmount):
        
        # status for person
        maritalStatus = np.random.choice(Passenger.status,1,Passenger.statusWeight)[0]

        # if single, get full name
        if maritalStatus == Passenger.status[0]:
            Name = names.get_full_name()
        # if married or have family, get the last name only to represent family
        else:
            Name = names.get_last_name()
        Loc = np.array([np.random.rand()*SimWidth,780])
        # create new passenger with the classes
        newPass = Passenger(maritalStatus, Name, Loc)
        newPass.start() # start
        DoorQ.append(newPass) # get the passenger into the list for initial queue
        CurrPassengers.append(newPass)
        threads.append(newPass) # thread list to wait for all thread finish
        passengerDisplay.append(canvas.create_oval(Loc[0], Loc[1], Loc[0] + 20, Loc[1] + 20, fill=random.choice(fillColor),tags=f'{Name}'))
    index = []
    for i in range(len(CurrPassengers)):
        if CurrPassengers[i].visible == False: 
            index.append(i)
        else:
            canvas.move(passengerDisplay[i],CurrPassengers[i].move[0],CurrPassengers[i].move[1])
            SimWindow.update()
    index.sort(reverse=True)
    for i in index:
        canvas.delete(f'{CurrPassengers[i].Name}')
        CurrPassengers.pop(i)
        passengerDisplay.pop(i)
    
    time.sleep(2) # 1 minute delay
    simTime += 1
    
for x in threads:
    x.join()
# output
print('\nOUTPUT:')
print(f'{len(DoorQ)} people went in.')
for i in range(len(CheckInServersQ)):
    print(f'Queue {i+1}')
    print(f'    People still in queue: {len(CheckInServersQ[i])}')
    print(f'    Served number: {qNumber[i]}')
    print(f'    Overall Waiting Time for this queue: {CheckInServersQTime[i]} Minutes.')
print(f'Overall waiting time for all queue: {OverallWaitingTime} Minutes.')
print(f'{len(rejected)} people has been rejected')
print(f'{len(exit)} people have done check-in process and proceed to the next stage')

SimWindow.mainloop()