import config
import requests
import time
import latlon
import json
import sys

class Godzina_przyjazdu:
    def __init__(self, godzina, nr_brygady):
        self.godzina = godzina
        self.nr_brygady = nr_brygady
    def __str__(self):
        return "Godzina_przyjazdu(godzina: "+self.godzina+", nr_brygady: "+self.nr_brygady+")"
    def __repr__(self):
        return str(self)

class Przystanek_na_linii:
    def __init__(self, godziny_przyjazdu, pozycja, zespół, nazwa, słupek):
        self.godziny_przyjazdu = godziny_przyjazdu
        self.pozycja = pozycja
        self.zespół = zespół
        self.nazwa = nazwa
        self.słupek = słupek
        
    def __str__(self):
        return "Przystanek_na_linii(godziny_przyjazdu: "+str(self.godziny_przyjazdu)+", pozycja: "+str(self.pozycja)+", zespół: "+self.zespół+", nazwa: "+self.nazwa+", słupek: "+self.słupek+")"
    def __repr__(self):
        return str(self)

class Linia:
    def __init__(self, nr, przystanki):
        self.nr = nr
        self.przystanki = przystanki
    def __str__(self):
        return "Linia(nr: "+self.nr+", przystanki: "+str(self.przystanki)+")"
    def __repr__(self):
        return str(self)

def różnica_czasu(czas1, czas2):
    if len(czas1)!=8 or len(czas2)!=8:
        return 0
    for i in [0, 1, 3, 4, 6, 7]:
        if ord(czas1[i])<ord('0') or ord('9')<ord(czas1[i]) or ord(czas2[i])<ord('0') or ord('9')<ord(czas2[i]):
            return 0
    # czasem pojawia się godzina w błędnej postaci, zwrócenie zera nie jest problemem, pomija odczyt
    return (int(czas1[:2])-int(czas2[:2]))*60*60+(int(czas1[3:5])-int(czas2[3:5]))*60+(int(czas1[6:])-int(czas2[6:]))

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

def pobierz_rozkład_jazdy(nazwa_pliku):
    with open(nazwa_pliku, "w") as plik:
        odpowiedź = requests.get("https://api.um.warszawa.pl/api/action/dbstore_get/?id=1c08a38c-ae09-46d2-8926-4f9d25cb0630&apikey="+config.apiKey)

        przystanki=odpowiedź.json()['result']
            
        for p in przystanki:
            print("pobieram:", p['values'][0]['value'], file=sys.stderr)
            odpowiedź = requests.get("https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=88cd555f-6f31-43ca-9de4-66c479ad5942&busstopId="+p['values'][0]['value']+"&busstopNr="+p['values'][1]['value']+"&apikey="+config.apiKey)

            linie=odpowiedź.json()['result']
                            
            p['linie']=[]
            for l in linie:
                p['linie'].append((l['values'][0]['value'], []))
                odpowiedź = requests.get("https://api.um.warszawa.pl/api/action/dbtimetable_get/?id=e923fa0e-d96c-43f9-ae6e-60518c9f3238&busstopId="+p['values'][0]['value']+"&busstopNr="+p['values'][1]['value']+"&line="+l['values'][0]['value']+"&apikey="+config.apiKey)
                przyjazdy = odpowiedź.json()['result']
                for przyjazd in przyjazdy:
                    p['linie'][-1][1].append((przyjazd['values'][2]['value'],przyjazd['values'][5]['value']))
                                
            plik.write(json.dumps(p)+"\n")
        
def wczytaj_rozkład_jazdy(nazwa_pliku):
    with open(nazwa_pliku, "r") as plik:
        przystanki=[]
        for linia in plik:
            przystanki.append(json.loads(linia))
    rozkład = {}
    for p in przystanki:
        for linia in p['linie']:
            if not linia[0] in rozkład:
                rozkład[linia[0]]=Linia(linia[0], [])
            rozkład[linia[0]].przystanki.append(Przystanek_na_linii([], latlon.LatLon(p['values'][4]['value'], p['values'][5]['value']),p['values'][0]['value'], p['values'][2]['value'], p['values'][1]['value']))
            for godz in linia[1]:
                rozkład[linia[0]].przystanki[-1].godziny_przyjazdu.append(Godzina_przyjazdu(godz[1], godz[0]))
    return rozkład
        
def pobierz_dane(planowany_czas_działania, nazwa_pliku, rozkład=None): # w sekundach
    with open(nazwa_pliku, "w") as plik:
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

        spóźnione_przyjazdy = 0
        
        niespóźnione_przyjazdy = 0
        
        suma_opóźnień = 0

        czas_rozpoczecia = time.time()

        while time.time()-czas_rozpoczecia < planowany_czas_działania:
            
            odpowiedz = requests.get("https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id=%20f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey="+config.apiKey+"&type=1")
                        
            if len(odpowiedz.text) < 100: # wykrywanie błędów pobierania danych
                continue

            dane=odpowiedz.json()
                        

            for autobus in dane['result']:
                if autobus['VehicleNumber'] in autobusy.keys():
                    poprzednia_pozycja=latlon.LatLon(autobusy[autobus['VehicleNumber']]['Lat'], autobusy[autobus['VehicleNumber']]['Lon'])
                    aktualna_pozycja=latlon.LatLon(autobus['Lat'], autobus['Lon'])
                    dystans=poprzednia_pozycja.distance(aktualna_pozycja)
                    zmiana_czasu=różnica_czasu(autobus['Time'][-8:], autobusy[autobus['VehicleNumber']]['Time'][-8:])
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
                            if rozkład!=None and autobus['Lines'] in rozkład: # sprawdzam punktualność
                                for przystanek in rozkład[autobus['Lines']].przystanki:
                                    if aktualna_pozycja.distance(przystanek.pozycja)<=0.05: # jeśli bliżej niż 50m od przystanku, to dojechał
                                        najmniejsza_różnica = 100000
                                        for godz in przystanek.godziny_przyjazdu:
                                            if godz.nr_brygady==autobus['Brigade']:
                                                opóźnienie=różnica_czasu(autobus['Time'][-8:], godz.godzina)//60
                                                if abs(najmniejsza_różnica)>abs(opóźnienie):
                                                    najmniejsza_różnica = opóźnienie
                                        if najmniejsza_różnica<60: # odrzucam pozostałe, bo stanie na pętli itp.
                                            if najmniejsza_różnica>5:
                                                spóźnione_przyjazdy+=1
                                                suma_opóźnień+=najmniejsza_różnica
                                            else:
                                                niespóźnione_przyjazdy+=1
                autobusy[autobus['VehicleNumber']]=autobus
              
            time.sleep(10)
                        
        plik.write("liczba_odczytów:"+"\n")
        plik.write(str(liczba_odczytów)+"\n")

        plik.write("odrzucone_odczyty:"+"\n")
        plik.write(str(odrzucone_odczyty)+"\n")

        plik.write("przekraczające:"+"\n")
        plik.write(str(len(autobusy_przekraczające_prędkość))+"\n")

        plik.write("wszystkie:"+"\n")
        plik.write(str(len(autobusy))+"\n")

        plik.write("prędkości:"+"\n")
        plik.write(str(len(prędkości))+"\n")
        for p in prędkości:
            plik.write(str(p)+"\n")

        lokalizacje = []
        for i in range(50*100):
            if len(autobusy_odwiedzające_lokalizację[i])>=3: # odrzucam miejsca, gdzie było mniej niż 3 autobusy
                lokalizacje.append((len(autobusy_przekraczające_prędkość_w_danej_lokalizacji[i])/len(autobusy_odwiedzające_lokalizację[i]), i, len(autobusy_przekraczające_prędkość_w_danej_lokalizacji[i]), len(autobusy_odwiedzające_lokalizację[i])))
        plik.write("lokalizacje:"+"\n")
        plik.write(str(len(lokalizacje))+"\n")
        for l in lokalizacje:
            plik.write(str(l[0])+" "+str(l[1])+" "+str(l[2])+" "+str(l[3])+"\n")
            
        plik.write("spóźnione_przyjazdy:"+"\n")
        plik.write(str(spóźnione_przyjazdy)+"\n")
        
        plik.write("niespóźnione_przyjazdy:"+"\n")
        plik.write(str(niespóźnione_przyjazdy)+"\n")
        
        plik.write("suma_opóźnień:"+"\n")
        plik.write(str(suma_opóźnień)+"\n")

        if spóźnione_przyjazdy:
            plik.write("średnie_opóźnienia:"+"\n")
            plik.write(str(suma_opóźnień/spóźnione_przyjazdy)+"\n")
            plik.write(str(suma_opóźnień/(spóźnione_przyjazdy+niespóźnione_przyjazdy))+"\n")
