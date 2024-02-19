import matplotlib.pyplot as plt
import requests
import config
import latlon


def numer_lokalizacji_na_lat_lon(nr):
    return (52+(nr%50+0.5)/100, 20.5+(nr//50+0.5)/100)

input()
liczba_odczytów=int(input())
print("liczba_odczytów:")
print(liczba_odczytów)

input()
odrzucone_odczyty=int(input())
print("odrzucone_odczyty:")
print(odrzucone_odczyty)

input()
przekraczające = int(input())
print("przekraczające:")
print(przekraczające)

input()
wszystkie = int(input())
print("wszystkie:")
print(wszystkie)

input()
prędkości = int(input())
print("prędkości:")
print(prędkości)

L=[]
for i in range(prędkości):
    L.append(float(input()))
L.sort()
print(L)

#  plt.plot(L)
#  plt.show()

input()
lokalizacje = int(input())
print("lokalizacje:")
print(lokalizacje)

L=[]
for i in range(lokalizacje):
    a, b, c, d = input().split()
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

#  plt.plot(W)
#  plt.show()

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
