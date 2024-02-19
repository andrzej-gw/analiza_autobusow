import config
import requests
import time
import latlon
from datetime import datetime

PLANOWANY_CZAS_DZIAŁANIA = 60 # w sekundach

autobusy = {}
prędkości = []


czas_rozpoczecia = time.time()

while time.time()-czas_rozpoczecia < PLANOWANY_CZAS_DZIAŁANIA:
    
    odpowiedz = requests.get("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey="+config.apiKey+"&type=1")
    
    if len(odpowiedz.text) < 100: # wykrywanie błędów
        print("Błąd pobierania danych")
        continue

    dane=odpowiedz.json()

    print(odpowiedz.text, odpowiedz.ok, odpowiedz.status_code)

    print(len(dane['result']))
    for autobus in dane['result']:
        if autobus['VehicleNumber'] in autobusy.keys():
            print("był")

            A=latlon.LatLon(autobusy[autobus['VehicleNumber']]['Lat'], autobusy[autobus['VehicleNumber']]['Lon'])
            B=latlon.LatLon(autobus['Lat'], autobus['Lon'])
            dystans=A.distance(B)
            poprzedni_czas=datetime.strptime(autobusy[autobus['VehicleNumber']]['Time'], '%Y-%m-%d %H:%M:%S')
            aktualny_czas=datetime.strptime(autobus['Time'], '%Y-%m-%d %H:%M:%S')
            zmiana_czasu=aktualny_czas-poprzedni_czas
            zmiana_czasu=zmiana_czasu.seconds
            print(poprzedni_czas)
            print(aktualny_czas)
            print(zmiana_czasu)
            if zmiana_czasu != 0: # nowy odczyt
                print("dystans:", dystans)
                print("czas:", dystans)
                autobus["prędkość"]=dystans/zmiana_czasu*60*60
                prędkości.append(autobus["prędkość"])
        autobusy[autobus['VehicleNumber']]=autobus
        print(autobus)
        print()
      
    print(time.time()-czas_rozpoczecia)
    time.sleep(10)

print(prędkości)
