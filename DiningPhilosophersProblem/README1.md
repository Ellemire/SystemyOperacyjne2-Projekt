# Opis problemu:

Problem jedzących filozofów (ang. Dining Philosophers Problem) to klasyczny problem synchronizacji procesów, w którym grupa filozofów siedzi wokół okrągłego stołu, a między każdymi dwoma filozofami leży widelec. Każdy z filozofów w danym momencie może rozmyślać albo jeść. W danym momencie maksymalnie połowa filozofów może jeść, ponieważ każdy z nich potrzebuje do jedzenia dwóch widelców. Problem polega na tym, że filozofowie mogą jednocześnie podnieść tylko jeden widelec, więc w może się zdarzyć sytuacja, w której wszyscy filozofowie będą chcieli jeść i wybiorą widelec po tej samej (prawej albo lewej) stronie, przez co utkną w martwym punkcie i nie będą mogli jeść. 

Na początku każdy z filozofów rozmyśla przez losowy czas, a następnie próbuje jeść. Jeśli nie ma dostępnych widelców, to czeka na ich zwolnienie. Jeżeli filozofowi uda się zjeść, to znowu rozmyśla przez losowy czas, następnie próbuje jeść i tak w kółko.


# Rozwiązanie problemu:

Filozof reprezentowany jest przez funkcję, która wywoływana jest jako wątek.

(Zostanie opisane po rozwiązanu problemu)


Wątki: Filozofowie

Sekcje krytyczne: podnoszenie i opuszczanie widelców


# Instrukcja uruchomienia programu:

1. Zainstaluj kompilator g++, jeżeli jeszcze nie jest zainstalowany.
2. Pobierz ten projekt.
3. Znajdź katalog projektu "DiningPhilosophersProblem" w terminalu.
4. Skompiluj kod przy użyciu g++: `g++ main.cpp -o main.exe`
5. Uruchom program z podaną liczbą filozofów n: `.\main.exe n`
6. Alternatywnie (Linux): Możesz wykorzystać komendę "make" (mam nadzieję).