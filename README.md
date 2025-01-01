# Symulacja ruchu w polu grawitacyjnym
Program służy symulacji ruchu obiektów (nie oddziałujących na siebie wzajemnie) wokół jednego obiektu centralnego oraz wygenerowaniu jej wyniku w postaci obrazu pokazującego ślady ruchu oraz raportu o kolizjach.

Pozwala na konfigurację ustawień symulacji (takich jak rozdzielczość czy ilość kroków) przy wywołaniu oraz wprowadzenie danych symulacji przez ręczne ich wpisanie lub w postaci pliku.

# Struktura projektu
## SpaceObject
Klasa reprezentująca obiekt w przestrzeni kosmicznej. Jest bazą dla pozostałych typów obiektów, więc zawiera jedynie pola pozycji i masy.

## CenterObject
Statyczny obiekt centralny. Rozszerza funkcjonalność SpaceObject o średnicę oraz na stałe ustala swoja pozycję na (0, 0)

## PointObject
Obiekt punktowy, którego ruch jest symulowany. Poza cechami odziedziczonymi od SpaceObject posiada prędkość i możliwość modyfikowania pozycji.

## Simulation
Klasa zajmująca się wykonywaniem obliczeń, przeprowadzaniem symulacji na podstawie podanych danych i przedstawianiem jej wyników.

## gravity_sim.py
Nie jest klasą, a jedynie prostym skryptem zapewniającym interfejs użytkownika do wprowadzenia danych.

# Instrukcja
Program wykonuje się poprzez interfejs CLI. Jedyne wymagane argumenty to ilość kroków oraz sposób wprowadzenia danych.

Istnieją dwa sposoby wprowadzania danych - przez tryb interaktywny (`-i`) lub z pliku (`-f FILE`).

Tryb interaktywny pozwala na ręczne wprowadzenie danych poprzez terminal. Użytkownik jest odpytywany o każdą wartość potrzebną do symulacji. Minimalny przykład wywołania:

`python3 gravity_sim.py 100 -i`

Tryb z pliku daje możliwość wykorzystania pliku .json opisującego każdy obiekt symulacji. Format tego pliku jest zgodny z tym, który można otrzymać zapisując stan końcowy argumentem `-s`. Przykładowy plik:

```
{
    "center_object": {
        "diameter": 6731000.0,
        "mass": 5.972e+24
    },
    "point_objects": [
        {
            "velocity": [
                7000,
                0
            ],
            "mass": 1000,
            "position": [
                55000.0,
                6771000.0
            ]
        }
    ]
}
```
Poza wymienionymi argumentami dostępne są również inne, umożliwiające np. zmianę rozdzielczości wyniku czy ilości metrów na pixel. Aby zobaczyć pełną listę należy wykonać plik `gravity_sim.py` z argumentem `-h`.