import sys
from parser import parser, memory_manager

from process import process


def main():
    try:
        input_file = sys.argv[1]
        output_file = sys.argv[2]
    except Exception:
        print('Nieprawidłowa liczba parametrów wejściowych.')
        exit()

    with open(input_file, 'r') as f:
        input_data = f.read()

    # try:
    result = parser.parse(input_data, tracking=True)
    result = process(result, memory_manager)
    # except Exception as e:
    #     print(e)
    #     exit()

    with open(output_file, 'w') as f:
        f.write('\n'.join(result))


if __name__ == '__main__':
    main()
