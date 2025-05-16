# Gra Tower Defense

Projekt przedstawię prostą grę typu **Tower Defense** napisaną w języku **Python** z użyciem biblioteki **Pygame** oraz **threading**. Celem gracza jest obrona swojej bazy przed falami nadciągających przeciwników, poprzez strategiczne rozmieszczanie wież na mapie.

---

## Opis rozgrywki

Gracz obserwuje rozgrywkę z góry i chroni swoją bazę, rozmieszczając wieże wokół wyznaczonej ścieżki, którą poruszają się przeciwnicy. Wrogowie nadciągają falami, a każdy z nich ma inne parametry (szybkość, wytrzymałość).  

Wieże automatycznie atakują przeciwników znajdujących się w ich zasięgu. Kluczem do sukcesu jest wybór odpowiedniego typu wież oraz ich rozmieszczenia w odpowiednich miejscach. Gra kończy się przegraną, gdy przeciwnicy przejdą przez linię obrony zbyt wiele razy.

Podczas gry gracz ma dostęp do **interfejsu HUD**, który wyświetla:
- aktualną liczbę punktów życia (lives),
- dostępną gotówkę (money),
- numer bieżącej fali przeciwników,
- aktualnie wybraną wieżę oraz koszty jej postawienia.

Dzięki temu gracz na bieżąco może kontrolować stan rozgrywki i podejmować strategiczne decyzje.


### Dostępne typy wież:
- **BaseTower** – uniwersalna, zbalansowana wieża o średnim zasięgu i obrażeniach.
- **FastTower** – szybka wieża o niskich obrażeniach i krótkim zasięgu.
- **SniperTower** – bardzo silna wieża dalekiego zasięgu, ale z wolnym czasem ataku.

### Przeciwnicy:
- **FastEnemy** – szybcy, ale słabi.
- **NormalEnemy** – standardowi przeciwnicy.
- **TankEnemy** – bardzo wolni, ale bardzo wytrzymali.

---

## Wątki i synchronizacja danych (threading + locks)

Gra została zaprojektowana z wykorzystaniem **wielowątkowości** w celu oddzielenia logiki rozgrywki od renderowania oraz zapewnienia płynności działania.
Dzięki temu logika przeciwników, wież, pocisków i fal może być przetwarzana równolegle, niezależnie od głównej pętli renderowania, co pozwala uniknąć opóźnień.
### Wątki (`threads.py`)

W trakcje działania programu ruchamiane są cztery równoległe wątki:

| Wątek              | Funkcja                         | Opis                                                                     |
| ------------------ | ------------------------------- |--------------------------------------------------------------------------|
| `enemy_logic`      | `enemy.move()`                  | Odpowiada za poruszanie się przeciwników w czasie rzeczywistym.          |
| `tower_logic`      | `tower.update()`                | Obsługuje logikę wież – wykrywanie przeciwników i generowanie pocisków.  |
| `projectile_logic` | `projectile.move()`             | Zarządza ruchem pocisków oraz ich kolizjami z wrogami, usuwa je, jeśli trafią cel lub wyjdą poza mapę                  |
| `wave_manager`     | `spawn_wave()` i kontrola stanu | Zarządza pojawianiem się nowych fal przeciwników i warunkami zwycięstwa. |

Wszystkie wątki uruchamiane są jako `daemon=True`, co oznacza, że automatycznie kończą działanie przy zamknięciu programu.

```python
threading.Thread(target=enemy_logic, daemon=True).start()
threading.Thread(target=tower_logic, daemon=True).start()
threading.Thread(target=projectile_logic, daemon=True).start()
threading.Thread(target=wave_manager, daemon=True).start()
```

---

### Synchronizacja – `threading.Lock`

Ponieważ dane gry są współdzielone między wątkami (np. lista przeciwników czy poziom życia gracza), zastosowano mechanizmy synchronizacji w postaci **blokad (locks)**.

#### Lista używanych blokad (`game_state.py`):

| Nazwa blokady     | Chronione dane                     | Opis                                                                        |
| ----------------- | ---------------------------------- | --------------------------------------------------------------------------- |
| `enemy_lock`      | `enemies`                          | Zapobiega konfliktom podczas dodawania, usuwania i rysowania przeciwników.  |
| `projectile_lock` | `projectiles`                      | Gwarantuje bezpieczeństwo przy dodawaniu i usuwaniu pocisków.               |
| `money_lock`      | `money`                            | Chroni operacje finansowe, takie jak zakup wież i nagrody za zabicie wroga. |
| `wave_lock`       | `wave`                             | Umożliwia bezpieczne przełączanie numeru aktualnej fali.                    |
| `game_lock`       | `game_over`, `game_won`, `running` | Zapobiega równoczesnej zmianie stanu końca gry przez wiele wątków.          |

#### Przykład użycia blokady:

```python
with enemy_lock:
    for enemy in enemies[:]:
        enemy.move()
```

Blokady zapewniają **atomiczność** operacji oraz chronią przed tzw. **race condition** – sytuacjami, w których wiele wątków modyfikuje te same dane jednocześnie, powodując błędy lub niestabilność gry.

---

## Technologie

- Python 3.10+
- [Pygame](https://www.pygame.org/)  
- Programowanie obiektowe
- Wątki (threading)

## Struktura katalogów

```
TowerDefence/
├── assets.py           # Ładowanie grafik i animacji
├── enemy.py            # Klasy przeciwników i ich logika ruchu
├── game.py             # Początkowa wersja projektu
├── game_state.py       # Globalny stan gry (pieniądze, fale, zamki itd.)
├── HUD.py              # Wyświetlanie interfejsu HUD i podglądu wieży
├── main.py             # Główna logika gry (pętla, renderowanie, interakcje)
├── map.py              # Definicje map i ścieżek
├── pathfinding.py      # Generowanie trasy dla przeciwników
├── settings.py         # Ustawienia gry (stałe, kolory, ekran)
├── threads.py          # Logika wątków (pociski, wieże, fale)
└── tower.py            # Klasy wież i pocisków
```

## Jak uruchomić projekt?

1. **Sklonuj repozytorium:**
   ```bash
   git clone https://github.com/Ellemire/SystemyOperacyjne2-Projekt
   cd SystemyOperacyjne2-Projekt/TowerDefence
    ```

2. **Utwórz środowisko wirtualne:**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # systemie Windows
   . venv/bin/activate  # w systemie Linux
   ```

3. **Zainstaluj zależności:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Uruchom grę:**

   ```bash
   python main.py
   ```
