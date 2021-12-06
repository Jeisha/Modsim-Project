from tkinter import *
from math import sqrt
import time

window =Tk()

ww = 1000
wh = 500

canvas = Canvas(window,width=ww,height=wh, bg="white")
canvas.grid(row=0,column=0)
window.title('Collision test integrating simulation and modelling')
m1 = 10
m2 = 5
v1 = 0.5
v2 = -0.5

l1 = sqrt(m1)*100
l2 = sqrt(m2)*100

b1 = canvas.create_rectangle(10,wh-l1, 10+l1,wh, fill="blue")
b2 = canvas.create_rectangle(ww-l2-10,wh-l2,ww-10,wh,fill='purple')

for i in range(100000):
    canvas.move(b1,v1,0)
    canvas.move(b2,v2,0)
    if canvas.coords(b1)[0] <= 0:
        v1 *= -1
    if canvas.coords(b2)[2] >= ww:
        v2 *= -1
    if canvas.coords(b1)[2] >= canvas.coords(b2)[0]:
        v = v1
        v1 = (m1 - m2) / (m1+m2) * v1 + 2 * m2 / (m1+m2)*v2
        v2 = (m2 - m1) / (m2+m1) * v2 + 2 * m1 / (m2+m1)*v
    window.update()

window.mainloop()