# Symulacja ruchu w polu grawitacyjnym
Projekt autorstwa Norbert Drabińskiego

## Spis treści
1. [Opis](#opis)
2. [Struktura](#struktura)
    - [SpaceObject](#spaceobject)
    - [CenterObject](#centerobject)
    - [PointObject](#pointobject)
    - [Collision](#collision)
    - [Simulation](#simulation)
    - [SimulationVisualizer](#simulationvisualizer)
    - [ConfigData](#configdata)
    - [CommandLineInterface](#commandlineinterface)
3. [Instrukcja](#instrukcja)
    - [Ogólny opis uruchamiania](#ogólny-opis-uruchamiania)
    - [Opcjonalne argumenty](#opcjonalne-argumenty)
    - [Przykładowy plik konfiguracyjny](#przykładowy-plik-konfiguracyjny)
4. [Refleksja](#refleksja)

## Opis
Program przyjmuje dane na temat obiektu centralnego, n liczby obiektów punktowych (nie oddziałujących na siebie wzajemnie) oraz właściwości symulacji, a następnie generuje obraz i raport zdarzeń.

Do uruchomienia wykorzystywany jest interfejs wiersza poleceń. Program pozwala na wprowadzenie danych ręcznie przez tryb interaktywny lub przy użyciu pliku JSON. Umożliwia również wprowadzenie dodatkowych argumentów zmieniających wyprowadzony wynik, np. zmieniając kolorystykę. Więcej na ten temat w sekcji [Instrukcja](#instrukcja).

Po przekazaniu przez użytkownika danych program symuluje ruch każdego obiektu punktowego przez podaną ilość kroków oraz wykrywa kolizja zarówno z obiektem centralnym, jak i między sobą.

Wynik domyślnie jest wyświetlany po ukończeniu symulacji, jednak istnieje również opcja zapisuje do pliku. Dodanie argumentu zapisującego symulację powoduje wytworzenie trzech plików:
- Obraz w formacie .png, przedstawiający ślady ruchu obiektów
- Raport zdarzeń w formacie .txt
- Plik konfiguracyjny w formacie .json, który zawiera informacje ze stanu końcowego. Może zostać jako plik konfiguracyjny dla następnego wywołania, aby kontynuować symulacje.

## Struktura
### SpaceObject
Klasa bazowa dla pozostałych dwóch typów obiektów kosmicznych. Posiada jedynie własności wspólne jak pozycja i masa, a także metody wirtualne do konwersji z lub na JSON.

### CenterObject
Jeden z dwóch dostępnych typów obiektów kosmicznych. Jest cały czas stacjonarny, więc nie pozwala na ustawienie pozycji. Jest ona na sztywno ustawiona na punkt (0, 0). Zawiera jednak średnicę.

### PointObject
Drugi z dostępnych typów obiektów kosmicznych. Główny element symulacji - ruchy jego instancji są obliczane i wyświetlane jako wynik symulacji.

### Collision
Prosta klasa, reprezentująca kolizję. Zawiera informacje o kroku, na którym wystąpiła oraz indeksach obiektów, które brały w niej udział.

### Simulation
Kluczowy element programu. Zajmuje się wszystkimi obliczeniami i analizą danych. Dla każdego elementu punktowego wylicza jego prędkość i aplikuje ją przez interfejs PointObject. Dla każdego kroku sprawdza wystąpenie kolizji.

### SimulationVisualizer
Przyjmuje dane wytworzone przez [Simulation](#simulation) i wizualizuje je. Pozwala na utworzenie obrazka przedstawiającego ślady ruchów obiektów punktowych i ich obecne pozycje, oraz na stworzenie tekstowego raportu zdarzeń, opisującego obiekty symulacji, ich pozycje startowe i końcowe, a także kolizje jakie wystąpiły.

### ConfigData
Pomocnicza klasa, służąca do odczytu i zapisu danych konfiguracyjnych. Dzięki niej zapewniony jest jednolity interfejs korzystania z danych otrzymanych zarówno z pliku, jak i z trybu interaktywnego.

### CommandLineInterface
Pozwala na interakcję użytkownika z programem. Zapewnia możliwość wprowadzenia danych konfiguracyjnych i przekazuje je odpowiednim klasom, aby następnie wyświetlić ich wyniki.

## Instrukcja
### Ogólny opis uruchamiania
Aby wystartować program należy uruchomić plik `cli.py` z argumentem określającym źródło danych. Dostępne opcje to:
- `-i` - Tryb interaktywny. Prosi użytkownika kolejno o wszystkie dane niezbędne do uruchomienia symulacji.
- `-f NAZWA_PLIKU` - Odczyt z pliku. Plik musi być w formacie .json i zawierać odpowiednie informacje.

### Opcjonalne argumenty
- `-s`, `--save` - Zapis danych wyjściowych symulacji (tj. obraz w formacie .png, raport w formacie .txt oraz plik konfiguracyjny ze stanem końcowym w formacie .json)
- `-q`, `--quiet` - Program uruchomiony z tym argumentem nie wyświetla swoich wyników. Przeznaczony do użytku razem z `-s`, aby natychmiastowo zapisać symulacje, bez wyświetlania jej.
- `--center-color R G B` - Kolor obiektu centralnego w obrazku końcowym. R, G i B muszą być liczbami całkowitymi (z dowolnego zakresu, jednak są później ściskane do <0, 255>) oznaczającymi kolejno wartość koloru czerwonego, zielonego i niebieskiego.
- `--step-color R G B` - Działa identycznie jak powyższy argument, zmienia jednak kolor śladów ruchu.
- `--point-color R G B` - Działa identycznie jak powyższy argument, zmienia jednak kolor pozycji końcowych obiektów punktowych

### Format pliku konfiguracyjnego
Plik konfiguracyjny musi być plikiem w formacie .json i zawierać następujące dane:
- steps - Całkowitoliczbowa ilość kroków symulacji.
- resolution - Rozdzielczość obrazka końcowego, przedstawiona jako lista dwóch liczb całkowitych.
- meters_per_pixel - Ilość metrów jaką reprezentuje pojedynczy piksel. Wartość liczbowa.
- center_object - Obiekt zawierający następujące dane:
    - diameter - Średnica obiektu centralnego. Wartość liczbowa > 0
    - mass - Masa obiektu centralnego. Wartość liczbowa >= 0
- point_objects - Lista obiektów, z których każdy musi zawierać:
    - velocity - Wektor prędkości danego obiektu punktowego. Lista dwóch wartości liczbowych.
    - mass - Masa danego obiektu punktowego. Wartość liczbowa >= 0
    - position - Wektor oznaczający pozycję danego obiektu punktowego. Listaw dwóch wartości liczbowych.

Warto również wspomnieć, że obiekt centralny zawsze znajduje się na pozycji (0, 0), więc pozycję obiektów punktowych należy do tego dostosować. Tzn. aby obiekt punktowy zaczynał "pod" obiektem centralnym jego pozycja w osi Y musi być mniejsza od 0.

### Przykładowy plik konfiguracyjny
Poniższy plik konfiguracyjny wygeneruje obraz przedstawiający pół obrotu małego satelity wokół orbity Ziemi.
```
{
    "steps": 3000,
    "resolution": [
        512,
        512
    ],
    "meters_per_pixel": 55000.0,
    "center_object": {
        "diameter": 6731000.0,
        "mass": 5.972e+24
    },
    "point_objects": [
        {
            "velocity": [
                7672.0,
                0.0
            ],
            "mass": 1000,
            "position": [
                0.0,
                6771000.0
            ]
        }
    ]
}
```

## Refleksja
Podsumowując, udało mi się wykonać prosty program, który symuluje ruch obiektów wokół danego ciała centralnego w pewnym przybliżeniu. Dokładność symulacji teoretycznie można zmieniać edytując zmienną Simulation._time_step, jednak zdecydowałem się nie pozwalać na to użytkownikom.

Końcowo przez brak czasu nie udało mi się też zrealizować funkcjonalności wykrywania obiektów, które znalazły się niebezpiecznie blisko siebie. Mimo to implementacja tego nie byłaby trudna. Wystarczyłoby dodać kolejną zmienną do oznaczającą jaki dystans definiuje niebezpieczną bliskość i wewnątrz Simulation.run() porównywać z nią dystanse między obiektami.

Planowałem też zapewnić więcej funkcjonalności przez argumenty przekazywane wierszem poleceń. Między innymi miał istnieć kolejny tryb wprowadzania danych, bezpośrednio wywołując komendę i podając wartości jako argumenty. Nie powstał jednak przez pewne ograniczenia biblioteki argparse co do zagnieżdżania grup argumentów oraz ponieważ uznałem go za dużo mniej wygodny w użyciu niż już istniejące tryby.

Z przeszkód dużo bardziej problematyczne niż zakładałem okazało się samo rysowanie symulacji na ekran. Początkowo pozycja obiektu centralnego była ustalana jak środek obrazu. To jednak oznaczało, że zmiana rozdzielczości zmieniała też cały wynik symulacji. Zdecydowałem na rozwiązanie tego problemu przez ustawienie stałej pozycji obiektu centralnego na (0, 0) i rysowanie wyniku tak, aby zawsze był na środku.
To generowało kolejny problem - otóż przestrzeń pikseli obrazu rośnie im niżej znajduje się dany piksel. Aby wynik symulacji był poprawny musiałem jeszcze odbić pozycje punktu w osi Y.