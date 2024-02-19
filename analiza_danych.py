import matplotlib.pyplot as plt

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
rozmiar_danych = int(input())

L=[]

for i in range(rozmiar_danych):
    L.append(float(input()))
    
L.sort()

print(L)
plt.plot(L)
plt.show()
