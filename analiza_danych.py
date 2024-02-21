import matplotlib.pyplot as plt
import requests
import config
import latlon


def numer_lokalizacji_na_lat_lon(nr):
    return (52+(nr%50+0.5)/100, 20.5+(nr//50+0.5)/100)

def analizuj(nazwa_pliku):
    with open(nazwa_pliku, "r") as plik:
        plik.readline()
        liczba_odczytów=int(plik.readline())
        print("liczba_odczytów:")
        print(liczba_odczytów)

        plik.readline()
        odrzucone_odczyty=int(plik.readline())
        print("odrzucone_odczyty:")
        print(odrzucone_odczyty)

        plik.readline()
        przekraczające = int(plik.readline())
        print("przekraczające:")
        print(przekraczające)

        plik.readline()
        wszystkie = int(plik.readline())
        print("wszystkie:")
        print(wszystkie)

        plik.readline()
        prędkości = int(plik.readline())
        print("prędkości:")
        print(prędkości)

        L=[]
        for i in range(prędkości):
            L.append(float(plik.readline()))
        L.sort()
        print(L)

        plt.plot(L)
        plt.show()

        plik.readline()
        lokalizacje = int(plik.readline())
        print("lokalizacje:")
        print(lokalizacje)

        L=[]
        for i in range(lokalizacje):
            a, b, c, d = plik.readline().split()
            a = float(a)
            b = int(b)
            c = int(c)
            d = int(d)
            L.append((a, b, c, d))
        L.sort()
        print(L)
        W=[]
        for i in L:
            W.append(i[0])

        plt.plot(W)
        plt.show()

        while True:
            odpowiedź = requests.get("https://api.um.warszawa.pl/api/action/dbstore_get/?id=1c08a38c-ae09-46d2-8926-4f9d25cb0630&apikey="+config.apiKey)

            przystanki=odpowiedź.json()['result']
            
            if len(odpowiedź.text)>100: # wykrywanie błędów podczas pobierania danych
                break

        for line in przystanki:
            print(line)

        for a, b, c, d in L[-5:]:
            lat, lon = numer_lokalizacji_na_lat_lon(b)
            print(a, b, c, d, lat, lon, end=" ")
            najbliższy_przystanek=(1000, przystanki[0])
            A=latlon.LatLon(lat, lon)
            for p in przystanki:
                #  print(p, p['values'][4]['value'])
                B=latlon.LatLon(p['values'][4]['value'], p['values'][5]['value'])
                najbliższy_przystanek=min(najbliższy_przystanek, (A.distance(B), p))
            print(najbliższy_przystanek[1]['values'][2]['value'], "w odległości", najbliższy_przystanek[0], "km")
            
            
        plik.readline()
        spóźnione_przyjazdy = int(plik.readline())
        print("spóźnione_przyjazdy:")
        print(spóźnione_przyjazdy)

        plik.readline()
        niespóźnione_przyjazdy = int(plik.readline())
        print("niespóźnione_przyjazdy:")
        print(niespóźnione_przyjazdy)

        plik.readline()
        suma_opóźnień = int(plik.readline())
        print("suma_opóźnień:")
        print(suma_opóźnień)

        if spóźnione_przyjazdy:
            plik.readline()
            print("średnie_opóźnienia:")
            średnie_opóźnienie = float(plik.readline())
            print(średnie_opóźnienie)
            średni_czas_dojazdu = float(plik.readline())
            print(średni_czas_dojazdu)
analizuj("aaa.txt")
