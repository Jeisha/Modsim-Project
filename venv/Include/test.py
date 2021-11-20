import threading
import time
import random
from tkinter import *
import names as name
from math import *
import numpy as np

window = Tk()
agents = []
simTime = 0
simEnd = 500
cusIndex = 0
appWidth = 1000
appHeight = 500
m1 = 5
m2 = 1
v1 = 1
v2 = -1
l1 = 50
l2 = 50
fillColor = ['red', 'blue', 'black', 'green', 'grey']

window.title("Homework week 8 class - sim3.py")
canvas = Canvas(window, width=appWidth, height=appHeight, bg="white")
canvas.grid(row=0, column=0)


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


class Agent(threading.Thread):  # User is a Thread

    def __init__(self, name, power, loc):
        global canvas
        threading.Thread.__init__(self)
        self.name = name
        self.power = power
        self.loc = loc
        print('Agent {0} created with power {1} at location {2}'.format(self.name, self.power, self.loc))

    def run(self):
        global simTime, simEnd, agents, canvas

        while simTime < simEnd:

            self.finaldir = np.array((0, 0))
            self.move = np.array((0, 0))
            self.adir = np.array((0, 0))
            for ag in range(len(agents)):
                if agents[ag].name == self.name:
                    continue

                if agents[ag].power < self.power:
                    continue

                self.adir = agents[ag].loc - self.loc
                self.finaldir = self.finaldir + self.adir

            self.move = normalize(self.finaldir) * 3
            self.loc = self.loc + self.move
            print('Agent {0} with power {1} moved at velocity {2}. Current location: {3}.'.format(self.name,self.power,tuple(self.move),tuple(self.loc)))
            time.sleep(0.05)

    def direction(self):
        return self.move


numAgents = 20
agentDisp = []
for i in range(numAgents):
    loc = [np.random.rand() * appWidth, np.random.rand() * appHeight]
    agent = Agent(name.get_first_name(), random.randint(0, 5), loc)
    agents.append(agent)
    agentDisp.append(canvas.create_oval(loc[0], loc[1], loc[0] + 20, loc[1] + 20, fill=random.choice(fillColor)))
    agent.start()

# simulation loop
while simTime < simEnd:
    simTime = simTime + 1
    time.sleep(0.05)
    for i in range(len(agentDisp)):
        canvas.move(agentDisp[i],agents[i].direction()[0],agents[i].direction()[1])
    window.update()

window.mainloop()
