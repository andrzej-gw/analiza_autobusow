import config
import requests
import time
import latlon
from datetime import datetime

def lat_lon_na_numer_lokalizacji(lat, lon):
    if lat<52:
        return -1
    if lon<20.5:
        return -1
    if 52.5<=lat:
        return -1
    if 21.5<=lon:
        return -1
    return int((lat-52)*100)+int((lon-20.5)*100)*50

PLANOWANY_CZAS_DZIAŁANIA = 60 # w sekundach

autobusy = {}

autobusy_przekraczające_prędkość = set()

prędkości = []
miejsca_przekroczenia_prędkości = []

autobusy_odwiedzające_lokalizację = []
autobusy_przekraczające_prędkość_w_danej_lokalizacji = []
for i in range(100*50):
    autobusy_odwiedzające_lokalizację.append(set())
    autobusy_przekraczające_prędkość_w_danej_lokalizacji.append(set())
    
odrzucone_odczyty = 0
liczba_odczytów = 0

czas_rozpoczecia = time.time()

#  min_Lat=max_Lat=52.233296
#  min_Lon=max_Lon=21.045162

while time.time()-czas_rozpoczecia < PLANOWANY_CZAS_DZIAŁANIA:
    
    odpowiedz = requests.get("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey="+config.apiKey+"&type=1")
    
    if len(odpowiedz.text) < 100: # wykrywanie błędów pobierania danych
        continue

    dane=odpowiedz.json()


    for autobus in dane['result']:
        #  min_Lat=min(min_Lat, autobus['Lat'])
        #  max_Lat=max(max_Lat, autobus['Lat'])
        #  min_Lon=min(min_Lon, autobus['Lon'])
        #  max_Lon=max(max_Lon, autobus['Lon'])
        if autobus['VehicleNumber'] in autobusy.keys():
            A=latlon.LatLon(autobusy[autobus['VehicleNumber']]['Lat'], autobusy[autobus['VehicleNumber']]['Lon'])
            B=latlon.LatLon(autobus['Lat'], autobus['Lon'])
            dystans=A.distance(B)
            poprzedni_czas=datetime.strptime(autobusy[autobus['VehicleNumber']]['Time'], '%Y-%m-%d %H:%M:%S')
            aktualny_czas=datetime.strptime(autobus['Time'], '%Y-%m-%d %H:%M:%S')
            zmiana_czasu=aktualny_czas-poprzedni_czas
            zmiana_czasu=zmiana_czasu.seconds
            if zmiana_czasu != 0: # nowy odczyt
                liczba_odczytów +=1
                prędkość=dystans/zmiana_czasu*60*60
                numer_lokalizacji = lat_lon_na_numer_lokalizacji(autobus['Lat'], autobus['Lon'])
                if prędkość>90 or numer_lokalizacji==-1: # odrzucam pozostałe odczyty
                    odrzucone_odczyty+=1
                else:
                    autobus["prędkość"]=prędkość
                    prędkości.append(prędkość)
                    if not autobus['VehicleNumber'] in autobusy_odwiedzające_lokalizację[numer_lokalizacji]:
                        autobusy_odwiedzające_lokalizację[numer_lokalizacji].add(autobus['VehicleNumber'])
                    if autobus["prędkość"]>50:
                        if not autobus['VehicleNumber'] in autobusy_przekraczające_prędkość:
                            autobusy_przekraczające_prędkość.add(autobus['VehicleNumber'])
                        if not autobus['VehicleNumber'] in autobusy_przekraczające_prędkość_w_danej_lokalizacji[numer_lokalizacji]:
                            autobusy_przekraczające_prędkość_w_danej_lokalizacji[numer_lokalizacji].add(autobus['VehicleNumber'])
        autobusy[autobus['VehicleNumber']]=autobus
      
    time.sleep(10)
    
#  print(min_Lat, max_Lat)
#  print(min_Lon, max_Lon)
    
print("liczba_odczytów:")
print(liczba_odczytów)

print("odrzucone_odczyty:")
print(odrzucone_odczyty)

print("przekraczające:")
print(len(autobusy_przekraczające_prędkość))

print("wszystkie:")
print(len(autobusy))

print("prędkości:")
print(len(prędkości))
for p in prędkości:
    print(p)

lokalizacje = []
for i in range(50*100):
    if len(autobusy_odwiedzające_lokalizację[i])>=3: # odrzucam miejsca, gdzie było mniej niż 3 autobusy
        lokalizacje.append((len(autobusy_przekraczające_prędkość_w_danej_lokalizacji[i])/len(autobusy_odwiedzające_lokalizację[i]), i, len(autobusy_przekraczające_prędkość_w_danej_lokalizacji[i]), len(autobusy_odwiedzające_lokalizację[i])))
print("lokalizacje:")
print(len(lokalizacje))
for l in lokalizacje:
    print(l[0], l[1], l[2], l[3])
