import json

def __init__(self):
    pass

f = open("C:\\Users\\Windows 10\\OneDrive - Universiti Teknologi PETRONAS\\UTP\\Y3S1\\Modelling and Simulation\\Modsim Project\\venv\\Include\\data.json",'r')
datas = json.loads(f.read())

data = datas['December']
TotalInternationalPassenger = data['International']
TotalDomesticPassenger = data['Domestic']
TotalPassenger = TotalInternationalPassenger + TotalDomesticPassenger
InternationalRatio = TotalInternationalPassenger / TotalPassenger
DomesticRatio = TotalDomesticPassenger / TotalPassenger
TotalPassengerDaily = round(TotalPassenger / 31)
TotalPassengerHourly = round(TotalPassengerDaily / 24)
TotalPassengerMinutely = round(TotalPassengerHourly / 60)

print(InternationalRatio)
print(DomesticRatio)