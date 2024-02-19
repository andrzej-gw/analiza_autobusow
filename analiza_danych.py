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
prędkości = int(input())
print("prędkości:")
print(prędkości)

L=[]
for i in range(prędkości):
    L.append(float(input()))
L.sort()
print(L)

plt.plot(L)
plt.show()

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

plt.plot(W)
plt.show()
