from tkinter import *
from CheckInServer import CheckInServer

SimWindow = Tk()
SimHeight = 800
SimWidth = 1000
server  = []
SimWindow.title('Modelling and Simulation project')

def serverCheckInCreate(x1,y1,x2,y2,space):
    for i in range(4):
        background.create_rectangle(x1,y1,x2,y2, fill='blue')
        y1 += space
        y2 += space

background = Canvas(SimWindow,width=SimWidth,height=SimHeight,bg='white')
background.grid(row=0,column=0)

bpPoints = [100,50,900,50,900,700,750,700,750,200,600,200,600,700,100,700]
blueprint =  background.create_polygon(bpPoints,outline='blue', fill='grey', width=2)

checkinCountersSpace = background.create_rectangle(130,400,200,670, fill='red')
serverCheckInCreate(150,420,180,470,60)


SimWindow.mainloop()
