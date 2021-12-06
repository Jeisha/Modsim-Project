import json
import numpy as np 

def __init__(self):
    pass

f = open("venv\\Include\\data.json",'r')
datas = json.loads(f.read())

data = datas['December']
TotalInternationalPassenger = 75000
TotalDomesticPassenger = 238000
TotalPassenger = TotalInternationalPassenger + TotalDomesticPassenger
InternationalRatio = TotalInternationalPassenger / TotalPassenger
DomesticRatio = TotalDomesticPassenger / TotalPassenger
TotalPassengerDaily = round(TotalPassenger / 31)
TotalPassengerHourly = round(TotalPassengerDaily / 24)
TotalPassengerMinutely = round(TotalPassengerHourly / 60)

PassengerArriveTime = [ 'True','False']
a = [2 for i in range(12)]
PassengerArriveProb = a + [3, 4, 8, 10, 8, 4, 3] + a