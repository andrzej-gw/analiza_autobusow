Biblioteka do analizowania Warszawskich autobusów, a dokładnie ich prędkości i opóźnień.

Aby użyć należy stworzyć plik config.py, a w nim zmienną apiKey, której wartość należy ustawić
na swój klucz api do strony z danymi autobusów.

Biblioteka pobieranie_danych zawiera 3 istotne funkcje:

    - pobierz_rozkład_jazdy(nazwa_pliku), która pobiera rozkład jazdy i zapisuje go do pliku
    "nazwa_pliku"
    
    - wczytaj_rozkład_jazdy(nazwa_pliku), która wczytuje i zwraca rozkład jazdy z pliku
    "nazwa_pliku"

    - pobierz_dane(planowany_czas_działania, nazwa_pliku, rozkład=None), która pobiera dane
    o autobusach przez zadany czas "planowany_czas_działania" w sekundach i zapisuje je do pliku
    "nazwa_pliku". Jeśli przekazano rozkład jazdy, to zostanie zmierzona również punktualność
    
Biblioteka analiza_danych zawiera funkcję:

    - analizuj(nazwa_pliku), która przeprowadza analizę danych dostarczonych w pliku "nazwa_pliku"
