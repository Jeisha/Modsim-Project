from tkinter import *
import random
import numpy as np

SimWindow = Tk()
SimHeight = 800
SimWidth = 1000
serverDisplay  = []
queueDisplay = []
passengerDisplay = []
fillColor = ['red', 'black', 'green']
SimWindow.title('Modelling and Simulation project')

canvas = Canvas(SimWindow,width=SimWidth,height=SimHeight,bg='white')
canvas.grid(row=0,column=0)

offset = 0
serverFill='blue'
queueFill = 'grey'
for i in range(3):
    serverLoc = [300+offset, 50]
    queueLoc = [300+offset,120]
    serverDisplay.append(canvas.create_rectangle(serverLoc[0], serverLoc[1], serverLoc[0] + 60, serverLoc[1] + 60, fill=serverFill))
    queueDisplay.append(canvas.create_rectangle(queueLoc[0], queueLoc[1], queueLoc[0] + 60, queueLoc[1] + 500, fill=queueFill))
    offset += 200

for i in range(10): 
    passengerLoc = [np.random.rand()*SimWidth,780]
    passengerDisplay.append(canvas.create_oval(passengerLoc[0], passengerLoc[1], passengerLoc[0] + 40, passengerLoc[1] + 40, fill=random.choice(fillColor)))



SimWindow.mainloop()
