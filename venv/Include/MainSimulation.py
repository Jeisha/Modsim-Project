from tkinter import *

SimWindow = Tk()
SimHeight = 800
SimWidth = 1500

SimWindow.title('Modelling and Simulation project')

background = Canvas(SimWindow,width=SimWidth,height=SimHeight,bg='white')
background.grid(row=0,column=0)

bpPoints = [100,50,1400,50,1400,700,1075,700,1075,200,800,200,800,700,100,700]
blueprint =  background.create_polygon(bpPoints,outline='blue', fill='grey', width=2)



SimWindow.mainloop()
