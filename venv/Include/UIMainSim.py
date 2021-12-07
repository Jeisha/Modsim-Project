from tkinter import *
import random
import numpy as np
import time

SimWindow = Tk()
SimHeight = 800
SimWidth = 1000
simTime = 0
simEnd = 1000
serverDisplay  = []
queueDisplay = []
inQPos = []
passengerDisplay = []
passengerLoc = []
fillColor = ['red', 'black', 'green']
SimWindow.title('Modelling and Simulation project')

canvas = Canvas(SimWindow,width=SimWidth,height=SimHeight,bg='white')
canvas.grid(row=0,column=0)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

offset = 0
serverFill='blue'
queueFill = 'grey'
for i in range(3):
    serverLoc = [300+offset, 50]
    queueLoc = [300+offset,120]
    serverDisplay.append(canvas.create_rectangle(serverLoc[0], serverLoc[1], serverLoc[0] + 60, serverLoc[1] + 60, fill=serverFill))
    queueDisplay.append(canvas.create_rectangle(queueLoc[0], queueLoc[1], queueLoc[0] + 60, queueLoc[1] + 500, fill=queueFill))
    offset += 200

offset = 0
for i in range(3):
    queueLoc = [320+offset,120]
    inQOffset = 0
    for j in range(17):
        inQPos.append(canvas.create_oval(queueLoc[0], queueLoc[1]+inQOffset, queueLoc[0]+20, queueLoc[1]+20+inQOffset,fill=random.choice(fillColor)))
        inQPos[i].append(queueLoc[0], queueLoc[1]+inQOffset, queueLoc[0]+20, queueLoc[1]+20+inQOffset)
        inQOffset +=30

    offset += 200

for i in range(10): 
    passengerLoc.append([np.random.rand()*SimWidth,780])
    passengerDisplay.append(canvas.create_oval(passengerLoc[i][0], passengerLoc[i][1], passengerLoc[i][0] + 20, passengerLoc[i][1] + 20, fill=random.choice(fillColor)))

queue1StartLoc = np.array((325,630))
queue2StartLoc = np.array((525,630))
queue3StartLoc = np.array((725,630))

while simTime < simEnd:
    for i in range(len(passengerDisplay)):
        finaldir = np.array((0, 0))
        move = np.array((0, 0))
        adir = np.array((0, 0))
        
        adir = queue1StartLoc - passengerLoc[i]
        finaldir = finaldir + adir
        move = normalize(finaldir) * 3
        passengerLoc[i] += move
        
        canvas.move(passengerDisplay[i],move[0],move[1])
    simTime += 1
    time.sleep(0.25)
    SimWindow.update()



SimWindow.mainloop()
