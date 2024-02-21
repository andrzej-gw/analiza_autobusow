import matplotlib.pyplot as plt
import requests
import config
import latlon


def numer_lokalizacji_na_lat_lon(nr):
    return (52+(nr%50+0.5)/100, 20.5+(nr//50+0.5)/100)

def analizuj(nazwa_pliku):
    fig, axs = plt.subplots(2, 1, constrained_layout=True)

    fig.suptitle('Dane', fontsize=16)

    with open(nazwa_pliku, "r") as plik:
        plik.readline()
        liczba_odczytów=int(plik.readline())

        plik.readline()
        odrzucone_odczyty=int(plik.readline())

        plik.readline()
        przekraczające = int(plik.readline())
        
        plik.readline()
        wszystkie = int(plik.readline())
        
        print("Autobusów, które przekroczyły prędkość było:", przekraczające, "na", wszystkie, "autobusów, czyli", str(int(przekraczające/wszystkie*100))+"%.")
        print("Odrzucano autobusy z prędkościami powyżej 90 km/h oraz te, których lokalizację, były daleko od Warszawy.")
        print("Odrzucono", odrzucone_odczyty,"na",liczba_odczytów, "odczytów, czyli", str(round(odrzucone_odczyty/liczba_odczytów*100, 3))+"%.")
        print()

        plik.readline()
        prędkości = int(plik.readline())

        L=[]
        for i in range(prędkości):
            L.append(float(plik.readline()))
        L.sort()

        axs[0].plot(L)
        axs[0].set_title("Prędkości autobusów")

        plik.readline()
        lokalizacje = int(plik.readline())
        print("Podzielono Warszawę i okolicę na 5000 obszarów, o powierzchni ~ 1km^2.")
        print("Z tych lokalizacji", lokalizacje, "zarejestrowało obecność przynajmniej jednego autobusu.")

        L=[]
        for i in range(lokalizacje):
            a, b, c, d = plik.readline().split()
            a = float(a)
            b = int(b)
            c = int(c)
            d = int(d)
            L.append((a, b, c, d))
        L.sort()
        W=[]
        L1=[]
        for i in L:
            if i[3]>=10: # odrzucam lokalizację z mniej niż 10 autobusami
                W.append(i[0])
                L1.append(i)

        axs[1].plot(W)
        axs[1].set_title("Ile średnio autobusów przekracza prędkość, w różnych lokalizacjach")

        # pobieram dane o przystankach, żeby uzyskać punkt odniesienia do współrzędnych lokalizacji
        while True:
            odpowiedź = requests.get("https://api.um.warszawa.pl/api/action/dbstore_get/?id=1c08a38c-ae09-46d2-8926-4f9d25cb0630&apikey="+config.apiKey)

            przystanki=odpowiedź.json()['result']
            
            if len(odpowiedź.text)>100: # wykrywanie błędów podczas pobierania danych
                break

        print()
        print("Lokalizacje, w których prędkość była najbardziej łamana:")
        for a, b, c, d in reversed(L1[-10:]):
            lat, lon = numer_lokalizacji_na_lat_lon(b)
            print(str(lat)+",", lon, ": prędkość złamało", str(int(a*100))+"% autobusów, najbliższy przystanek od tej lokalizacji to ", end="")
            najbliższy_przystanek=(1000, przystanki[0])
            A=latlon.LatLon(lat, lon)
            for p in przystanki:
                B=latlon.LatLon(p['values'][4]['value'], p['values'][5]['value'])
                najbliższy_przystanek=min(najbliższy_przystanek, (A.distance(B), p))
            print(najbliższy_przystanek[1]['values'][2]['value'], "w odległości", int(najbliższy_przystanek[0]*1000), "m.")
        print()    
        
        plik.readline()
        spóźnione_przyjazdy = int(plik.readline())

        plik.readline()
        niespóźnione_przyjazdy = int(plik.readline())

        plik.readline()
        suma_opóźnień = int(plik.readline())

        print("Dalej statystyki są prowadzone dla przyjazdów, a nie autobusów, czyli jeden autobus może spóźnić się wiele razy.")
        print("Spóźnienie było liczone powyżej 5 minut.")
        print("Na", spóźnione_przyjazdy+niespóźnione_przyjazdy, "spóźnione były", str(spóźnione_przyjazdy)+".")

        if spóźnione_przyjazdy:
            plik.readline()
            średnie_opóźnienie = float(plik.readline())
            średni_czas_dojazdu = float(plik.readline())

            print("Średnie opóźnienie (licząc tylko spóźnione przyjazdy) wyniosło", int(średnie_opóźnienie), "minut.")
            print("Średni czas dojazdu (licząc wszystkie przyjazdy) wyniósł", int(średni_czas_dojazdu), "minut.")
        
        plt.show()
        
analizuj("dane_21_02_1200.txt")
