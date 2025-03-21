# Makefile dla projektu "Dining Philosophers Problem"

# Kompilacja programu
all: main.exe

# Kompilacja pliku .cpp do .o
main.o : main.cpp
    g++ -std=c++11 -c main.cpp

# Linkowanie obiektów w plik wykonywalny
main.exe: main.o
    g++ -std=c++11 main.o -o main.exe

# Usuwanie plików obiektowych i wynikowego
clean:
    rm -f main.o main.exe

# Uruchomienie programu
run: main.exe
	./main.exe $(ARG)