### Kompilator, semestr 2019/2020
Autor: Mateusz Sopiński

### Pliki
- `lexer.py` deklaracja tokenów
- `parser.py` deklaracja gramatyki, wywołania funkcji które generują kod wynikowy
- `config.py` deklaracje stałych pomocniczych
- `exceptions.py` deklaracje obsługiwanych błędów
- `main.py` obsługa wejścia/wyjścia
- `memory.py` moduł służący do zarządzania pamięcią maszyny wirtualnej
- `process.py` moduł służący do ustalenia, indeksów, modyfikacji kodu wyjściowego
- `parsetab.py, parser.out` - pliki wygenerowane przez bibliotekę
- `generator` folder zawierający metody generujące kod wyjściowy
    - `assign.py` przypisanie
    - `condition.py` warunki logiczne
    - `conditional.py` instrukcje warunkowe
    - `const.py` generowanie stałych
    - `expression.py` operatory +,-,*,/,%
    - `io.py` operacje wejścia/wyjścia
    - `loop.py` pętle

### Instalacja
`pip3 install ply==3.11`

### Użycie
`python3 compiler/main.py input_file output_file`
