import config
import requests
import time
import latlon
from datetime import datetime

PLANOWANY_CZAS_DZIAŁANIA = 60 # w sekundach

autobusy = {}

autobusy_przekraczające_prędkość = set()

prędkości = []
miejsca_przekroczenia_prędkości = []

odrzucone_odczyty = 0
liczba_odczytów = 0

czas_rozpoczecia = time.time()

while time.time()-czas_rozpoczecia < PLANOWANY_CZAS_DZIAŁANIA:
    
    odpowiedz = requests.get("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey="+config.apiKey+"&type=1")
    
    if len(odpowiedz.text) < 100: # wykrywanie błędów pobierania danych
        continue

    dane=odpowiedz.json()


    for autobus in dane['result']:
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
                if prędkość>90: # odrzucam pozostałe odczyty
                    odrzucone_odczyty+=1
                else:
                    autobus["prędkość"]=prędkość
                    prędkości.append(prędkość)
                    if autobus["prędkość"]>50:
                        if not autobus['VehicleNumber'] in autobusy_przekraczające_prędkość:
                            autobusy_przekraczające_prędkość.add(autobus['VehicleNumber'])
        autobusy[autobus['VehicleNumber']]=autobus
      
    time.sleep(10)
    
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
