import pobieranie_danych
import analiza_danych

if __name__ == "__main__":

    pobieranie_danych.pobierz_rozkład_jazdy("rozklad_przyklad.txt")

    pobieranie_danych.pobierz_dane(60, "dane_przyklad.txt", pobieranie_danych.wczytaj_rozkład_jazdy("rozklad_21_02.txt"))

    analiza_danych.analizuj("dane_przyklad.txt")
    #  analiza_danych.analizuj("dane_21_02_1050.txt")
    #  analiza_danych.analizuj("dane_21_02_1200.txt")
    #  analiza_danych.analizuj("dane_21_02_0110.txt")
